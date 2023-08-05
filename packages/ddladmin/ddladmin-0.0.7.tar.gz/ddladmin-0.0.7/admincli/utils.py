import requests

class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Token ' + self.token
        return r

def print_error(error, message):
    print("[Error] {}".format(error))
    print("[Error Details] {}".format(message))
    return

def print_invalid_command(command, message):
    print("Invalid Syntax for Command `{}`: {}. Type `{} {}` for more information.".format(
            command,
            message,
            MasterServerApi.CMD_HELP,
            command))
    return

def print_table(table, vertical_split="||", horizontal_split="-"):
    s = [[str(e) for e in row] for row in table]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = ('  '+vertical_split+' ').join('{{:{}}}'.format(x) for x in lens)
    output = [fmt.format(*row) for row in s]
    print(horizontal_split*len(output[0]))
    print(output[0])
    print(horizontal_split*len(output[0]))
    print('\n'.join(output[1:]))
    return

def print_accounts_as_table(account_data):
    header = ["UUID", "Type", "Created At", "Email", "Capability"]
    table = [header]
    for account_datum in account_data:
        account_out = []
        account_out.append(account_datum["account_uuid"])
        account_out.append(account_datum["account_type"])
        account_out.append(account_datum["created_at"])
        if account_datum["account_type"] == "worker":
            account_out.append("N/A")
            worker_cap = []
            if account_datum["machine_spec_cpu"] != 0:
                worker_cap.append("cpu")
            if account_datum["machine_spec_gpu"] != 0:
                worker_cap.append("gpu")
            account_out(",".join(worker_cap))
        elif account_datum["account_type"] == "user":
            account_out.append(account_datum["email"])
            account_out.append("N/A")
        else:
            account_out.append("N/A")
            account_out.append("N/A")
        table += [account_out]
    print_table(table, '|', '=')
