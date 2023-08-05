from admincli.parse import *

CMD_HELP = "help"
CMD_LOGOUT = "logout"

def help_select():
    print("Command: [<ALIAS> =] {} <COLLECTION> [{} <CONDITION>]".format(Query.QUERY_CMD_SELECT, Query.QUERY_CMD_SELECT_WHERE))
    print("")
    print("Examples:")
    print("  - SELECT account")
    print("     ** Selects all information of all accounts")
    print("  - SELECT account(account_uuid, account_type)")
    print("     ** Selects (account_uuid, account_type) of all accounts")
    print("  - SELECT account WHERE account_type=worker")
    print("     ** Selects all information of all accounts that have `account_type` equal to `worker`")
    print("  - SELECT task WHERE parent_job_uuid=<UUID>")
    print("     ** Selects all information of all children tasks of job with `<UUID>`")


def help_create():
    print("create")

def help_delete():
    print("delete")

def help_general():
    print("Supported Commands:")
    print("\t- {}".format(CMD_HELP))
    print("\t- {}".format(CMD_LOGOUT))
    for command in Query.SUPPORTED_QUERY_COMMANDS:
        print("\t- {}".format(command))
    print("")
    print("Type `{} <Command>` for information about the command".format(CMD_HELP))

def help_logout():
    print("logout")

def help(commands):
    if len(commands) == 1:
        help_general()
    else:
        command_to_help = commands[1]
        if command_to_help.lower() == Query.QUERY_CMD_SELECT:
            help_select()
        elif command_to_help.lower() == Query.QUERY_CMD_CREATE:
            help_create()
        elif command_to_help.lower() == Query.QUERY_CMD_DELETE:
            help_delete()
        elif command_to_help.lower() == CMD_LOGOUT:
            help_logout()
        else:
            help_general()
