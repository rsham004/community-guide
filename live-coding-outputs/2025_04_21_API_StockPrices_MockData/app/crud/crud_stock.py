import random
from datetime import datetime, date, timedelta
from typing import List, Optional

from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.stock import QuoteRead, HistoricalPriceRead, HistoricalPrice

# Define a static list of mock symbols
MOCK_SYMBOLS = ["MOCK", "FAKE", "TEST", "SMPL", "DEMO"]

def get_available_symbols() -> List[str]:
    """Returns the list of available mock symbols."""
    return MOCK_SYMBOLS

async def seed_initial_data(session: AsyncSession, num_days: int = 365 * 2):
    """
    Populates the database with mock historical data if it's empty.
    Generates data for the past `num_days`.
    """
    print(f"Checking if initial data seeding is required for {len(MOCK_SYMBOLS)} symbols...")

    # Check if data already exists for the first symbol to prevent reseeding
    first_symbol = MOCK_SYMBOLS[0]
    statement = select(HistoricalPrice).where(HistoricalPrice.symbol == first_symbol).limit(1)
    result = await session.exec(statement)
    existing_data = result.first()

    if existing_data:
        print("Database already seeded. Skipping initial data generation.")
        return

    print(f"Seeding database with historical data for the past {num_days} days...")
    today = date.today()
    start_date_seed = today - timedelta(days=num_days)

    all_prices_to_add: List[HistoricalPrice] = []

    for symbol in MOCK_SYMBOLS:
        print(f"Generating data for symbol: {symbol}")
        historical_data_symbol: List[HistoricalPrice] = []
        current_date = start_date_seed
        # Start with a base price influenced by the symbol
        base_price = 100 + (len(symbol) * 10)
        last_close = base_price # Initialize last close price

        while current_date <= today:
            # Simulate daily price fluctuations based on the previous day's close
            open_price = last_close + random.uniform(-1.5, 1.5) # Slightly wider fluctuation
            open_price = round(max(0.1, open_price), 2) # Ensure price doesn't go below 0.1

            # Simulate High, Low, Close relative to Open
            high_price = round(open_price + random.uniform(0, 4), 2) # Wider range possible
            low_price = round(open_price - random.uniform(0, 4), 2)
            # Ensure low isn't higher than open/high or below 0.1
            low_price = round(min(open_price, high_price, max(0.1, low_price)), 2)
            close_price = round(random.uniform(low_price, high_price), 2)

            # Simulate Volume
            volume = random.randint(5000, 1000000) # Wider volume range

            historical_data_symbol.append(
                HistoricalPrice( # Use the table model here
                    symbol=symbol,
                    date=current_date,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    volume=volume,
                )
            )
            last_close = close_price # Update last close for next day's calculation
            current_date += timedelta(days=1)

        all_prices_to_add.extend(historical_data_symbol)

    print(f"Adding {len(all_prices_to_add)} historical price records to the database...")
    session.add_all(all_prices_to_add)
    await session.commit()
    print("Database seeding complete.")


async def get_mock_quote(session: AsyncSession, symbol: str) -> Optional[QuoteRead]:
    """
    Retrieves the latest historical data point for a symbol from the DB
    and returns it as a 'quote'.
    Returns None if the symbol is not recognized or has no data.
    """
    if symbol not in MOCK_SYMBOLS:
        return None

    statement = (
        select(HistoricalPrice)
        .where(HistoricalPrice.symbol == symbol)
        .order_by(col(HistoricalPrice.date).desc())
        .limit(1)
    )
    result = await session.exec(statement)
    latest_historical = result.first()

    if not latest_historical:
        return None

    # Create a QuoteRead object from the latest historical data
    return QuoteRead(
        symbol=latest_historical.symbol,
        price=latest_historical.close, # Use closing price as the 'current' quote price
        timestamp=datetime.combine(latest_historical.date, datetime.min.time()) # Use date as timestamp
    )


async def get_mock_historical_data(
    session: AsyncSession, symbol: str, start_date: date, end_date: date
) -> Optional[List[HistoricalPriceRead]]:
    """
    Retrieves historical stock data points (OHLCV) from the database
    for a given symbol and date range.
    Returns None if the symbol is not recognized.
    Returns an empty list if the date range yields no data.
    """
    if symbol not in MOCK_SYMBOLS:
        return None # Symbol not supported

    statement = (
        select(HistoricalPrice)
        .where(HistoricalPrice.symbol == symbol)
        .where(HistoricalPrice.date >= start_date)
        .where(HistoricalPrice.date <= end_date)
        .order_by(HistoricalPrice.date)
    )
    result = await session.exec(statement)
    historical_data = result.all()

    # Convert HistoricalPrice (table model) to HistoricalPriceRead (API model)
    # In this case, they are identical, but this pattern is good practice
    return [HistoricalPriceRead.model_validate(item) for item in historical_data]
