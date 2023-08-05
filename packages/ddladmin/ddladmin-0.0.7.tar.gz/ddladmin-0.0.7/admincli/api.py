import json
import requests

from admincli.utils import *

class MasterServerApi:
    def __init__(self, master_endpoint):
        self.master_endpoint = master_endpoint

    def login(self, access_id, password):
        resp = requests.post("{}/api/v1/admin/login/".format(self.master_endpoint),
                             data={'access_id':access_id, 'password':password})

        resp_data = json.loads(resp.text)
        if resp.ok == False:
            print_error(resp_data.get("error"), resp_data.get("message"))
            return None
        else:
            auth_token = TokenAuth(resp_data.get('auth_token'))
            account_data = resp_data.get('account_data')
            meta = resp_data.get('meta')
            return {"auth_token" : auth_token, "account_data" : account_data, "meta" : meta}

    def logout(self, cred):
        requests.post("{}/api/v1/admin/logout/".format(self.master_endpoint), auth=cred["auth_token"])
        return

    def query(self, cred, collection, query_data):
        resp = requests.post("{}/api/v1/admin/query/{}/".format(self.master_endpoint, collection), data=query_data, auth=cred["auth_token"])
        resp_data = json.loads(resp.text)
        if resp.ok == False:
            print_error(resp_data.get("error"), resp_data.get("message"))
            return None
        else:
            return resp_data