from time import sleep


def read_account_alias(session, account, dry_run):
    iam_client = session.client('iam')
    account_id = account['Id']
    sleep(10)
    if not dry_run:
        aliases = iam_client.list_account_aliases()['AccountAliases']
        print(f"Aliases for account {account_id}: {aliases}")