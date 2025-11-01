# NSE Utility Reports

This tool is to get publicly available data on NSE india website

> ⚠️**Disclaimer** : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.

##### This Tool provide the following data's:

-   🗒️Index Data
-   📈Pre Market Data
-   📅FII and DII Data
-   ✏️F&O - Participant wise Open Interest (Long/Short) ratio
-   📈Advances/Declines
-   📉Top 20 Gainers/ Losers
-   📊Most Active Equities
-   🤝Large Deals
-   💰Index Dividend Yield
-   📈Index PE & PB Ratio
-   🎬Corporate Actions
-   📻Corporate Announcements
-   🗓️Upcoming Results
-   🪂Holidays
-   💶ETF's Data

## 📋 Prerequisites

-   [UV](https://docs.astral.sh/uv/getting-started/installation/) Python package and project manager
-   Python 3.10 or higher

## 🛠️ Installation

1. **Clone this repository:**

    ```bash
    $ git clone https://github.com/thisismegopi/nse_utility_reports.git
    $ cd nse_utility_reports
    ```

2. **Install dependencies using uv:**

    ```bash
    $ uv sync
    ```

## 🎮 Usage

### Local Development

```bash
$ uv run streamlit run main.py
```

### Using Docker

#### Option 1: Using Docker Compose (Recommended)

```bash
# Build and run the application
$ docker-compose up --build

# Run in detached mode
$ docker-compose up -d

# Stop the application
$ docker-compose down
```

The application will be available at `http://localhost:8501`

#### Option 2: Using Docker directly

```bash
# Build the Docker image
$ docker build -t nse-utility-reports .

# Run the container
$ docker run -p 8501:8501 nse-utility-reports

# Run in detached mode
$ docker run -d -p 8501:8501 --name nse-reports nse-utility-reports

# Stop the container
$ docker stop nse-reports
```

The application will be available at `http://localhost:8501`

## 🐳 Docker Details

-   **Base Image**: Python 3.10-slim
-   **Port**: 8501
-   **Package Manager**: uv (faster Python package management)
-   **Health Check**: Included for monitoring

Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).
