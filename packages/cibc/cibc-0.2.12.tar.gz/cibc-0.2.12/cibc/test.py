from . import banking
import os

dirr = os.path.abspath(os.path.filename(__file__))


if __name__ == '__main__':
    c = CIBC('username', 'password')
    c.Accounts() # grab the accounts associated with this username and login
    c.gTransactions(dateFrom=datetime.datetime(year=2018, month=9,day=1),dateUntil= datetime.datetime(year=2018, month=9, day=17)) # for each account, get all the transactions in this range
    accounts = c.accounts
    for account in accounts:
        account.tocsv('C:\\Users\\louis\\Desktop\\{}.csv'.format(account))
        print(account.tolist())

    # print(account)
    # print(len(account.diff()))
    # print(len(account.tolist()))