import jmespath

class Organization():

    def __init__(self, session) -> None:
        self.client = session.client('organizations')
        self.master_account_id = self.client.describe_organization()['Organization']['MasterAccountId']

    def get_accounts(self, ou_id=None, tag_key=None, tag_value=None, exclude_master=True, recursive=True):
        if ou_id:
            accounts = self.get_accounts_by_ou_id(ou_id, recursive)
        elif tag_key and tag_value:
            accounts = self.get_accounts_by_tag(tag_key, tag_value)
        else:
            accounts = self.get_all_accounts()
        if exclude_master:
            return jmespath.search(f"[?Id != '{self.master_account_id}' && Status == 'ACTIVE']", accounts)
        else:
            return jmespath.search("[?Status=='ACTIVE']", accounts)

    def get_all_accounts(self):
        paginator = self.client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()
        accounts = []
        for response in response_iterator:
            accounts.extend(response['Accounts'])
        return accounts 

    def get_accounts_by_tag(self, tag_key, tag_value): 
        return [account for account in self.get_all_accounts() if account['Tags'].get(tag_key) == tag_value]        

    def get_accounts_by_ou_id(self, ou_id, recursive):
        accounts = []
        self._get_member_accounts_recursive(ou_id, accounts, recursive)
        return accounts 

    def _get_member_accounts_recursive(self, ou_id, accounts, recursive):
        paginator = self.client.get_paginator('list_accounts_for_parent')
        response_iterator = paginator.paginate(ParentId=ou_id)
        for response in response_iterator:
            res_accounts = response['Accounts']
            accounts.extend(res_accounts)
        if recursive:
            ou_response = self.client.list_organizational_units_for_parent(ParentId=ou_id)
            children_ous = ou_response['OrganizationalUnits']
            for child_ou in children_ous:
                child_ou_id = child_ou['Id']
                self._get_member_accounts_recursive(child_ou_id, accounts)