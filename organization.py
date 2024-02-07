import jmespath

class Organization():

    def __init__(self, session) -> None:
        self.session = session
        self.client = session.client('organizations')

    def get_member_accounts(self, ou_id=None, tag_key=None, tag_value=None):
        if ou_id:
            return self.get_all_member_accounts_by_ou_id(ou_id)
        elif tag_key and tag_value:
            return self.get_all_member_accounts_by_tag(tag_key, tag_value)
        else:
            return self.get_all_member_accounts()
        
    def get_all_member_accounts(self):
        response = self.client.list_accounts()

        member_accounts = response['Accounts']
        while 'NextToken' in response:
            response = self.client.list_accounts(NextToken=response['NextToken'])
            member_accounts.extend(response['Accounts'])

        return jmespath.search("[].Id", member_accounts)

    def get_all_member_accounts_by_ou_id(self, ou_id):
        response = self.client.list_accounts_for_parent(ParentId=ou_id)

        member_accounts = response['Accounts']
        while 'NextToken' in response:
            response = self.client.list_accounts_for_parent(ParentId=ou_id, NextToken=response['NextToken'])
            member_accounts.extend(response['Accounts'])

        return jmespath.search("[].Id", member_accounts)

    def get_all_member_accounts_by_tag(self, tag_key, tag_value):
        response = self.client.list_accounts()

        member_accounts = response['Accounts']
        while 'NextToken' in response:
            response = self.client.list_accounts(NextToken=response['NextToken'])
            member_accounts.extend(response['Accounts'])
        
        accounts = [account for account in member_accounts if account['Tags'].get(tag_key) == tag_value]        
        return jmespath.search("[].Id", accounts)