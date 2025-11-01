# Docker Setup for NSE Utility Reports

## Overview

This document explains the Docker setup for the NSE Utility Reports application.

## Project Analysis

### Application Type

-   **Framework**: Streamlit web application
-   **Purpose**: NSE (National Stock Exchange) utility reports and data visualization
-   **Main Language**: Python 3.10+

### Key Features

1. Index details and analysis
2. Pre-market information
3. FII & DII trading data
4. Participant-wise open interest (Long/Short ratio)
5. Advances/Declines analysis
6. Top gainers/losers
7. Most active equities
8. Large deals tracking
9. Index dividend yield
10. Index PE & PB ratios
11. Corporate actions and announcements
12. Insider trading data
13. Upcoming results calendar
14. NSE holidays
15. ETF and Mutual Fund data

### Technology Stack

-   **Python**: 3.10+
-   **Web Framework**: Streamlit 1.47.0+
-   **Data Manipulation**: Pandas 2.3.1+
-   **Data Visualization**: Matplotlib 3.10.5+
-   **Financial Data**: mftool 2.9+
-   **Package Manager**: uv

### Project Structure

```
nse_utility_reports/
├── main.py              # Main Streamlit application entry point
├── pages/               # Individual Streamlit pages
│   ├── index.py        # Home page
│   ├── index_details.py
│   ├── pre_market_info.py
│   ├── fii_dii_data.py
│   └── ... (15 more pages)
├── utils/               # Utility modules
│   └── NseUtility.py   # NSE API interaction utilities
├── pyproject.toml       # Python project configuration
└── uv.lock             # Dependency lock file
```

## Docker Implementation

### Files Created

1. **Dockerfile**

    - Base: Python 3.10-slim (lightweight)
    - Uses `uv` for fast package management
    - Exposes port 8501 (Streamlit default)
    - Includes health check
    - Runs application in production-ready mode

2. **docker-compose.yml**

    - Simple, single-service configuration
    - Port mapping: 8501:8501
    - Health check included
    - Auto-restart on failure
    - Environment variables configured

3. **.dockerignore**

    - Excludes unnecessary files from Docker build
    - Reduces build context size
    - Improves build speed

4. **DOCKER_SETUP.md**
    - This documentation file

### Key Docker Features

#### Efficiency

-   Uses Python 3.10-slim base image (minimal size)
-   Leverages `uv` for faster package installation
-   Multi-stage approach not needed (simple app)

#### Security

-   Runs as non-root user (best practice)
-   Minimal attack surface with slim image
-   Health checks for monitoring

#### Production Ready

-   Health checks configured
-   Auto-restart policy
-   Proper logging
-   Environment variable configuration

## Usage Instructions

### Prerequisites

-   Docker installed on your system
-   Docker Compose (optional, for easier management)

### Quick Start with Docker Compose

```bash
# Build and start the application
docker-compose up --build

# Start in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Using Docker Directly

```bash
# Build the image
docker build -t nse-utility-reports .

# Run the container
docker run -p 8501:8501 nse-utility-reports

# Run in detached mode with name
docker run -d -p 8501:8501 --name nse-reports nse-utility-reports

# View logs
docker logs -f nse-reports

# Stop the container
docker stop nse-reports

# Remove the container
docker rm nse-reports
```

## Access the Application

Once running, access the application at:

```
http://localhost:8501
```

## Configuration

### Environment Variables

You can customize the application using these environment variables:

-   `STREAMLIT_SERVER_PORT`: Server port (default: 8501)
-   `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)
-   `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: Disable usage stats (default: false)
-   `STREAMLIT_SERVER_HEADLESS`: Run without browser (default: true)

### Customizing Port

To use a different port:

**Docker Compose:**

```yaml
ports:
    - '8080:8501' # Map host port 8080 to container port 8501
```

**Docker:**

```bash
docker run -p 8080:8501 nse-utility-reports
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs nse-reports

# Check container status
docker ps -a
```

### Port already in use

```bash
# Find what's using port 8501
# Windows: netstat -ano | findstr :8501
# Linux/Mac: lsof -i :8501

# Use a different port in docker-compose.yml or use -p flag
```

### Build issues

```bash
# Clean build without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build --no-cache -t nse-utility-reports .
```

## Production Deployment

For production deployment, consider:

1. **Reverse Proxy**: Use Nginx or Traefik in front of the container
2. **HTTPS**: Configure SSL/TLS certificates
3. **Resource Limits**: Add resource constraints to docker-compose.yml
4. **Volume Mounts**: Mount volumes for data persistence if needed
5. **Monitoring**: Add monitoring and logging tools

Example production docker-compose.yml addition:

```yaml
services:
    nse-reports:
        # ... existing config ...
        deploy:
            resources:
                limits:
                    cpus: '1'
                    memory: 2G
                reservations:
                    cpus: '0.5'
                    memory: 1G
```

## Benefits of Dockerization

1. **Consistency**: Same environment across development, staging, and production
2. **Isolation**: Application dependencies don't conflict with system packages
3. **Portability**: Run anywhere Docker is supported
4. **Scalability**: Easy to scale horizontally
5. **Deployment**: Simplified CI/CD integration
6. **Rollback**: Easy to revert to previous versions

## Next Steps

1. Test the Docker setup locally
2. Configure your CI/CD pipeline to build and deploy
3. Set up monitoring and logging
4. Consider multi-container setup for database/external services if needed
5. Add SSL/TLS for production

## Support

For issues or questions:

-   Check the main [README.md](README.md)
-   Review Docker logs: `docker logs nse-reports`
-   Check Docker Compose logs: `docker-compose logs`
