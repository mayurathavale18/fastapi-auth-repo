# from .database import engine, Base

# # Recreate all tables
# Base.metadata.create_all(bind=engine)

# print("Tables recreated successfully.")

data = (afterMarketOrder=False amoTime='' boProfitValue='' boStopLossValue='' correlationId='123ab8' dhanClientId='1100795679' disclosedQuantity='' exchangeSegment='NSE' orderType='MARKET' price='' productType='INTRADAY' quantity='1' securityId='2029' transactionType='SELL' triggerPrice='' validity='DAY').dict()

print(data)