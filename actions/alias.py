def set_account_alias(session, account):
    iam_client = session.client('iam')
    account_id = account['Id']
    account_name = account['Name']
    aliases = iam_client.list_account_aliases()['AccountAliases']
    print(f"Aliases for account {account_id}: {aliases}")
    if len(aliases) < 1:
        try:
            print(f"The following alias: {account_name} will be set for Account: {account_id}.")
            iam_client.create_account_alias(AccountAlias=account_name.lower().replace(' ', '-')[:63])
            print(f"Alias set successfully for account {account_id}")
        except Exception as e:
            print(f"Failed to set alias for account {account_id}: {e}")