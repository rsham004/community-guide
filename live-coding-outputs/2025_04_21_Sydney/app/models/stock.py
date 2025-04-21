from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Optional
from datetime import datetime, date

# Shared properties for Quote
class QuoteBase(SQLModel):
    symbol: str = Field(index=True)
    price: float
    timestamp: datetime

# Database model for Quote (if we were storing them persistently)
# Although we generate mock data, defining this helps structure
class Quote(QuoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Pydantic model for reading/returning Quote data via API
class QuoteRead(QuoteBase):
    pass # Inherits all fields from QuoteBase


# Shared properties for HistoricalPrice
class HistoricalPriceBase(SQLModel):
    symbol: str = Field(index=True)
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

# Database model for HistoricalPrice (if we were storing them persistently)
class HistoricalPrice(HistoricalPriceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Ensure that for a given symbol, each date has only one entry
    __table_args__ = (UniqueConstraint("symbol", "date", name="uq_symbol_date"),)

# Pydantic model for reading/returning HistoricalPrice data via API
class HistoricalPriceRead(HistoricalPriceBase):
    pass # Inherits all fields from HistoricalPriceBase
