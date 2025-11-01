# NSE Utility Reports - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [Features & Pages](#features--pages)
7. [API Reference](#api-reference)
8. [Data Retrieval Details](#data-retrieval-details)
9. [Deployment](#deployment)
10. [Operational Considerations](#operational-considerations)
11. [Extension Ideas](#extension-ideas)

---

## Project Overview

**NSE Utility Reports** is a Streamlit-based web application that aggregates publicly available market data from the National Stock Exchange (NSE) of India. The tool provides a user-friendly interface to access various market metrics, corporate actions, derivatives data, and financial information through an organized multi-page dashboard.

### Key Characteristics

- **Frontend Framework**: Streamlit (Python-based web framework)
- **Data Source**: NSE India public APIs and data archives
- **Package Manager**: UV (fast Python package management)
- **Containerization**: Docker support with Docker Compose
- **Purpose**: Educational and analytical tool for accessing NSE market data

### Important Disclaimer

⚠️ **This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.**

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit Application                    │
│                         (main.py)                            │
├─────────────────────────────────────────────────────────────┤
│                    Navigation System                         │
│              (18 Pages via st.navigation)                    │
├──────────────────────┬──────────────────────────────────────┤
│   UI Layer (Pages)   │     Data Layer (Utils)               │
│                      │                                       │
│  - index.py          │  - NseUtility.py                     │
│  - index_details.py  │    └─ NseUtils class                 │
│  - pre_market_info.py│       ├─ Session Management          │
│  - fii_dii_data.py   │       ├─ API Methods                 │
│  - ... (15 more)     │       └─ Data Processing             │
└──────────────────────┴───────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   NSE India API  │
                    │  (nseindia.com)  │
                    └──────────────────┘
```

### Component Relationships

1. **Entry Point (`main.py`)**: Configures Streamlit and sets up page navigation
2. **Utility Module (`utils/NseUtility.py`)**: Core data fetching and processing logic
3. **Page Modules (`pages/*.py`)**: UI components that consume utility functions
4. **External Services**: NSE India APIs, AMFI (for mutual funds)

### Design Patterns

- **Single Responsibility**: Each page handles one specific data view
- **Session Management**: Reuses HTTP sessions for NSE API calls to maintain cookies
- **Data Transformation**: Raw API responses → Filtered dictionaries → Pandas DataFrames
- **Error Handling**: Try-except blocks with user-friendly error messages

---

## Installation & Setup

### Prerequisites

- **UV Package Manager**: [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Python**: Version 3.10 or higher
- **Docker** (optional): For containerized deployment

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thisismegopi/nse_utility_reports.git
   cd nse_utility_reports
   ```

2. **Install dependencies using UV**:
   ```bash
   uv sync
   ```

3. **Run the application**:
   ```bash
   uv run streamlit run main.py
   ```

4. **Access the application**:
   - Open your browser and navigate to `http://localhost:8501`

### Docker Setup

#### Option 1: Docker Compose (Recommended)

```bash
# Build and run the application
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the application
docker-compose down
```

#### Option 2: Docker Directly

```bash
# Build the Docker image
docker build -t nse-utility-reports .

# Run the container
docker run -p 8501:8501 nse-utility-reports

# Run in detached mode
docker run -d -p 8501:8501 --name nse-reports nse-utility-reports

# Stop the container
docker stop nse-reports
```

### Docker Configuration Details

- **Base Image**: Python 3.10-slim
- **Exposed Port**: 8501
- **Package Manager**: UV (faster Python package management)
- **Health Check**: Included for monitoring

---

## Project Structure

```
nse_utility_reports/
├── main.py                          # Application entry point
├── README.md                        # Basic project information
├── DOCUMENTATION.md                 # This file
├── pyproject.toml                   # Project dependencies (UV)
├── uv.lock                         # Dependency lock file
├── Dockerfile                      # Docker container configuration
├── docker-compose.yml              # Docker Compose configuration
├── DOCKER_SETUP.md                 # Docker setup instructions
│
├── pages/                           # Streamlit page modules
│   ├── index.py                    # Home/Landing page
│   ├── index_details.py            # Index constituents view
│   ├── pre_market_info.py          # Pre-market data
│   ├── fii_dii_data.py             # FII & DII activity
│   ├── long_short_ratio.py         # F&O participant OI ratios
│   ├── advance_decline.py           # Market breadth (A/D)
│   ├── gainers_losers.py           # Top gainers/losers
│   ├── most_active_equity.py        # Most active stocks/ETFs
│   ├── large_deals.py              # Bulk/Block/Short deals
│   ├── index_div_yield.py          # Index dividend yields
│   ├── index_pe_pb_ratio.py        # PE & PB ratios
│   ├── corporate_action.py         # Corporate actions search
│   ├── corporate_announcement.py    # Corporate announcements
│   ├── corporate_filings_insider_trading.py  # Insider trading
│   ├── upcoming_results_calendar.py # Results calendar
│   ├── holidays.py                 # Trading/Clearing holidays
│   ├── etf.py                      # ETF listings
│   └── mutual_fund.py              # Mutual fund explorer
│
└── utils/                          # Utility modules
    ├── __init__.py
    └── NseUtility.py               # Core NSE API wrapper class
```

---

## Core Components

### 1. Main Application (`main.py`)

**Purpose**: Entry point that configures Streamlit and sets up multi-page navigation.

**Key Functions**:
- `main()`: Sets up page navigation using `st.navigation()` with 18 pages

**Code Structure**:
```python
def main():
    st.set_page_config(layout="wide")
    pg = st.navigation([
        st.Page("./pages/index.py", title="Home", icon="🏠"),
        st.Page("./pages/index_details.py", title="Index Details", icon="🗒️"),
        # ... 16 more pages
    ])
    pg.run()
```

### 2. NSE Utility Class (`utils/NseUtility.py`)

**Purpose**: Core data fetching engine that wraps NSE India APIs.

**Class**: `NseUtils`

#### Initialization

The `__init__` method sets up:
- HTTP headers mimicking a browser request
- A persistent `requests.Session` object
- Initial cookie retrieval from NSE website

```python
def __init__(self):
    self.headers = {
        "User-Agent": "Mozilla/5.0 ...",
        "Accept": "text/html,application/xhtml+xml,...",
        # ... other headers
    }
    self.session = requests.Session()
    self.session.get("http://nseindia.com", headers=self.headers)
    self.cookies = self.session.cookies.get_dict()
```

#### Available Index Lists

**Equity Market Indices** (`equity_market_list`):
- Contains 47+ index names including:
  - Major indices: NIFTY 50, NIFTY NEXT 50, NIFTY BANK
  - Sectoral indices: NIFTY IT, NIFTY PHARMA, NIFTY FMCG, etc.
  - Strategy indices: NIFTY 50 EQUAL WEIGHT, NIFTY ALPHA 50, etc.

**Pre-Market Categories** (`pre_market_list`):
- NIFTY 50, Nifty Bank, Emerge, Securities in F&O, Others, All

---

## Features & Pages

### Home Page (`pages/index.py`)

**Purpose**: Landing page with project overview and disclaimer.

**Features**:
- Project introduction
- Feature list with icons
- Disclaimer notice
- GitHub link

### Index Details (`pages/index_details.py`)

**Purpose**: View constituent stocks of selected indices with detailed price statistics.

**User Inputs**:
- Index selection dropdown (from `equity_market_list`)

**Data Displayed**:
- Symbol, Priority, Open, High, Low, Last Price
- Previous Close, Change, % Change
- Market Cap, 52W High/Low
- Volume, Value traded
- 30-day and 365-day percentage changes

**API Method**: `get_index_details(category)`

### Pre Market Info (`pages/pre_market_info.py`)

**Purpose**: View pre-market trading data with advance/decline metrics.

**User Inputs**:
- Category selection (NIFTY 50, Nifty Bank, Emerge, etc.)

**Data Displayed**:
- Advance/Decline/Unchanged counts (metrics)
- Symbol-wise data table with:
  - Previous Close, IEP, Change, % Change
  - Last Price, Final Quantity, Turnover
  - Market Cap, 52W High/Low
  - Today's chart path

**API Method**: `pre_market_info(category)`

**Special Features**: Color-coded rows (green for positive, red for negative changes)

### FII & DII Data (`pages/fii_dii_data.py`)

**Purpose**: Display Foreign Institutional Investors (FII) and Domestic Institutional Investors (DII) trading activity.

**Data Displayed**:
- Category (FII/DII)
- Date
- Buy Value, Sell Value, Net Value

**API Method**: `fii_dii_activity()`

### F&O Participant OI (`pages/long_short_ratio.py`)

**Purpose**: View Futures & Options participant-wise Open Interest (Long/Short) ratios.

**User Inputs**:
- Date picker (select trading date)

**Data Displayed**:
- Four participant categories: FII, DII, Client, Pro
- For each participant:
  - Future Index Long/Short ratios
  - Future Stock Long/Short ratios

**Data Source**: Direct CSV download from NSE archives
- URL format: `https://archives.nseindia.com/content/nsccl/fao_participant_oi_{DDMMYYYY}.csv`

**Calculation**:
```python
long_ratio = (long / (long + short)) * 100
short_ratio = (short / (long + short)) * 100
```

### Advances/Declines (`pages/advance_decline.py`)

**Purpose**: Market breadth indicator showing advancing vs declining stocks per index.

**Data Displayed**:
- Index name
- Advances count
- Declines count
- Unchanged count

**API Method**: `get_advance_decline()`

### Top Gainers/Losers (`pages/gainers_losers.py`)

**Purpose**: View top performing and worst performing stocks.

**User Inputs**:
- Index selection (NIFTY 50, BANK NIFTY, NIFTY NEXT 50, F&O Securities, All Securities)

**Data Displayed**:
- Two tabs: "Gainers" and "Losers"
- For each stock:
  - Symbol, Open/High/Low prices
  - LTP, Previous Price
  - % Change, Volume, Turnover

**API Method**: `get_gainers_losers_v2(index)` where index = "gainers" or "loosers"

### Most Active Equities (`pages/most_active_equity.py`)

**Purpose**: View most actively traded stocks and ETFs.

**Data Displayed**:
- Four tabs:
  1. Stocks by Volume
  2. Stocks by Value
  3. ETFs by Volume
  4. ETFs by Value

**For Stocks**:
- Symbol, OHLC prices, Change, % Change
- Volume (shares), Value (₹ Lakhs)
- 52W High/Low, Last Update Time

**For ETFs**:
- Similar to stocks, plus NAV (Net Asset Value)

**API Methods**:
- `most_active_equity_stocks(index_str)` where index_str = "volume" or "value"
- `most_active_equity_etf(index_str)` where index_str = "volume" or "value"

### Large Deals (`pages/large_deals.py`)

**Purpose**: View bulk deals, block deals, and short selling data.

**Data Displayed**:
- Three tabs: Bulk Deals, Block Deals, Short Selling
- For each deal:
  - Date, Symbol, Name
  - Client Name
  - Buy/Sell indicator
  - Quantity Traded
  - Weighted Average Trade Price (WATP)

**API Method**: `large_deals(deal_str)` where deal_str = "BULK_DEALS_DATA", "BLOCK_DEALS_DATA", or "SHORT_DEALS_DATA"

### Index Dividend Yield (`pages/index_div_yield.py`)

**Purpose**: View dividend yield percentages for various indices.

**Data Displayed**:
- Index name, Type, Dividend Yield

**API Method**: `get_index_div_yield()`

### Index PE & PB Ratio (`pages/index_pe_pb_ratio.py`)

**Purpose**: View Price-to-Earnings (PE) and Price-to-Book (PB) ratios for indices.

**Data Displayed**:
- Two sections:
  1. PE Ratio: Index, Type, Profit Earning Ratio
  2. PB Ratio: Index, Type, Price Book Ratio

**API Methods**:
- `get_index_pe_ratio()`
- `get_index_pb_ratio()`

### Corporate Actions (`pages/corporate_action.py`)

**Purpose**: Search and view corporate actions (dividends, splits, bonuses, etc.).

**User Inputs**:
- Symbol (optional text input)
- From Date (date picker)
- To Date (date picker)

**Data Displayed**:
- Symbol, Series, Face Value
- Subject (action description)
- Ex Date, Record Date
- ISIN, Company name

**API Method**: `get_corporate_action(symbol, from_date_str, to_date_str, filter)`

**Default Range**: Last 30 days if dates not specified

### Corporate Announcements (`pages/corporate_announcement.py`)

**Purpose**: View corporate filings and announcements with attachments.

**User Inputs**:
- Symbol (optional text input)
- From Date (default: 30 days ago)
- To Date (default: today)

**Data Displayed**:
- Symbol, Company Name
- Subject/Description
- Attachment link (clickable)
- Attachment text/details
- Date and Time of announcement

**API Method**: `get_corporate_announcement(symbol, from_date_str, to_date_str)`

### Corporate Filings - Insider Trading (`pages/corporate_filings_insider_trading.py`)

**Purpose**: View insider trading disclosures.

**User Inputs**:
- Symbol (optional text input)

**Data Displayed**:
- Symbol, Company, Acquirer/Disposer name
- Broadcast Date/Time
- Acquisition Mode, Person Category
- Security Type, Quantity Acquired/Disposed
- Transaction Type (Buy/Sell - color coded)
- Before/After acquisition shares (count and percentage)
- Securities value, Intimation Date

**API Method**: `get_corporate_filings_insider_trading(symbol)`

**Special Features**: Row coloring (green for Buy, red for Sell)

### Upcoming Results Calendar (`pages/upcoming_results_calendar.py`)

**Purpose**: View scheduled financial results announcements.

**User Inputs**:
- Symbol (optional text input)
- From Date (default: today)
- To Date (default: 30 days ahead)

**Data Displayed**:
- Symbol, Company
- Purpose, Description
- Date (scheduled announcement date)

**API Method**: `get_upcoming_results_calendar(symbol, from_date_str, to_date_str)`

**Filter**: Only shows events where description contains "Results"

### Holidays (`pages/holidays.py`)

**Purpose**: View NSE trading and clearing holidays calendar.

**Data Displayed**:
- Two tabs: Trading Holidays, Clearing Holidays
- For each holiday:
  - Date, Week day
  - Description
  - Morning/Evening session details

**API Methods**:
- `trading_holidays()`
- `clearing_holidays()`

### ETF's (`pages/etf.py`)

**Purpose**: Browse Exchange Traded Funds with search capability.

**User Inputs**:
- Search text (optional - filters by underlying asset name)
- Toggle for row color highlighting

**Data Displayed**:
- Symbol, Underlying Asset
- OHLC prices, LTP, Change, % Change
- Volume, Value (₹ Crores)
- NAV, 52W High/Low
- 30-day and 365-day percentage changes

**API Method**: `get_etf_list(search_text)`

### Mutual Funds (`pages/mutual_fund.py`)

**Purpose**: Explore AMFI (Association of Mutual Funds in India) mutual fund schemes.

**User Inputs**:
- Fund selection dropdown
- Balance units input (for market value calculation)

**Data Displayed**:
- **Scheme Details**:
  - Fund House, Scheme Type/Category
  - Scheme Code, Name
  - Start Date, NAV at Start Date
- **Scheme Quote**:
  - Scheme Code, Name
  - Last Updated, Current NAV
- **Market Value Calculator**:
  - Balance Units input
  - Calculated Market Value

**Data Source**: `mftool` library (third-party AMFI data wrapper)

**Note**: This page doesn't use `NseUtils` class; it directly uses `Mftool` from the `mftool` package.

---

## API Reference

### NseUtils Class Methods

#### Market Data Methods

##### `pre_market_info(category="All")`
- **Purpose**: Get pre-market trading information
- **Parameters**: 
  - `category` (str): "NIFTY 50", "Nifty Bank", "Emerge", "Securities in F&O", "Others", "All"
- **Returns**: Dictionary with keys:
  - `data_frame`: DataFrame with symbol-wise pre-market data
  - `advance_decline`: Dict with "advance", "decline", "unchanged" counts

##### `get_index_details(category)`
- **Purpose**: Get constituent stocks and statistics for an index
- **Parameters**: 
  - `category` (str): Index name (from `equity_market_list`)
- **Returns**: DataFrame with index constituents data

##### `get_advance_decline()`
- **Purpose**: Get advances/declines statistics per index
- **Returns**: DataFrame with columns: Index, Advances, Declines, Unchanged

##### `get_gainers_losers_v2(index)`
- **Purpose**: Get top gainers or losers data
- **Parameters**: 
  - `index` (str): "gainers" or "loosers"
- **Returns**: Dictionary with nested data by index category (NIFTY, BANKNIFTY, etc.)

##### `most_active_equity_stocks(index_str)`
- **Purpose**: Get most actively traded stocks
- **Parameters**: 
  - `index_str` (str): "volume" or "value"
- **Returns**: DataFrame with most active stocks

##### `most_active_equity_etf(index_str)`
- **Purpose**: Get most actively traded ETFs
- **Parameters**: 
  - `index_str` (str): "volume" or "value"
- **Returns**: DataFrame with most active ETFs

##### `large_deals(deal_str)`
- **Purpose**: Get large deals data (bulk, block, or short selling)
- **Parameters**: 
  - `deal_str` (str): "BULK_DEALS_DATA", "BLOCK_DEALS_DATA", or "SHORT_DEALS_DATA"
- **Returns**: DataFrame with large deals information

#### Index Analysis Methods

##### `get_index_pe_ratio()`
- **Purpose**: Get Price-to-Earnings ratios for indices
- **Returns**: DataFrame with columns: Index, Type, Profit Earning Ratio

##### `get_index_pb_ratio()`
- **Purpose**: Get Price-to-Book ratios for indices
- **Returns**: DataFrame with columns: Index, Type, Price Book Ratio

##### `get_index_div_yield()`
- **Purpose**: Get dividend yield percentages for indices
- **Returns**: DataFrame with columns: Index, Type, Div Yield

#### Corporate Data Methods

##### `get_corporate_action(symbol=None, from_date_str=None, to_date_str=None, filter=None)`
- **Purpose**: Get corporate actions (dividends, splits, bonuses, etc.)
- **Parameters**: 
  - `symbol` (str, optional): Stock symbol to filter
  - `from_date_str` (str, optional): Start date in "DD-MM-YYYY" format (default: 30 days ago)
  - `to_date_str` (str, optional): End date in "DD-MM-YYYY" format (default: today)
  - `filter` (str, optional): Text filter for action purpose
- **Returns**: DataFrame with corporate actions, or None if no data

##### `get_corporate_announcement(symbol=None, from_date_str=None, to_date_str=None)`
- **Purpose**: Get corporate announcements and filings
- **Parameters**: Same as `get_corporate_action`
- **Returns**: DataFrame with announcements, or None if no data

##### `get_corporate_filings_insider_trading(symbol=None)`
- **Purpose**: Get insider trading disclosures
- **Parameters**: 
  - `symbol` (str, optional): Stock symbol to filter
- **Returns**: DataFrame with insider trading data, or None if no data

##### `get_upcoming_results_calendar(symbol=None, from_date_str=None, to_date_str=None)`
- **Purpose**: Get scheduled financial results announcements
- **Parameters**: Same as `get_corporate_action`
- **Returns**: DataFrame with results calendar, or None if no data

#### Institutional Data Methods

##### `fii_dii_activity()`
- **Purpose**: Get FII and DII trading activity
- **Returns**: DataFrame with columns: category, date, buyValue, sellValue, netValue

#### Derivatives Methods

##### `get_option_chain(symbol, indices=False)`
- **Purpose**: Get full option chain for a symbol
- **Parameters**: 
  - `symbol` (str): Stock or index symbol
  - `indices` (bool): True if symbol is an index
- **Returns**: DataFrame with option chain data

##### `get_live_option_chain(symbol, expiry_date=None, oi_mode="full", indices=False)`
- **Purpose**: Get live option chain with optional expiry filter
- **Parameters**: 
  - `symbol` (str): Stock or index symbol
  - `expiry_date` (str, optional): Expiry date in "DD-MM-YYYY" format
  - `oi_mode` (str): "full" or "compact"
  - `indices` (bool): True if symbol is an index
- **Returns**: DataFrame with live option chain data

##### `futures_data(symbol, indices=False)`
- **Purpose**: Get futures instruments for a symbol
- **Parameters**: Same as `get_option_chain`
- **Returns**: DataFrame with futures data

#### Reference Data Methods

##### `trading_holidays(list_only=False)`
- **Purpose**: Get NSE trading holidays
- **Parameters**: 
  - `list_only` (bool): If True, returns list of dates; else returns DataFrame
- **Returns**: DataFrame or list of holiday dates

##### `clearing_holidays(list_only=False)`
- **Purpose**: Get NSE clearing holidays
- **Parameters**: Same as `trading_holidays`
- **Returns**: DataFrame or list of holiday dates

##### `is_nse_trading_holiday(date_str=None)`
- **Purpose**: Check if a date is a trading holiday
- **Parameters**: 
  - `date_str` (str, optional): Date in "DD-MMM-YYYY" format (default: today)
- **Returns**: True if holiday, False otherwise

##### `is_nse_clearing_holiday(date_str=None)`
- **Purpose**: Check if a date is a clearing holiday
- **Parameters**: Same as `is_nse_trading_holiday`
- **Returns**: True if holiday, False otherwise

##### `get_equity_full_list(list_only=False)`
- **Purpose**: Get list of all equity stocks on NSE
- **Parameters**: 
  - `list_only` (bool): If True, returns list of symbols; else returns DataFrame
- **Returns**: DataFrame or list of equity symbols

##### `get_fno_full_list(list_only=False)`
- **Purpose**: Get list of all F&O securities
- **Parameters**: Same as `get_equity_full_list`
- **Returns**: DataFrame or list of F&O symbols

##### `get_etf_list(search_text=None)`
- **Purpose**: Get list of ETFs with optional search
- **Parameters**: 
  - `search_text` (str, optional): Filter by underlying asset name
- **Returns**: DataFrame with ETF data, or None if no matches

#### Historical Data Methods

##### `get_index_historic_data(index, from_date, to_date)`
- **Purpose**: Get historical index data for a date range
- **Parameters**: 
  - `index` (str): Index name
  - `from_date` (str): Start date in "DD-MM-YYYY" format
  - `to_date` (str): End date in "DD-MM-YYYY" format
- **Returns**: DataFrame with historical index data
- **Note**: Automatically handles ranges > 365 days by splitting into chunks

##### `bhav_copy_with_delivery(trade_date)`
- **Purpose**: Get daily bhav copy with delivery data
- **Parameters**: 
  - `trade_date` (str): Date in "DD-MM-YYYY" format
- **Returns**: DataFrame with bhav copy data

##### `equity_bhav_copy(trade_date)`
- **Purpose**: Get equity bhav copy for a date
- **Parameters**: Same as `bhav_copy_with_delivery`
- **Returns**: DataFrame with equity bhav copy

##### `fno_bhav_copy(trade_date)`
- **Purpose**: Get F&O bhav copy for a date
- **Parameters**: Same as `bhav_copy_with_delivery`
- **Returns**: DataFrame with F&O bhav copy

#### Individual Stock Methods

##### `equity_info(symbol)`
- **Purpose**: Get comprehensive information for a stock
- **Parameters**: 
  - `symbol` (str): Stock symbol
- **Returns**: Dictionary with equity information and trade data

##### `price_info(symbol)`
- **Purpose**: Get key price information for a stock
- **Parameters**: 
  - `symbol` (str): Stock symbol
- **Returns**: Dictionary with price metrics (LTP, Open, High, Low, VWAP, etc.)

##### `get_52week_high_low(stock=None)`
- **Purpose**: Get 52-week high/low data
- **Parameters**: 
  - `stock` (str, optional): Stock symbol (if None, returns all stocks)
- **Returns**: Dictionary with 52W high/low data or DataFrame for all stocks

##### `get_market_depth(symbol)`
- **Purpose**: Get market depth (order book) for a symbol
- **Parameters**: 
  - `symbol` (str): Stock symbol
- **Returns**: Dictionary with "ask" and "bid" order book data

---

## Data Retrieval Details

### NSE API Interaction Pattern

The application follows a consistent pattern for interacting with NSE APIs:

1. **Initial Session Setup**: 
   - Make a GET request to `http://nseindia.com` to obtain cookies
   - Store cookies in the session object

2. **Reference Page Visit**:
   - For many endpoints, first visit the corresponding NSE web page
   - Extract cookies from that page
   - Use these cookies for the actual API call

3. **API Call**:
   - Make GET request to NSE API endpoint with:
     - Appropriate headers (User-Agent, Accept, etc.)
     - Cookies from reference page
     - URL-encoded parameters

4. **Data Processing**:
   - Parse JSON response
   - Filter to extract only required fields
   - Convert to Pandas DataFrame
   - Return processed data

### Date Format Requirements

- **Input Format**: `DD-MM-YYYY` (e.g., "25-01-2024")
- **NSE Format**: Some APIs expect `DD-MMM-YYYY` (e.g., "25-Jan-2024")
- **Validation**: Basic validation with `datetime.strptime()`; errors raise `ValueError`

### Error Handling

- **403 Forbidden**: Often occurs due to missing/invalid cookies; handled by retry with reference page
- **404 Not Found**: Common for historical data; raises `FileNotFoundError`
- **Empty Data**: Methods return `None` or empty DataFrame
- **API Changes**: Unhandled exceptions propagate to UI; user sees generic error message

### Rate Limiting

- **No Built-in Rate Limiting**: Repeated navigation may trigger rate limits
- **Recommendation**: Implement request throttling or caching
- **NSE Behavior**: May block excessive requests; session reuse helps but not guaranteed

### Data Filtering Strategy

Most methods filter API responses to extract only essential fields:

```python
keys_to_extract = [
    "symbol",
    "previousClose",
    "iep",
    # ... other fields
]
filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in processed_data]
df = pd.DataFrame(filtered_data)
```

This reduces memory usage and improves performance for large datasets.

---

## Deployment

### Local Deployment

1. Install dependencies: `uv sync`
2. Run application: `uv run streamlit run main.py`
3. Access at `http://localhost:8501`

### Docker Deployment

#### Build and Run
```bash
docker-compose up --build
```

#### Production Considerations

1. **Environment Variables**: 
   - No secrets required (all data is public)
   - Consider adding `STREAMLIT_SERVER_PORT` if customizing port

2. **Resource Limits**:
   - Minimal CPU/memory requirements
   - Consider setting Docker resource limits for production

3. **Health Checks**:
   - Dockerfile includes health check
   - Monitor `/healthz` endpoint if added

4. **Logging**:
   - Streamlit logs to stdout/stderr
   - Configure log aggregation for production

### Cloud Deployment Options

- **Streamlit Cloud**: Direct GitHub integration
- **AWS/Azure/GCP**: Container-based deployment
- **Heroku/Railway**: Platform-as-a-Service options

---

## Operational Considerations

### Performance

#### Current Limitations

1. **No Caching**: Every page navigation triggers fresh API calls
2. **Synchronous Requests**: All API calls are blocking
3. **No Request Pooling**: Each `NseUtils` instance creates new session

#### Recommendations

1. **Implement Caching**:
   ```python
   @st.cache_data(ttl=300)  # Cache for 5 minutes
   def get_cached_data():
       return nse.get_index_details("NIFTY 50")
   ```

2. **Session Reuse**:
   ```python
   @st.cache_resource
   def get_nse_instance():
       return NseUtility.NseUtils()
   ```

3. **Background Refresh**: Use Streamlit's background processes for heavy data loads

### Error Handling

#### Current State

- Generic try-except blocks in most pages
- Error messages show "Unable to fetch data" or exception string
- No logging infrastructure

#### Improvements Needed

1. **Structured Logging**: Use Python's `logging` module
2. **User-Friendly Messages**: Replace technical errors with helpful guidance
3. **Retry Logic**: Implement exponential backoff for transient failures
4. **Error Tracking**: Log errors for debugging and monitoring

### Security

#### Current Security Posture

- ✅ No sensitive data stored
- ✅ All data sources are public
- ✅ No authentication required (by design)
- ⚠️ No input validation on user inputs
- ⚠️ No rate limiting protection

#### Recommendations

1. **Input Sanitization**: Validate symbol names, dates, etc.
2. **Rate Limiting**: Implement client-side throttling
3. **Error Information**: Avoid exposing internal error details

### Monitoring

#### Recommended Metrics

1. **API Response Times**: Track latency per endpoint
2. **Error Rates**: Monitor 403/404/500 responses
3. **Usage Patterns**: Track most used pages/features
4. **Data Freshness**: Alert if data becomes stale

### Known Issues

1. **`long_short_ratio.py`**: Potential undefined `response` variable if date not selected
2. **`mutual_fund.py`**: No error handling if AMFI service unavailable
3. **Missing Dependency**: `requests` library not in `pyproject.toml` (used heavily)
4. **Date Validation**: Limited validation on date inputs may cause unexpected errors

---

## Extension Ideas

### Immediate Improvements

1. **Add Missing Dependency**:
   ```toml
   dependencies = [
       "requests>=2.31.0",  # Add this
       # ... existing dependencies
   ]
   ```

2. **Fix `long_short_ratio.py` Bug**:
   ```python
   if date is not None:
       url = f"..."
       response = requests.get(url)
       if response.status_code == 200:
           # ... process data
   else:
       st.info("Please select a date to view data")
   ```

3. **Add Centralized Styling**:
   ```python
   # utils/styling.py
   def get_color_styles(df, change_column):
       # Reusable color coding function
   ```

### Feature Enhancements

1. **Data Export**:
   - Add CSV/Excel export buttons to all tables
   - Implement PDF report generation

2. **Charts and Visualization**:
   - Integrate Plotly or similar for interactive charts
   - Add price history graphs
   - Volume/price correlation charts

3. **Alerts and Notifications**:
   - Set price alerts for specific stocks
   - Email notifications for corporate actions
   - Watchlist functionality

4. **Advanced Analytics**:
   - Technical indicators (RSI, MACD, etc.)
   - Portfolio tracking
   - Performance benchmarking

5. **Historical Analysis**:
   - Compare multiple dates
   - Trend analysis over time periods
   - Sector/stock comparison tools

### Architecture Improvements

1. **Database Layer**:
   - Cache API responses in SQLite/PostgreSQL
   - Store historical data for analysis
   - Reduce API load

2. **API Layer**:
   - Create REST API wrapper for NSE data
   - Enable programmatic access
   - Support multiple frontends

3. **Testing Infrastructure**:
   - Unit tests for utility methods
   - Integration tests for API calls
   - UI component tests with Playwright

4. **Documentation**:
   - API documentation with examples
   - User guide with screenshots
   - Video tutorials

### Integration Ideas

1. **Third-Party Services**:
   - Real-time market data providers (Alpha Vantage, etc.)
   - News aggregation for corporate announcements
   - Social sentiment analysis

2. **Mobile App**:
   - React Native or Flutter app using same backend
   - Push notifications for alerts

3. **Browser Extension**:
   - Quick stock lookup
   - Price ticker
   - Portfolio tracker

---

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make changes following existing code style
4. Test thoroughly
5. Submit pull request

### Code Style

- Follow PEP 8 conventions
- Use descriptive variable names
- Add docstrings to functions
- Handle errors gracefully

### Testing

- Test with various date ranges
- Verify data accuracy against NSE website
- Check error handling with invalid inputs

---

## License & Credits

- **Author**: [Gopi](https://github.com/thisismegopi)
- **Repository**: [GitHub](https://github.com/thisismegopi/nse_utility_reports)
- **Disclaimer**: Educational purposes only. NSE data usage requires explicit approval.

---

## Changelog

### Version 0.1.0
- Initial release
- 18 feature pages
- Docker support
- UV package management

---

## Support & Contact

- **GitHub Issues**: Report bugs or request features
- **Pull Requests**: Welcome contributions
- **Documentation**: This file and README.md

---

**Last Updated**: January 2025

