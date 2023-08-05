import re
import json
import traceback as tb

from admincli.utils import *
from admincli.api import *

# A global alias table
alias_table = {}
alias_re = re.compile('(^[a-zA-z]+)[a-zA-z0-9]*')

class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)

class QueryRuntimeError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Collection:
    collection_queryed = []
    collection_eval = []

    def __init__(self, meta, collection):
        global alias_table
        self.meta = meta
        self.friend_name = collection
        # <COLLECTION> must be of the form <NAME>, or <NAME>(<FIELD>,...)
        # If there is left parenthesis in the collection, then there must be a
        # right parenthesis at the end.
        if collection.count("(") > 1 or collection.count(")") > 1:
            raise ParseError("Collection `{}` invalid. Must be of the form <NAME>, or <NAME>(<FIELD>,...)".format(collection))

        collection_name = collection
        fields = []
        lp_index = collection.find("(")
        if lp_index == 0:
            raise ParseError("Collection `{}` invalid. Must be of the form <NAME>, or <NAME>(<FIELD>,...)".format(collection))
        elif lp_index != -1:
            if collection[-1] != ")":
                raise ParseError("Collection `{}` invalid. Must be of the form <NAME>, or <NAME>(<FIELD>,...)".format(collection))
            collection_name = collection[:lp_index]
            fields_raw = collection[lp_index+1:-1].split(",")
            fields = [field.strip() for field in fields_raw if len(field) > 0]

        # Make sure the collection is defined.
        if collection_name not in alias_table and collection_name not in self.meta["tables"]:
            raise ParseError("Collection <NAME> `{}` unrecognized. Must be previously aliased or one of {}".format(collection_name, self.meta["tables"]))

        collection_supported_fields = []
        if collection_name in alias_table:
            aliased_collection = alias_table[collection_name]
            collection_supported_fields = aliased_collection.fields
        else:
            collection_supported_fields = self.meta["table_fields"][collection_name]

        self.collection_supported_fields = collection_supported_fields
        whole_object = False
        # Make sure each fields are supported.
        if len(fields) > 0:
            for field in fields:
                if field not in collection_supported_fields:
                    raise ParseError("Collection <FIELD> `{}` unrecognized. Must be one of {}".format(field, collection_supported_fields))
        else:
            fields = collection_supported_fields
            whole_object = True

        self.collection_name = collection_name
        if self.collection_name in self.meta["tables"]:
            self.real_name = self.collection_name
        else:
            self.real_name = alias_table[self.collection_name].real_name
        self.fields = fields
        self.whole_object = whole_object
        self.primary_key = self.meta["table_primary"][self.real_name]

class Condition:
    def __init__(self, meta, collection, condition, level):
        self.meta = meta
        self.collection = collection

        # <CONDITION> must be of the form:
        # - <FIELD>=<STR>,...
        # - <FIELD>=<QUERY>
        # - <FIELD>=...&<FIELD>=...&...

        parsed_conditions = {}
        sub_conditions = condition.split("&")
        for sub_condition in sub_conditions:
            condition_to_parse = sub_condition
            eq_index = condition_to_parse.find("=")
            if eq_index == -1:
                raise ParseError("Condition `{}` invalid. Must be of the form FIELD>=<STR>,... or <FIELD>=<QUERY> or <FIELD>=...&<FIELD>=...&...".format(
                                    condition_to_parse))

            field = condition_to_parse[:eq_index].strip()
            # Make sure the field is in the collection.
            if field not in self.collection.collection_supported_fields:
                raise ParseError("Condition <FIELD> `{}` unrecognized. Must be in the <COLLECTION> `{}` {}".format(
                                    field,
                                    self.collection.friend_name,
                                    self.collection.collection_supported_fields))

            if field not in parsed_conditions:
                parsed_conditions[field] = []

            current_condition = condition_to_parse[eq_index+1:].strip()
            if current_condition == '':
                raise ParseError("Condition `{}` invalid. Must be of the form FIELD>=<STR>,... or <FIELD>=<QUERY> or <FIELD>=...&<FIELD>=...&...".format(condition_to_parse))
            # Attempt to parse as Query. If failed, treat as plain string.
            try:
                subquery = Query(meta, current_condition, level)
                parsed_conditions[field].append(subquery)
            except:
                values = current_condition.split(",")
                parsed_conditions[field] += values

        self.parsed_conditions = parsed_conditions

    def eval(self, api, cred):
        fields_evaled = {}
        fields = list(self.parsed_conditions.keys())
        for field in fields:
            fields_evaled[field] = []
            values = self.parsed_conditions[field]
            for value in values:
                if isinstance(value, Query):
                    fields_evaled[field] += value.eval(api, cred)
                else:
                    fields_evaled[field].append(value)

        return fields_evaled

