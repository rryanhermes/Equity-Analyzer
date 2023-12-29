from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Replace host and port with your TWS/Gateway details

account = ib.accountSummary()
util.df(account)

# Disconnect from IB
ib.disconnect()
