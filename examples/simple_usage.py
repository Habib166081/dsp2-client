from dsp2_client.core.client import DSP2Client

USERNAME = "mdupuis"
PASSWORD = "111111"

with DSP2Client(username=USERNAME, password=PASSWORD) as client:
    identity = client.get_identity()
    print("Identity:", identity)

    accounts = client.list_accounts()
    for acc in accounts:
        print("Account:", acc)
        balances = client.list_balances(acc.id)
        print("Balances:", balances)
        transactions = client.list_transactions(acc.id, page=1, count=3)
        for tx in transactions:
            print("Transaction:", tx)
