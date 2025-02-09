from fastapi import APIRouter, Query, HTTPException, Request
import pandas as pd
import httpx

router = APIRouter()

@router.get("/")
def get_filtered_instruments(
    # exchange: str = Query(None),
    # segment: str = Query(None),
    # symbol: str = Query(None),
    request: Request,
    detailed: bool = Query(False)  # Toggle for detailed CSV
):
    """Returns filtered instrument data from the stored CSV file."""
    df = request.app.state.detailed_df if detailed else request.app.state.compact_df

    if df is None:
        raise HTTPException(status_code=404, detail="Instrument list is not available.")


    # # Apply filters
    # if exchange:
    #     df = df[df["EXCH_ID"] == exchange]
    # if segment:
    #     df = df[df["SEGMENT"] == segment]
    # if symbol:
    #     df = df[df["SYMBOL_NAME"].str.contains(symbol, case=False, na=False)]

    return df.to_dict(orient="records")


@router.get("/holdings")
async def get_instruments_list_for_holdings(request: Request):
    """Fetch user holdings, extract relevant instruments, and store them in state."""
    
    # Step 1: Call /user/holdings to update request.app.state.holdings
    async with httpx.AsyncClient() as client:
        response = await client.get(
            str(request.url_for("get_holdings"))  # Calls the /user/holdings API
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch holdings")

    request.app.state.holdings = response.json()  # Update state

    # Step 2: Extract security_id values
    holdings = request.app.state.holdings  # Use the list directly
    security_ids = {str(holding["securityId"]) for holding in holdings if "securityId" in holding}  

    # Step 3: Get compact_df and filter relevant instruments
    df: pd.DataFrame = request.app.state.compact_df  # Load compact_df
    if df is None:
        raise HTTPException(status_code=404, detail="Instrument list is not available.")

    # Debugging: Print available columns in the DataFrame
    print("DataFrame columns:", df.columns)

    # Ensure correct column name is used
    security_id_column = "SEM_SMST_SECURITY_ID" if "SEM_SMST_SECURITY_ID" in df.columns else None
    if not security_id_column:
        raise HTTPException(status_code=400, detail="Security ID column not found in DataFrame")
    
    # Convert column to str for comparison
    df[security_id_column] = df[security_id_column].astype(str)

    print("🔍 Unique security IDs in CSV:", df[security_id_column].unique())  # Debugging

    # Filter DataFrame: Match security IDs AND Instrument Name = "EQUITY"
    filtered_df = df[df[security_id_column].isin(security_ids) & (df["SEM_INSTRUMENT_NAME"] == "EQUITY")]  

    instruments_list = filtered_df.to_dict(orient="records")
    
    # Step 4: Store the result in request.app.state
    request.app.state.instruments_in_holdings = instruments_list

    # Step 5: Return the filtered instruments
    return {"instruments_in_holdings": instruments_list}