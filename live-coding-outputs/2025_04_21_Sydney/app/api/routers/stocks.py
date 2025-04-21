from fastapi import APIRouter, HTTPException, Query, Depends # Add Depends
from typing import List, Optional
from datetime import date, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession # Import AsyncSession for type hinting

from app.models.stock import QuoteRead, HistoricalPriceRead
from app.crud import crud_stock
from app.api.deps import get_db_session # Import the dependency

router = APIRouter()

# Optional endpoint to list available symbols
@router.get(
    "/symbols/",
    response_model=List[str],
    summary="Get Available Mock Symbols",
    tags=["stocks"]
)
async def get_symbols(): # No session needed here as it reads a static list
    """
    Retrieves a list of all available mock stock symbols that can be used
    with the `/quotes/{symbol}` and `/historical/{symbol}` endpoints.
    """
    return crud_stock.get_available_symbols()

# --- Endpoints for quotes and historical data will be added below ---

@router.get(
    "/quotes/{symbol}",
    response_model=QuoteRead,
    summary="Get Latest Mock Quote",
    tags=["stocks"],
    responses={404: {"description": "Symbol not found"}}
)
async def get_quote(
    symbol: str,
    session: AsyncSession = Depends(get_db_session) # Inject session
):
    """
    Retrieves the latest (mock) stock quote for a given symbol by querying
    the most recent historical data point from the database.
    """
    quote = await crud_stock.get_mock_quote(session=session, symbol=symbol.upper()) # Pass session
    if quote is None:
        raise HTTPException(
            status_code=404,
            detail=f"Symbol '{symbol.upper()}' not found or not supported."
        )
    return quote


@router.get(
    "/historical/{symbol}",
    response_model=List[HistoricalPriceRead],
    summary="Get Mock Historical Data",
    tags=["stocks"],
    responses={
        404: {"description": "Symbol not found"},
        422: {"description": "Validation Error (e.g., invalid date format)"}
    }
)
async def get_historical(
    symbol: str,
    session: AsyncSession = Depends(get_db_session), # Inject session
    start_date: Optional[date] = Query(
        None, # Default to None initially
        description="Start date for historical data (YYYY-MM-DD). Defaults to 30 days ago if not provided."
    ),
    end_date: Optional[date] = Query(
        None, # Default to None initially
        description="End date for historical data (YYYY-MM-DD). Defaults to today if not provided."
    )
):
    """
    Retrieves mock historical stock data (OHLCV - Open, High, Low, Close, Volume)
    for a given symbol over a specified date range.

    - If `start_date` is omitted, it defaults to 30 days before `end_date`.
    - If `end_date` is omitted, it defaults to the current date.
    """
    # Set default dates if not provided
    today = date.today()
    if end_date is None:
        end_date = today
    if start_date is None:
        start_date = end_date - timedelta(days=30)

    # Basic validation (FastAPI handles date format validation)
    if start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="Start date cannot be after end date."
        )

    historical_data = await crud_stock.get_mock_historical_data( # Await the async function
        session=session, # Pass session
        symbol=symbol.upper(), # Standardize symbol
        start_date=start_date,
        end_date=end_date
    )

    # crud_stock now returns None only if symbol is invalid
    if historical_data is None:
        # This means the symbol was not found in crud_stock
        raise HTTPException(
            status_code=404,
            detail=f"Symbol '{symbol.upper()}' not found or not supported."
        )

    # crud_stock returns [] for invalid ranges already, but we keep the check above too
    return historical_data
