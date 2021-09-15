from app.accounts.models import Account


def get_account(account_id):
    """Get account by id

    Args:
        account_id (int): id

    Returns:
        [Account]: account with the id
    """
    return Account.objects.get(pk=account_id)
