import pytest
from httpx import AsyncClient

from app.crud.crud_stock import MOCK_SYMBOLS # Import the source of truth


async def test_get_symbols_success(async_client: AsyncClient):
    """Test retrieving the list of available symbols."""
    response = await async_client.get("/api/v1/symbols/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check if the returned symbols match the defined MOCK_SYMBOLS
    assert sorted(data) == sorted(MOCK_SYMBOLS)
    assert len(data) == len(MOCK_SYMBOLS)


# --- Tests for /quotes/{symbol} ---

async def test_get_quote_success(async_client: AsyncClient):
    """Test retrieving a quote for a valid symbol."""
    symbol = MOCK_SYMBOLS[0] # Use the first mock symbol
    response = await async_client.get(f"/api/v1/quotes/{symbol}")

    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == symbol
    assert "price" in data
    assert isinstance(data["price"], float)
    assert "timestamp" in data
    # Could add more specific checks on timestamp format if needed

async def test_get_quote_not_found(async_client: AsyncClient):
    """Test retrieving a quote for an invalid symbol."""
    symbol = "INVALID"
    response = await async_client.get(f"/api/v1/quotes/{symbol}")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert symbol in data["detail"]


# --- Tests for /historical/{symbol} ---

async def test_get_historical_success_default_dates(async_client: AsyncClient):
    """Test retrieving historical data for a valid symbol with default dates."""
    symbol = MOCK_SYMBOLS[1] # Use a different mock symbol
    response = await async_client.get(f"/api/v1/historical/{symbol}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Since we seeded 10 days, the default (30 days back) should return those 10 days
    assert len(data) > 0 # Check that some data is returned
    assert len(data) <= 10 # Should not exceed seeded data
    if data:
        item = data[0]
        assert item["symbol"] == symbol
        assert "date" in item
        assert "open" in item
        assert "high" in item
        assert "low" in item
        assert "close" in item
        assert "volume" in item

async def test_get_historical_success_specific_dates(async_client: AsyncClient):
    """Test retrieving historical data for a valid symbol with specific dates."""
    symbol = MOCK_SYMBOLS[2]
    # Assuming seeding put data for the last 10 days
    # Request data for a smaller range within that period
    from datetime import date, timedelta
    today = date.today()
    start_date = today - timedelta(days=5)
    end_date = today - timedelta(days=1)

    response = await async_client.get(
        f"/api/v1/historical/{symbol}",
        params={"start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Expecting data for end_date - start_date + 1 days = 5 days
    assert len(data) == 5
    if data:
        assert data[0]["symbol"] == symbol
        assert data[0]["date"] == start_date.isoformat()
        assert data[-1]["date"] == end_date.isoformat()

async def test_get_historical_not_found(async_client: AsyncClient):
    """Test retrieving historical data for an invalid symbol."""
    symbol = "INVALID"
    response = await async_client.get(f"/api/v1/historical/{symbol}")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert symbol in data["detail"]

async def test_get_historical_invalid_date_range(async_client: AsyncClient):
    """Test retrieving historical data with start_date after end_date."""
    symbol = MOCK_SYMBOLS[0]
    from datetime import date, timedelta
    today = date.today()
    start_date = today
    end_date = today - timedelta(days=1) # End date is before start date

    response = await async_client.get(
        f"/api/v1/historical/{symbol}",
        params={"start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
    )

    assert response.status_code == 422 # Validation error for date range
    data = response.json()
    assert "detail" in data
    # The specific detail message might vary slightly based on FastAPI version/Pydantic
    assert "Start date cannot be after end date" in data["detail"]

async def test_get_historical_invalid_date_format(async_client: AsyncClient):
    """Test retrieving historical data with an invalid date format."""
    symbol = MOCK_SYMBOLS[0]
    response = await async_client.get(
        f"/api/v1/historical/{symbol}",
        params={"start_date": "2023-13-01"} # Invalid month
    )
    assert response.status_code == 422 # Validation error from Pydantic/FastAPI
    # Check for detail message indicating validation error
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list) # FastAPI validation errors are lists
    assert "Input should be a valid date" in str(data["detail"]) # Check for relevant error message
