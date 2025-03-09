from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from datetime import datetime as dt, date, timezone
# from DateTime.DateTime import datetime as dt

class OrderSchema(BaseModel):
    afterMarketOrder: Optional[bool] = False
    amoTime: Optional[str] = ""
    boProfitValue: Optional[str] = ""
    boStopLossValue: Optional[str] = ""
    correlationId: str = "123ab8"
    dhanClientId: str ="1000003"
    disclosedQuantity: str = ""
    exchangeSegment: str ="NSE"
    orderType: str ="MARKET"
    price: Optional[str] = ""
    productType: str = "INTRADAY"
    quantity: str = "1"
    securityId: str =""
    transactionType: str ="SELL"
    triggerPrice: Optional[str] = ""
    validity: str="DAY"
    
