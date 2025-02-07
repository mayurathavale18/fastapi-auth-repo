from fastapi import APIRouter, Query, HTTPException, Request

router = APIRouter()

@router.get("/instruments/")
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
