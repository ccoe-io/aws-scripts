import jmespath
import boto3
class Organization():

    def __init__(self, session) -> None:
        self.session = session
        sts_client = session.client('sts')
        self.account_id = sts_client.get_caller_identity()['Account']
        self.client = session.client('organizations')

    def get_member_accounts(self, ou_id=None, tag_key=None, tag_value=None):
        if ou_id:
            return self.get_all_member_accounts_by_ou_id(ou_id)
        elif tag_key and tag_value:
            return self.get_all_member_accounts_by_tag(tag_key, tag_value)
        else:
            return self.get_all_member_accounts()

    def get_all_member_accounts_by_ou_id(self, ou_id):
        member_accounts = []
        self._get_member_accounts_recursive(ou_id, member_accounts)
        return jmespath.search("[?Status=='ACTIVE'].Id", member_accounts)

    def _get_member_accounts_recursive(self, ou_id, member_accounts):
        paginator = self.client.get_paginator('list_accounts_for_parent')
        response_iterator = paginator.paginate(ParentId=ou_id)

        for response in response_iterator:
            accounts = response['Accounts']
            member_accounts.extend(accounts)

        # Get the children OUs
        ou_response = self.client.list_organizational_units_for_parent(ParentId=ou_id)
        children_ous = ou_response['OrganizationalUnits']
        for child_ou in children_ous:
            child_ou_id = child_ou['Id']
            self._get_member_accounts_recursive(child_ou_id, member_accounts)

    def get_all_member_accounts_by_tag(self, tag_key, tag_value):
        paginator = self.client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()

        member_accounts = []
        for response in response_iterator:
            member_accounts.extend(response['Accounts'])
        
        accounts = [account for account in member_accounts if account['Tags'].get(tag_key) == tag_value]        
        return jmespath.search("[?Status=='ACTIVE'].Id", accounts)

    def get_all_member_accounts(self):
        paginator = self.client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()

        member_accounts = []
        for response in response_iterator:
            member_accounts.extend(response['Accounts'])

        return jmespath.search(f"[?Id != '{self.account_id}' && Status == 'ACTIVE'].Id", member_accounts)