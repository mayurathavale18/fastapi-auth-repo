from fastapi import APIRouter, HTTPException, Request
import pandas as pd
import httpx
import asyncio
from app.utils.websocket import ws_client

router = APIRouter()

@router.get("/")
def get_filtered_instruments(request: Request, detailed: bool = False):
    """Returns filtered instrument data from the stored CSV file."""
    df = request.app.state.detailed_df if detailed else request.app.state.compact_df

    if df is None:
        raise HTTPException(status_code=404, detail="Instrument list is not available.")

    return df.to_dict(orient="records")


@router.get("/holdings")
async def get_instruments_list_for_holdings(request: Request):
    """Fetch user holdings, extract relevant instruments, and store them in state."""
    
    # Step 1: Fetch holdings data
    async with httpx.AsyncClient() as client:
        response = await client.get(str(request.url_for("get_holdings")))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch holdings")

    request.app.state.holdings = response.json()

    # Step 2: Extract security IDs
    holdings = request.app.state.holdings
    security_ids = {str(holding["securityId"]) for holding in holdings if "securityId" in holding}

    # Step 3: Get instrument data
    df: pd.DataFrame = request.app.state.compact_df  
    if df is None:
        raise HTTPException(status_code=404, detail="Instrument list is not available.")

    df.columns = df.columns.str.strip()

    # Ensure correct column name is used
    security_id_column = "SEM_SMST_SECURITY_ID" if "SEM_SMST_SECURITY_ID" in df.columns else None
    if not security_id_column:
        raise HTTPException(status_code=400, detail="Security ID column not found in DataFrame")

    df[security_id_column] = df[security_id_column].astype(str)

    print("🔍 Unique security IDs in CSV:", df[security_id_column].unique())  # Debugging

    # Filter DataFrame: Match security IDs AND Instrument Name = "EQUITY"
    filtered_df = df[(df[security_id_column].isin(security_ids)) & (df["SEM_INSTRUMENT_NAME"] == "EQUITY")]

    instruments_list = filtered_df.to_dict(orient="records")
    
    # Step 4: Store the result in request.app.state
    request.app.state.instruments_in_holdings = instruments_list

    # ✅ Start WebSocket with updated instruments
    print(f"🚀 Starting WebSocket with {len(instruments_list)} instruments...")
    asyncio.create_task(ws_client.run(instruments_list))

    # Step 5: Return the filtered instruments
    return {"instruments_in_holdings": instruments_list}
