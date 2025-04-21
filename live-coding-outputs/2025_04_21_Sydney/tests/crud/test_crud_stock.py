import pytest
from datetime import date, timedelta
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud import crud_stock
from app.models.stock import HistoricalPrice, QuoteRead, HistoricalPriceRead
from app.crud.crud_stock import MOCK_SYMBOLS


# Note: The `seed_test_db_data` fixture from conftest.py runs automatically
# before each test function, ensuring the test DB is seeded with 10 days of data.

async def test_get_available_symbols():
    """Test the static symbol list retrieval."""
    symbols = crud_stock.get_available_symbols()
    assert symbols == MOCK_SYMBOLS

async def test_seed_initial_data_runs_once(session: AsyncSession):
    """
    Test that seeding logic correctly identifies existing data and skips reseeding.
    The `seed_test_db_data` fixture already ran once. We call it again manually
    to check the skipping logic.
    """
    # Check initial count (should be 10 days * num_symbols)
    statement = select(HistoricalPrice)
    results = await session.exec(statement)
    initial_count = len(results.all())
    assert initial_count == 10 * len(MOCK_SYMBOLS)

    # Call seeding again - it should detect existing data and not add more
    await crud_stock.seed_initial_data(session, num_days=5) # Use different num_days

    # Verify count hasn't changed
    statement_after = select(HistoricalPrice)
    results_after = await session.exec(statement_after)
    final_count = len(results_after.all())
    assert final_count == initial_count

async def test_get_mock_quote_success(session: AsyncSession):
    """Test retrieving the latest quote (historical data point) for a valid symbol."""
    symbol = MOCK_SYMBOLS[0]
    quote = await crud_stock.get_mock_quote(session, symbol)

    assert quote is not None
    assert isinstance(quote, QuoteRead)
    assert quote.symbol == symbol
    assert isinstance(quote.price, float)
    assert quote.price > 0
    # Check if timestamp corresponds to the latest date seeded (today)
    assert quote.timestamp.date() == date.today()

async def test_get_mock_quote_invalid_symbol(session: AsyncSession):
    """Test retrieving a quote for an invalid symbol."""
    quote = await crud_stock.get_mock_quote(session, "INVALID")
    assert quote is None

async def test_get_mock_historical_data_success(session: AsyncSession):
    """Test retrieving historical data for a valid symbol and date range."""
    symbol = MOCK_SYMBOLS[1]
    today = date.today()
    start_date = today - timedelta(days=5)
    end_date = today - timedelta(days=1)

    data = await crud_stock.get_mock_historical_data(session, symbol, start_date, end_date)

    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 5 # Should match the date range requested (within seeded data)
    for item in data:
        assert isinstance(item, HistoricalPriceRead)
        assert item.symbol == symbol
        assert start_date <= item.date <= end_date

async def test_get_mock_historical_data_full_range(session: AsyncSession):
    """Test retrieving the full seeded date range."""
    symbol = MOCK_SYMBOLS[2]
    today = date.today()
    start_date = today - timedelta(days=9) # Seeded 10 days total (0-9 days ago)
    end_date = today

    data = await crud_stock.get_mock_historical_data(session, symbol, start_date, end_date)

    assert data is not None
    assert len(data) == 10 # Should retrieve all seeded data points

async def test_get_mock_historical_data_invalid_symbol(session: AsyncSession):
    """Test retrieving historical data for an invalid symbol."""
    today = date.today()
    start_date = today - timedelta(days=5)
    end_date = today
    data = await crud_stock.get_mock_historical_data(session, "INVALID", start_date, end_date)
    assert data is None

async def test_get_mock_historical_data_date_range_no_data(session: AsyncSession):
    """Test retrieving historical data for a date range outside seeded data."""
    symbol = MOCK_SYMBOLS[0]
    today = date.today()
    # Request dates far in the past, before seeded data
    start_date = today - timedelta(days=100)
    end_date = today - timedelta(days=90)

    data = await crud_stock.get_mock_historical_data(session, symbol, start_date, end_date)

    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 0 # Expect empty list as range is outside seeded data
