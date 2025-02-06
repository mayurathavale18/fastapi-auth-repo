from fastapi import APIRouter, Query, HTTPException
import pandas as pd
import os

router = APIRouter()

COMPACT_FILE_PATH = os.getenv("COMPACT_FILE_PATH")
DETAILED_FILE_PATH = os.getenv("DETAILED_FILE_PATH")

@router.get("/instruments/")
def get_filtered_instruments(
    exchange: str = Query(None),
    segment: str = Query(None),
    symbol: str = Query(None),
    detailed: bool = Query(False)  # Toggle for detailed CSV
):
    """Returns filtered instrument data from the stored CSV file."""
    file_path = DETAILED_FILE_PATH if detailed else COMPACT_FILE_PATH

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Instrument list not available yet.")

    df = pd.read_csv(file_path, keep_default_na=False)

    # Apply filters
    if exchange:
        df = df[df["EXCH_ID"] == exchange]
    if segment:
        df = df[df["SEGMENT"] == segment]
    if symbol:
        df = df[df["SYMBOL_NAME"].str.contains(symbol, case=False, na=False)]

    return df.to_dict(orient="records")