class Query:
    QUERY_CMD_SELECT = "select"
    QUERY_CMD_CREATE = "create"
    QUERY_CMD_DELETE = "delete"

    SUPPORTED_QUERY_COMMANDS = [
        QUERY_CMD_SELECT,
        QUERY_CMD_CREATE,
        QUERY_CMD_DELETE
    ]

    QUERY_CMD_SELECT_WHERE = "where"

    RESERVED_KEYWORDS = [
        QUERY_CMD_SELECT,
        QUERY_CMD_CREATE,
        QUERY_CMD_DELETE,
        QUERY_CMD_SELECT_WHERE
    ]

    def __init__(self, meta, query, level):
        global alias_table
        global alias_re
        if query in alias_table:
            self.aliased = True
            self.aliased_collection = alias_table[query]
            self.query_str = query
        else:
            self.aliased = False
            self.query_str = query
            query = query.lower()
            self.meta = meta
            parsed_tokens = {}
            # A query is a space separated string.
            query_tokens = query.split(" ")
            if len(query_tokens) < 2:
                raise ParseError("Query `{}` invalid. Must be of the form [<ALIAS> =] <CMD> <COLLECTION> [WHERE <CONDITION>]".format(query))

            # Determine command and (optional) alias.
            command = query_tokens[0]
            query_left = query_tokens[1:]
            aliased = False
            while True:
                if command not in self.SUPPORTED_QUERY_COMMANDS:
                    # A special case is if the query is aliased. This is only allowed for the
                    # outter-most query statement.
                    if level == 0 and not aliased:
                        if len(query_tokens) < 4:
                            raise ParseError("Query `{}` invalid. Must be of the form [<ALIAS> =] <CMD> <COLLECTION> [WHERE <CONDITION>]".format(query))

                        if query_tokens[1] != "=":
                            raise ParseError("Query `{}` invalid. Must be of the form [<ALIAS> =] <CMD> <COLLECTION> [WHERE <CONDITION>]".format(query))

                        alias = command
                        if not alias_re.match(alias):
                            raise ParseError("Query <ALIAS> `{}` invalid. Must start with an alphabet character and only use alphabet characters and numbers".format(alias))

                        if alias in self.RESERVED_KEYWORDS:
                            raise ParseError("Query <ALIAS> `{}` invalid. `{}` is a reserved keyword".format(alias, alias))

                        if alias in self.meta["tables"]:
                            raise ParseError("Query <ALIAS> `{}` invalid. `{}` is a reserved name".format(alias, alias))

                        command = query_tokens[2]
                        query_left = query_tokens[3:]
                        aliased = True
                        parsed_tokens["alias"] = alias
                        continue
                    elif aliased:
                        raise ParseError("Query `{}` invalid. Must be of the form [<ALIAS> =] <CMD> <COLLECTION> WHERE <CONDITION>]".format(query))
                    else:
                        raise ParseError("Query <CMD> `{}` invalid. <CMD> must be one of {}".format(
                                            command, SUPPORTED_QUERY_COMMANDS))
                else:
                    parsed_tokens["command"] = command
                    break

            # Look for keyword `where`. If `where` is found, then it is the anchor point to
            # locate the <COLLECTION>. Otherwise, the rest of the command is <COLLECTION>.
            index = 0
            collection_str = ' '.join(query_left)
            condition_str = ' '
            for token in query_left:
                if token == self.QUERY_CMD_SELECT_WHERE:
                    collection_str = ' '.join(query_left[:index])
                    condition_str = ' '.join(query_left[index+1:])
                    break
                index += 1

            collection_str = collection_str.strip()
            condition_str = condition_str.strip()
            if collection_str in self.RESERVED_KEYWORDS:
                raise ParseError("Query <COLLECTION> `{}` invalid. `{}` is a reserved keyword".format(collection_str, collection_str))

            # Parse the collection.
            parsed_tokens["collection"] = Collection(self.meta, collection_str)

            # If there is still a condition left, parse the condition.
            if condition_str != '':
                parsed_tokens["condition"] = Condition(self.meta, parsed_tokens["collection"], condition_str, level+1)

            self.tokens = parsed_tokens

    def eval(self, api, cred):
        if self.aliased:
            collection = self.aliased_collection
            return collection.collection_eval
        else:
            # First, evaluation the condition if exists.
            condition_evaled = {}
            if "condition" in self.tokens:
                condition_evaled = self.tokens["condition"].eval(api, cred)

            query_data = {
                "command" : self.tokens["command"],
                "condition" : json.dumps(condition_evaled)
            }

            query_results = api.query(cred, self.tokens["collection"].real_name, query_data)
            if query_results is None:
                raise QueryRuntimeError("Query Execution Failure at `{}`".format(self.query_str))

            collection = self.tokens["collection"]
            collection.collection_queryed = query_results
            if "alias" in self.tokens:
                alias_table[self.tokens["alias"]] = collection

            # If the collection specifies the whole object, replace that with the primary key.
            if collection.whole_object:
                values = []
                for result in query_results:
                    values.append(result[collection.primary_key])
            else:
                values = []
                header = collection.fields
                for value in query_results:
                    for item in header:
                        values.append(value[item])

            collection.collection_eval = values
            return values

    def get_collection(self):
        if self.aliased:
            return self.aliased_collection
        else:
            return self.tokens["collection"]

def query(api, cred, command):
    global alias_table
    try:
        q = Query(cred["meta"], command, 0)
        q.eval(api, cred)
        collection = q.get_collection()

        # Print the collection.
        header = collection.fields
        table = [header]
        for value in collection.collection_queryed:
            row = []
            for item in header:
                row.append(value[item])
            table.append(row)

        print_table(table)
    except Exception as e:
        print_error(str(e), tb.format_exc())
        return
