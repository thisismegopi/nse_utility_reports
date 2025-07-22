"""
    * NSE UTILITY *

    Description: This utility is Python Library to get publicly available data on new NSE india website

    Disclaimer : This utility is meant for educational purposes only. Downloading data from NSE
    website requires explicit approval from the exchange. Hence, the usage of this utility is for
    limited purposes only under proper/explicit approvals.

    Requirements : Following packages are to be installed (using pip) prior to using this utility
    - pandas
    - python 3.8 and above

"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO, BytesIO
import zipfile


class NseUtils:
    equity_market_list = ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100',
                          'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100', 'NIFTY SMALLCAP 250',
                          'NIFTY MIDSMALLCAP 400', 'NIFTY 100', 'NIFTY 200', 'NIFTY AUTO',
                          'NIFTY BANK', 'NIFTY ENERGY', 'NIFTY FINANCIAL SERVICES', 'NIFTY FINANCIAL SERVICES 25/50',
                          'NIFTY FMCG',
                          'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY PHARMA', 'NIFTY PSU BANK', 'NIFTY REALTY',
                          'NIFTY PRIVATE BANK', 'Securities in F&O', 'Permitted to Trade',
                          'NIFTY DIVIDEND OPPORTUNITIES 50',
                          'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30', 'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT',
                          'NIFTY100 LOW VOLATILITY 30', 'NIFTY ALPHA 50', 'NIFTY200 QUALITY 30',
                          'NIFTY ALPHA LOW-VOLATILITY 30',
                          'NIFTY200 MOMENTUM 30', 'NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE',
                          'NIFTY INFRASTRUCTURE',
                          'NIFTY MNC', 'NIFTY GROWTH SECTORS 15', 'NIFTY PSE', 'NIFTY SERVICES SECTOR',
                          'NIFTY100 LIQUID 15',
                          'NIFTY MIDCAP LIQUID 15']
    pre_market_list = ['NIFTY 50', 'Nifty Bank', 'Emerge', 'Securities in F&O', 'Others', 'All']

    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Upgrade-Insecure-Requests': "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8",
            'Accept-Language': 'en-US,en;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)
        self.cookies = self.session.cookies.get_dict()

    def pre_market_info(self, category='All'):
        pre_market_xref = {"NIFTY 50": "NIFTY", "Nifty Bank": "BANKNIFTY", "Emerge": "SME", "Securities in F&O": "FO",
                           "Others": "OTHERS", "All": "ALL"}

        ref_url = 'https://www.nseindia.com/market-data/pre-open-market-cm-and-emerge-market'
        ref = requests.get(ref_url, headers=self.headers)
        url = f"https://www.nseindia.com/api/market-data-pre-open?key={pre_market_xref[category]}"
        response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
        processed_data = []
        data = response.json()['data']
        for i in data:
            processed_data.append(i["metadata"])
        df = pd.DataFrame(processed_data)
        df = df.set_index("symbol", drop=True)
        return df

    def get_index_details(self, category, list_only=False):
        category = category.upper().replace('&', '%26').replace(' ', '%20')

        ref_url = "https://www.nseindia.com/market-data/live-equity-market?symbol={category}"
        ref = requests.get(ref_url, headers=self.headers)
        url = f"https://www.nseindia.com/api/equity-stockIndices?index={category}"
        data = requests.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()

        # ✅ Only extract specific keys from each dictionary
        keys_to_extract = ['symbol', 'priority','open', 'dayHigh', 'dayLow', 'lastPrice', 'previousClose', 'change', 'pChange', 'ffmc', 'yearHigh', 'yearLow', 'totalTradedVolume', 'totalTradedValue', 'perChange30d', 'perChange365d']
        filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in data['data']]
        df = pd.DataFrame(filtered_data)
        if list_only:
            symbol_list = sorted(df.index[1:].tolist())
            return symbol_list
        else:
            return df

    def clearing_holidays(self, list_only=False):
        """
        Returns the list of NSE clearing holidays
        :param list_only: If case of  list_only, the holidays are returned as a simple list. Else
        full details are provided in a dataframe
        :return:
        """
        response = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={'Clearing'.lower()}',
                                headers=self.headers).json()
        data = list(response.values())[0]

        # ✅ Only extract specific keys from each dictionary
        keys_to_extract = ['tradingDate', 'weekDay','description', 'Sr_no']
        filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in data]

        df = pd.DataFrame(filtered_data)
        df.set_index('Sr_no', inplace=True)
        if list_only:
            holiday_list = df['tradingDate'].tolist()
            return holiday_list
        else:
            return df

    def trading_holidays(self, list_only=False):
        """
        Returns the list of NSE trading holidays
        :param list_only: If case of  list_only, the holidays are returned as a simple list. Else
        full details are provided in a dataframe
        :return:
        """
        response = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={'Trading'.lower()}',
                                headers=self.headers).json()
        data = list(response.values())[0]

        # ✅ Only extract specific keys from each dictionary
        keys_to_extract = ['tradingDate', 'weekDay','description', 'Sr_no']
        filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in data]

        df = pd.DataFrame(filtered_data)
        df.set_index('Sr_no', inplace=True)
        if list_only:
            holiday_list = df['tradingDate'].tolist()
            return holiday_list
        else:
            return df

    def is_nse_trading_holiday(self, date_str=None):
        """
        Return True if the date supplied in a NSE trading holiday, else False
        :param date_str: Optional. If no date provided, current data will be assumed
        :return:
        """
        holidays = self.trading_holidays(list_only=True)  # Fetch Trading holiday list from NSE

        date_format = "%d-%b-%Y"  # Define the expected date format
        # If date_str is provided, validate and parse it
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, date_format)  # Convert string to datetime
            except ValueError:
                print("Error: Invalid date format! Please use 'DD-MMM-YYYY' (e.g., '19-Feb-2025').")
                return None
        else:
            date_obj = datetime.today()  # Use today's date if no input is given

        formatted_date = date_obj.strftime(date_format)  # Convert date back to the required format
        return formatted_date in holidays  # Check if it’s a holiday

    def is_nse_clearing_holiday(self, date_str=None):
        """
        Return True if the date supplied in a NSE clearing holiday, else False
        :param date_str: Optional. If no date provided, current data will be assumed
        :return:
        """
        holidays = self.clearing_holidays(list_only=True)  # Fetch Trading holiday list from NSE

        date_format = "%d-%b-%Y"  # Define the expected date format
        # If date_str is provided, validate and parse it
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, date_format)  # Convert string to datetime
            except ValueError:
                print("Error: Invalid date format! Please use 'DD-MMM-YYYY' (e.g., '19-Feb-2025').")
                return None
        else:
            date_obj = datetime.today()  # Use today's date if no input is given

        formatted_date = date_obj.strftime(date_format)  # Convert date back to the required format
        return formatted_date in holidays  # Check if it’s a holiday

    def equity_info(self, symbol):
        """
        Extracts the full details of a symbol as see on NSE website
        :param symbol:
        :return:
        """
        symbol = symbol.replace(' ', '%20').replace('&', '%26')

        # Fetch primary details
        ref_url = 'https://www.nseindia.com/get-quotes/equity?symbol=' + symbol
        ref = requests.get(ref_url, headers=self.headers)
        url = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol
        data = requests.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()

        # Fetch Trade Data for symbol  ('Trade Information' tab on NSE website)
        url = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol + "&section=trade_info"
        trade_data = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()

        # Merge Meta data with Trade Information into final dataset
        data['tradeData'] = trade_data
        return data

    def price_info(self, symbol):
        """
        Gets all key price related information for a given stock
        :param symbol:
        :param trade_info:
        :return:
        """
        symbol = symbol.replace(' ', '%20').replace('&', '%26')
        ref_url = 'https://www.nseindia.com/get-quotes/equity?symbol=' + symbol
        ref = requests.get(ref_url, headers=self.headers)
        url = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol
        data = requests.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()
        if not data:
            return None
        if 'error' in data:
            return None

        return {
            "Symbol": symbol,
            "LastTradedPrice": data['priceInfo']['lastPrice'],
            "PreviousClose": data['priceInfo']['previousClose'],
            "Change": data['priceInfo']['change'],
            "PercentChange": data['priceInfo']['pChange'],
            "Open": data['priceInfo']['open'],
            "Close": data['priceInfo']['close'],
            "High": data['priceInfo']['intraDayHighLow']['max'],
            "Low": data['priceInfo']['intraDayHighLow']['min'],
            "VWAP": data['priceInfo']['vwap'],
            "UpperCircuit": data['priceInfo']['upperCP'],
            "LowerCircuit": data['priceInfo']['lowerCP'],
        }

    def futures_data(self, symbol, indices=False):
        """
        Returns the list of futures instruments for a given stock and its  details
        :param symbol:
        :param indices: This is to set to true if symbol is an index
        :return:
        """
        symbol = symbol.replace(' ', '%20').replace('&', '%26')

        ref_url = 'https://www.nseindia.com/get-quotes/derivatives?symbol=' + symbol
        ref = requests.get(ref_url, headers=self.headers)

        url = 'https://www.nseindia.com/api/quote-derivative?symbol=' + symbol
        data = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()

        lst = []
        for i in data["stocks"]:
            if i["metadata"]["instrumentType"] == ("Index Futures" if indices else "Stock Futures"):
                lst.append(i["metadata"])
        df = pd.DataFrame(lst)
        df = df.set_index("identifier", drop=True)
        return df

    def get_option_chain(self, symbol, indices=False):
        """
        Returns the full option chain table as seen on NSE website for the given stock/index
        :param symbol:
        :param indices:
        :return:
        """
        symbol = symbol.replace(' ', '%20').replace('&', '%26')
        if not indices:
            ref_url = 'https://www.nseindia.com/get-quotes/derivatives?symbol=' + symbol
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/option-chain-equities?symbol=' + symbol
            data = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()["records"]
        else:
            ref_url = 'https://www.nseindia.com/get-quotes/derivatives?symbol=' + symbol
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/option-chain-indices?symbol=' + symbol
            data = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()["records"]

        my_df = []
        for i in data["data"]:
            for k, v in i.items():
                if k == "CE" or k == "PE":
                    info = v
                    info["instrumentType"] = k
                    info["timestamp"] = data["timestamp"]
                    my_df.append(info)
        df = pd.DataFrame(my_df)
        df = df.set_index("identifier", drop=True)
        return df

    def get_52week_high_low(self, stock=None):
        """
        Get 52 Week High and Low data.  If stock is provided, the High/Low data for that
        particular stock is returned. If not, the  full list is returned
        :param stock: Optional
        :return:
        """
        url = 'https://nsearchives.nseindia.com/content/CM_52_wk_High_low_25012024.csv'

        response = requests.get(url, headers=self.headers)
        data = StringIO(response.text.replace(
            '"Disclaimer - The Data provided in the adjusted 52 week high and adjusted 52 week low columns  are adjusted for corporate actions (bonus, splits & rights).For actual (unadjusted) 52 week high & low prices, kindly refer bhavcopy."\n"Effective for 25-Jan-2024"\n',
            ''))
        df = pd.read_csv(data)
        if stock is not None:
            # Return the full 52 Week High/Low list of stock input
            row = df[df['SYMBOL'] == stock]
            if row.empty:
                return None
            return {
                "Symbol": stock,
                "52 Week High": row["Adjusted 52_Week_High"].values[0],
                "52 Week High Date": row["52_Week_High_Date"].values[0],
                "52 Week Low": row["Adjusted 52_Week_Low"].values[0],
                "52 Week Low Date": row["52_Week_Low_DT"].values[0]
            }
        # Return the full 52 Week High/Low list of all stocks
        return df

    def fno_bhav_copy(self, trade_date: str = ""):
        """
        Get the NSE FNO bhav copy data as per the traded date
        :param trade_date: eg:'20-06-2023'
        :return: pandas data frame
        """
        bhav_df = pd.DataFrame()
        trade_date = datetime.strptime(trade_date, "%d-%m-%Y")
        url = 'https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_'
        payload = f"{str(trade_date.strftime('%Y%m%d'))}_F_0000.csv.zip"
        request_bhav = requests.get(url + payload, headers=self.headers)
        bhav_df = pd.DataFrame()

        if request_bhav.status_code == 200:
            zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), 'r')
            for file_name in zip_bhav.filelist:
                if file_name:
                    bhav_df = pd.read_csv(zip_bhav.open(file_name))
        elif request_bhav.status_code == 403:
            url2 = "https://www.nseindia.com/api/reports?archives=" \
                   "%5B%7B%22name%22%3A%22F%26O%20-%20Bhavcopy(csv)%22%2C%22type%22%3A%22archives%22%2C%22category%22" \
                   f"%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date={str(trade_date.strftime('%d-%b-%Y'))}" \
                   f"&type=equity&mode=single"
            request_bhav = requests.get(url2 + payload, headers=self.headers)
            if request_bhav.status_code == 200:
                zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), 'r')
                for file_name in zip_bhav.filelist:
                    if file_name:
                        bhav_df = pd.read_csv(zip_bhav.open(file_name))
            elif request_bhav.status_code == 403:
                raise FileNotFoundError(f' Data not found, change the date...')

        return bhav_df

    def bhav_copy_with_delivery(self, trade_date: str):
        """
        Get the NSE bhav copy with delivery data as per the traded date
        :param trade_date: eg:'20-06-2023'
        :return: pandas data frame
        """
        trade_date = datetime.strptime(trade_date, "%d-%m-%Y")
        use_date = trade_date.strftime("%d%m%Y")
        url = f'https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{use_date}.csv'
        request_bhav = requests.get(url, headers=self.headers)
        if request_bhav.status_code == 200:
            bhav_df = pd.read_csv(BytesIO(request_bhav.content))
        else:
            raise FileNotFoundError(f' Data not found, change the trade_date...')
        bhav_df.columns = [name.replace(' ', '') for name in bhav_df.columns]
        bhav_df['SERIES'] = bhav_df['SERIES'].str.replace(' ', '')
        bhav_df['DATE1'] = bhav_df['DATE1'].str.replace(' ', '')
        return bhav_df

    def equity_bhav_copy(self, trade_date: str):
        """
        Extract Equity Bhav Copy per the traded date provided
        :param trade_date:
        :return: pandas dataframe
        """
        trade_date = datetime.strptime(trade_date, "%d-%m-%Y")
        # trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
        url = 'https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_'
        payload = f"{str(trade_date.strftime('%Y%m%d'))}_F_0000.csv.zip"
        request_bhav = requests.get(url + payload, headers=self.headers)
        bhav_df = pd.DataFrame()
        if request_bhav.status_code == 200:
            zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), 'r')
            for file_name in zip_bhav.filelist:
                if file_name:
                    bhav_df = pd.read_csv(zip_bhav.open(file_name))
        elif request_bhav.status_code == 403:
            raise FileNotFoundError(f' Data not found, change the trade_date...')
        return bhav_df

    def bhav_copy_indices(self, trade_date: str):
        """
        Get nse bhav copy as per the traded date provided
        :param trade_date: eg:'20-06-2023'
        :return: pandas dataframe
        """
        trade_date = datetime.strptime(trade_date, "%d-%m-%Y")
        url = f"https://nsearchives.nseindia.com/content/indices/ind_close_all_{str(trade_date.strftime('%d%m%Y').upper())}.csv"
        # nse_resp = nse_urlfetch(url)
        nse_resp = requests.get(url, headers=self.headers)
        if nse_resp.status_code != 200:
            raise FileNotFoundError(f" No data available for : {trade_date}")
        try:
            bhav_df = pd.read_csv(BytesIO(nse_resp.content))
        except Exception as e:
            raise FileNotFoundError(f' Bhav copy indices not found for : {trade_date} :: NSE error : {e}')
        return bhav_df

    def fii_dii_activity(self):
        """
        FII and DII trading activity of the day in data frame
        :return: pd.DataFrame
        """
        ref_url = 'https://www.nseindia.com/reports/fii-dii'
        ref = requests.get(ref_url, headers=self.headers)
        url = 'https://www.nseindia.com/api/fiidiiTradeReact'
        response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
        data = response.json()  # Convert response to JSON
        data_df = pd.DataFrame(data)
        return data_df

    def get_live_option_chain(self, symbol: str, expiry_date: str | None = None, oi_mode: str = "full", indices=False):
        """
        get live nse option chain.
        :param symbol: eg:SBIN/BANKNIFTY
        :param expiry_date: '20-06-2023'
        :param oi_mode: eg: full/compact
        :return: pands dataframe
        """
        symbol = symbol.replace(' ', '%20').replace('&', '%26')
        ref_url = 'https://www.nseindia.com/option-chain'
        ref = requests.get(ref_url, headers=self.headers)
        if not indices:
            url = 'https://www.nseindia.com/api/option-chain-equities?symbol=' + symbol
        else:
            # ref_url = 'https://www.nseindia.com/option-chain'
            # ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/option-chain-indices?symbol=' + symbol
        payload = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()
        # payload = get_nse_option_chain(symbol).json()
        if expiry_date:
            exp_date = pd.to_datetime(expiry_date, format='%d-%m-%Y')
            expiry_date = exp_date.strftime('%d-%b-%Y')

        if oi_mode == 'compact':
            col_names = ['Fetch_Time', 'Symbol', 'Expiry_Date', 'CALLS_OI', 'CALLS_Chng_in_OI', 'CALLS_Volume',
                         'CALLS_IV',
                         'CALLS_LTP', 'CALLS_Net_Chng', 'Strike_Price', 'PUTS_OI', 'PUTS_Chng_in_OI', 'PUTS_Volume',
                         'PUTS_IV', 'PUTS_LTP', 'PUTS_Net_Chng']
        else:
            col_names = ['Fetch_Time', 'Symbol', 'Expiry_Date', 'CALLS_OI', 'CALLS_Chng_in_OI', 'CALLS_Volume',
                         'CALLS_IV',
                         'CALLS_LTP', 'CALLS_Net_Chng', 'CALLS_Bid_Qty', 'CALLS_Bid_Price', 'CALLS_Ask_Price',
                         'CALLS_Ask_Qty', 'Strike_Price', 'PUTS_Bid_Qty', 'PUTS_Bid_Price', 'PUTS_Ask_Price',
                         'PUTS_Ask_Qty',
                         'PUTS_Net_Chng', 'PUTS_LTP', 'PUTS_IV', 'PUTS_Volume', 'PUTS_Chng_in_OI', 'PUTS_OI']

        oi_data = pd.DataFrame(columns=col_names)

        oi_row = {'Fetch_Time': None, 'Symbol': None, 'Expiry_Date': None, 'CALLS_OI': 0, 'CALLS_Chng_in_OI': 0,
                  'CALLS_Volume': 0,
                  'CALLS_IV': 0, 'CALLS_LTP': 0, 'CALLS_Net_Chng': 0, 'CALLS_Bid_Qty': 0, 'CALLS_Bid_Price': 0,
                  'CALLS_Ask_Price': 0, 'CALLS_Ask_Qty': 0, 'Strike_Price': 0, 'PUTS_OI': 0, 'PUTS_Chng_in_OI': 0,
                  'PUTS_Volume': 0, 'PUTS_IV': 0, 'PUTS_LTP': 0, 'PUTS_Net_Chng': 0, 'PUTS_Bid_Qty': 0,
                  'PUTS_Bid_Price': 0, 'PUTS_Ask_Price': 0, 'PUTS_Ask_Qty': 0}

        for m in range(len(payload['records']['data'])):
            if not expiry_date or (payload['records']['data'][m]['expiryDate'] == expiry_date):
                try:
                    oi_row['Expiry_Date'] = payload['records']['data'][m]['expiryDate']
                    oi_row['CALLS_OI'] = payload['records']['data'][m]['CE']['openInterest']
                    oi_row['CALLS_Chng_in_OI'] = payload['records']['data'][m]['CE']['changeinOpenInterest']
                    oi_row['CALLS_Volume'] = payload['records']['data'][m]['CE']['totalTradedVolume']
                    oi_row['CALLS_IV'] = payload['records']['data'][m]['CE']['impliedVolatility']
                    oi_row['CALLS_LTP'] = payload['records']['data'][m]['CE']['lastPrice']
                    oi_row['CALLS_Net_Chng'] = payload['records']['data'][m]['CE']['change']
                    if oi_mode == 'full':
                        oi_row['CALLS_Bid_Qty'] = payload['records']['data'][m]['CE']['bidQty']
                        oi_row['CALLS_Bid_Price'] = payload['records']['data'][m]['CE']['bidprice']
                        oi_row['CALLS_Ask_Price'] = payload['records']['data'][m]['CE']['askPrice']
                        oi_row['CALLS_Ask_Qty'] = payload['records']['data'][m]['CE']['askQty']
                except KeyError:
                    oi_row['CALLS_OI'], oi_row['CALLS_Chng_in_OI'], oi_row['CALLS_Volume'], oi_row['CALLS_IV'], oi_row[
                        'CALLS_LTP'], oi_row['CALLS_Net_Chng'] = 0, 0, 0, 0, 0, 0
                    if oi_mode == 'full':
                        oi_row['CALLS_Bid_Qty'], oi_row['CALLS_Bid_Price'], oi_row['CALLS_Ask_Price'], oi_row[
                            'CALLS_Ask_Qty'] = 0, 0, 0, 0
                    pass

                oi_row['Strike_Price'] = payload['records']['data'][m]['strikePrice']

                try:
                    oi_row['PUTS_OI'] = payload['records']['data'][m]['PE']['openInterest']
                    oi_row['PUTS_Chng_in_OI'] = payload['records']['data'][m]['PE']['changeinOpenInterest']
                    oi_row['PUTS_Volume'] = payload['records']['data'][m]['PE']['totalTradedVolume']
                    oi_row['PUTS_IV'] = payload['records']['data'][m]['PE']['impliedVolatility']
                    oi_row['PUTS_LTP'] = payload['records']['data'][m]['PE']['lastPrice']
                    oi_row['PUTS_Net_Chng'] = payload['records']['data'][m]['PE']['change']
                    if oi_mode == 'full':
                        oi_row['PUTS_Bid_Qty'] = payload['records']['data'][m]['PE']['bidQty']
                        oi_row['PUTS_Bid_Price'] = payload['records']['data'][m]['PE']['bidprice']
                        oi_row['PUTS_Ask_Price'] = payload['records']['data'][m]['PE']['askPrice']
                        oi_row['PUTS_Ask_Qty'] = payload['records']['data'][m]['PE']['askQty']
                except KeyError:
                    oi_row['PUTS_OI'], oi_row['PUTS_Chng_in_OI'], oi_row['PUTS_Volume'], oi_row['PUTS_IV'], oi_row[
                        'PUTS_LTP'], oi_row['PUTS_Net_Chng'] = 0, 0, 0, 0, 0, 0
                    if oi_mode == 'full':
                        oi_row['PUTS_Bid_Qty'], oi_row['PUTS_Bid_Price'], oi_row['PUTS_Ask_Price'], oi_row[
                            'PUTS_Ask_Qty'] = 0, 0, 0, 0

                if oi_data.empty:
                    oi_data = pd.DataFrame([oi_row]).copy()
                else:
                    oi_data = pd.concat([oi_data, pd.DataFrame([oi_row])], ignore_index=True)
                oi_data['Symbol'] = symbol
                oi_data['Fetch_Time'] = payload['records']['timestamp']
        return oi_data

    def get_market_depth(self, symbol):

        """
        Function to retrieve market depth for a given symbol
        :param symbol:
        :return: Market Dept as Dict
        """
        data = self.equity_info(symbol)
        merged_dict = {
            'ask': data['tradeData']['marketDeptOrderBook']['ask'],
            'bid': data['tradeData']['marketDeptOrderBook']['bid']
        }
        return merged_dict

    def get_index_historic_data(self, index: str, from_date: str | None = None, to_date: str | None = None):
        """
        get historical index data set for the specific time period.
        apply the index name as per the nse india site
        :param index: 'NIFTY 50'/'NIFTY BANK'
        :param from_date: '17-03-2022' ('dd-mm-YYYY')
        :param to_date: '17-06-2023' ('dd-mm-YYYY')
        :return: pandas.DataFrame
        :raise ValueError if the parameter input is not proper
        """
        index_data_columns = ['TIMESTAMP', 'INDEX_NAME', 'OPEN_INDEX_VAL', 'HIGH_INDEX_VAL', 'CLOSE_INDEX_VAL',
                              'LOW_INDEX_VAL', 'TRADED_QTY', 'TURN_OVER']

        # Check for valid dates and period inputs
        if not from_date or not to_date:
            raise ValueError(' Please provide the valid parameters')

        try:
            from_dt = datetime.strptime(from_date, "%d-%m-%Y")
            to_dt = datetime.strptime(to_date, "%d-%m-%Y")
            time_delta = (to_dt - from_dt).days
            if time_delta < 1:
                raise ValueError(f'to_date should greater than from_date ')
        except Exception as e:
            print(e)
            raise ValueError(f'either or both from_date = {from_date} || to_date = {to_date} are not valid value')

        nse_df = pd.DataFrame(columns=index_data_columns)
        from_date = datetime.strptime(from_date, "%d-%m-%Y")
        to_date = datetime.strptime(to_date, "%d-%m-%Y")
        load_days = (to_date - from_date).days

        while load_days > 0:
            if load_days > 365:
                end_date = (from_date + timedelta(364)).strftime("%d-%m-%Y")
                start_date = from_date.strftime("%d-%m-%Y")
            else:
                end_date = to_date.strftime("%d-%m-%Y")
                start_date = from_date.strftime("%d-%m-%Y")

            data_df = self.get_index_data(index=index, from_date=start_date, to_date=end_date)
            from_date = from_date + timedelta(365)
            load_days = (to_date - from_date).days
            if nse_df.empty:
                nse_df = data_df
            else:
                nse_df = pd.concat([nse_df, data_df], ignore_index=True)
        return nse_df

    def get_index_data(self, index: str, from_date: str, to_date: str):

        index_data_columns = ['TIMESTAMP', 'INDEX_NAME', 'OPEN_INDEX_VAL', 'HIGH_INDEX_VAL', 'CLOSE_INDEX_VAL',
                              'LOW_INDEX_VAL', 'TRADED_QTY', 'TURN_OVER']

        index = index.replace(' ', '%20').upper()
        ref_url = 'https://www.nseindia.com/reports-indices-historical-index-data'
        ref = requests.get(ref_url, headers=self.headers)

        url = f"https://www.nseindia.com/api/historical/indicesHistory?indexType={index}&from={from_date}&to={to_date}"

        try:
            data_json = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict()).json()

            data_close_df = pd.DataFrame(data_json['data']['indexCloseOnlineRecords']).drop(
                columns=['_id', "EOD_TIMESTAMP"])
            data_turnover_df = pd.DataFrame(data_json['data']['indexTurnoverRecords']).drop(columns=['_id',
                                                                                                     'HIT_INDEX_NAME_UPPER'])
            data_df = pd.merge(data_close_df, data_turnover_df, on='TIMESTAMP', how='inner')
        except Exception as e:
            raise " Resource not available"

        data_df.drop(columns='TIMESTAMP', inplace=True)

        unwanted_str_list = ['FH_', 'EOD_', 'HIT_']
        new_col = data_df.columns
        for unwanted in unwanted_str_list:
            new_col = [name.replace(f'{unwanted}', '') for name in new_col]

        data_df.columns = new_col
        return data_df[index_data_columns]

    def get_equity_full_list(self, list_only=False):
        """
        get list of all equity available to trade in NSE
        :param list_only: Optional. If you only need the symbols in a list, set this to true.
        Otherwise, the full table is downloaded as a dataframe
        :return: pandas data frame
        """
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        nse_resp = self.session.get(url, headers=self.headers, cookies=self.cookies)
        if nse_resp.status_code != 200:
            raise FileNotFoundError(f" No data equity list available")
        try:
            data_df = pd.read_csv(BytesIO(nse_resp.content))
        except Exception as e:
            raise FileNotFoundError(f' Equity List not found :: NSE error : {e}')
        data_df = data_df[['SYMBOL', 'NAME OF COMPANY', ' SERIES', ' DATE OF LISTING', ' FACE VALUE']]
        if list_only:
            symbol_list = data_df['SYMBOL'].tolist()
            return symbol_list
        return data_df

    def get_fno_full_list(self, list_only=False):
        """
        get a dataframe of all listed derivative list with the recent lot size to trade
        :param list_only: Optional. If you only need the symbols in a list, set this to true.
        Otherwise, the full table is downloaded as a dataframe
        :return: pandas data frame
        """
        ref_url = 'https://www.nseindia.com/products-services/equity-derivatives-list-underlyings-information'
        ref = requests.get(ref_url, headers=self.headers)
        url = "https://www.nseindia.com/api/underlying-information"
        response = requests.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

        if response.status_code != 200:
            raise ("Resource not available for fno_equity_list")
        data_dict = response.json()
        data_df = pd.DataFrame(data_dict['data']['UnderlyingList'])
        if list_only:
            symbol_list = data_df['symbol'].tolist()
            return symbol_list
        return data_df

    def get_gainers_losers(self):

        gain_loss_dict = {}

        ref_url = 'https://www.nseindia.com/market-data/top-gainers-losers'
        ref = requests.get(ref_url, headers=self.headers)

        url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers'
        data_obj = requests.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
        if data_obj.status_code != 200:
            raise ("Resource not available for fno_equity_list")
        data_dict = data_obj.json()

        # Nifty Gainer
        data_df = pd.DataFrame(data_dict['NIFTY']['data'])
        nifty_gainer = data_df['symbol'].to_list()

        # Bank Nifty Gainer
        data_df = pd.DataFrame(data_dict['BANKNIFTY']['data'])
        banknifty_gainer = data_df['symbol'].to_list()

        # Nifty Next 50 Gainer
        data_df = pd.DataFrame(data_dict['NIFTYNEXT50']['data'])
        next50_gainer = data_df['symbol'].to_list()

        # All Securities Gainer
        data_df = pd.DataFrame(data_dict['allSec']['data'])
        allsec_gainer = data_df['symbol'].to_list()

        # FNO Securities Gainer
        data_df = pd.DataFrame(data_dict['FOSec']['data'])
        fno_gainer = data_df['symbol'].to_list()

        url = 'https://www.nseindia.com/api/live-analysis-variations?index=loosers'
        data_obj = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
        if data_obj.status_code != 200:
            raise ("Resource not available for fno_equity_list")
        data_dict = data_obj.json()

        # Nifty Gainer
        data_df = pd.DataFrame(data_dict['NIFTY']['data'])
        nifty_loser = data_df['symbol'].to_list()

        # Bank Nifty Gainer
        data_df = pd.DataFrame(data_dict['BANKNIFTY']['data'])
        banknifty_loser = data_df['symbol'].to_list()

        # Bank Nifty Gainer
        data_df = pd.DataFrame(data_dict['NIFTYNEXT50']['data'])
        next50_loser = data_df['symbol'].to_list()

        # All Securities Gainer
        data_df = pd.DataFrame(data_dict['allSec']['data'])
        allsec_loser = data_df['symbol'].to_list()

        # FNO Securities Gainer
        data_df = pd.DataFrame(data_dict['FOSec']['data'])
        fno_loser = data_df['symbol'].to_list()

        gain_dict = {
            'Nifty Gainer': nifty_gainer,
            'Bank Nifty Gainer': banknifty_gainer,
            'Nifty Next 50 Gainer': next50_gainer,
            'All Securities Gainer': allsec_gainer,
            'FNO Gainer': fno_gainer
        }

        loss_dict = {
            'Nifty Loser': nifty_loser,
            'Bank Nifty Loser': banknifty_loser,
            'Nifty Next 50 Loser': next50_loser,
            'All Securities Loser': allsec_loser,
            'FNO Loser': fno_loser
        }

        return gain_dict, loss_dict

    def get_corporate_action(self, symbol: str | None = None, from_date_str: str | None = None, to_date_str: str | None = None, filter: str | None = None):

        # Fetch Corporate Action data from NSE
        if from_date_str is None:
            from_date  = datetime.now() - timedelta(days=30)
            from_date_str = from_date.strftime("%d-%m-%Y")
            to_date_str = datetime.now().strftime("%d-%m-%Y")
        if to_date_str is None:
            to_date_str = datetime.now().strftime("%d-%m-%Y")
        try:
            ref_url = 'https://www.nseindia.com/companies-listing/corporate-filings-actions'
            ref = requests.get(ref_url, headers=self.headers)

            if symbol is not None:
                url = f"https://www.nseindia.com/api/corporates-corporateActions?index=equities&symbol={symbol}&from_date={from_date_str}&to_date={to_date_str}"
            else:
                url = f"https://www.nseindia.com/api/corporates-corporateActions?index=equities&from_date={from_date_str}&to_date={to_date_str}"
            data_obj = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            all_data = data_obj.json()

            # ✅ Only extract specific keys from each dictionary
            keys_to_extract = ['symbol', 'comp','series', 'subject', 'faceVal', 'exDate', 'recDate']
            filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in all_data]

            corp_action = pd.DataFrame(filtered_data)

            if corp_action.empty:
                return None

            if filter is not None:
                corp_action = corp_action[corp_action['purpose'].str.contains(filter, case=False, na=False)]

            return corp_action

        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            print("Details:", e)
            return None

    def get_corporate_announcement(self, from_date_str: str | None = None, to_date_str: str | None = None):

        # Fetch Corporate Announcements data from NSE
        if from_date_str is None:
            from_date  = datetime.now() - timedelta(days=30)
            from_date_str = from_date.strftime("%d-%m-%Y")
            to_date_str = datetime.now().strftime("%d-%m-%Y")
        if to_date_str is None:
            to_date_str = datetime.now().strftime("%d-%m-%Y")

        try:
            ref_url = ('https://www.nseindia.com/companies-listing/corporate-filings-announcements')
            ref = requests.get(ref_url, headers=self.headers)
            url = f'https://www.nseindia.com/api/corporate-announcements?index=equities&from_date={from_date_str}&to_date={to_date_str}'
            data_obj = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            # ✅ Only extract specific keys from each dictionary
            keys_to_extract = ['symbol', 'sm_name','desc', 'attchmntFile', 'attchmntText', 'exchdisstime']
            filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in data_obj.json()]

            corp_announcement = pd.DataFrame(filtered_data)
            return corp_announcement
        except:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def get_index_pe_ratio(self):

        # try:
            ref_url = 'https://www.nseindia.com/market-data/index-performances'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/allIndices'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON

            # Convert JSON data to a DataFrame
            df = pd.json_normalize(data['data'])  # Extract the main data list

            # Retain only PE Ratio
            if not df.empty:
                df = df[['indexSymbol', 'key', 'pe']]
                df = df[df['pe'].str.strip() != '']  # Removes rows where PE is an empty string
                df = df[df['pe'].str.strip() != 'None']  # Removes rows where PE is none
                df.columns = ['Index', 'Type', 'Profit Earning Ratio']
                return df
            else:
                return None

        # except:
        #     print("Error fetching Corporate Action Data. Check your input")
        #     return None

    def get_index_pb_ratio(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/index-performances'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/allIndices'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON

            # Convert JSON data to a DataFrame
            df = pd.json_normalize(data['data'])  # Extract the main data list

            # Retain only PE Ratio
            if not df.empty:
                df = df[['indexSymbol', 'key', 'pb']]
                df = df[df['pb'].str.strip() != '']  # Removes rows where PE is an empty string
                df = df[df['pb'].str.strip() != 'None']  # Removes rows where PE is none
                df.columns = ['Index', 'Type', 'Price Book Ratio']
                return df
            else:
                return None

        except:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def get_index_div_yield(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/index-performances'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/allIndices'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON

            # Convert JSON data to a DataFrame
            df = pd.json_normalize(data['data'])  # Extract the main data list

            # Retain only PE Ratio
            if not df.empty:
                df = df[['indexSymbol', 'key', 'dy']]
                df = df[df['dy'].str.strip() != '']  # Removes rows where PE is an empty string
                df = df[df['dy'].str.strip() != 'None']  # Removes rows where PE is none
                df.columns = ['Index', 'Type', 'Div Yield']
                return df
            else:
                return None

        except:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def get_advance_decline(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/live-market-indices'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/allIndices'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON

            # Convert JSON data to a DataFrame
            df = pd.json_normalize(data['data'])  # Extract the main data list

            # Retain only PE Ratio
            if not df.empty:
                df = df[['indexSymbol', 'advances', 'declines', 'unchanged']]
                df.dropna(inplace=True)
                df.columns = ['Index', 'Advances', 'Declines', 'Unchanged']
                return df
            else:
                return None

        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_equity_stocks(self, index_str: str):
        if index_str not in ['volume', 'value']:
            raise ValueError("Invalid index_str. Use 'volume' or 'value'.")
        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-equities'
            ref = requests.get(ref_url, headers=self.headers)
            url = f'https://www.nseindia.com/api/live-analysis-most-active-securities?index={index_str}'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()['data']  # Convert response to JSON

            # ✅ Only extract specific keys from each dictionary
            keys_to_extract = ['symbol', 'open', 'dayHigh', 'dayLow', 'lastPrice', 'previousClose', 'change', 'pChange', 'totalTradedVolume', 'totalTradedValue', 'yearHigh', 'yearLow', 'lastUpdateTime']
            filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in data]

            # Convert JSON data to a DataFrame
            df = pd.DataFrame(filtered_data)  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_equity_etf(self, index_str: str):
        if index_str not in ['volume', 'value']:
            raise ValueError("Invalid index_str. Use 'volume' or 'value'.")
        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-equities'
            ref = requests.get(ref_url, headers=self.headers)
            url = f'https://www.nseindia.com/api/live-analysis-most-active-etf?index={index_str}'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()['data']  # Convert response to JSON

            # ✅ Only extract specific keys from each dictionary
            keys_to_extract = ['symbol', 'open', 'dayHigh', 'dayLow', 'lastPrice', 'nav', 'previousClose', 'pChange', 'totalTradedVolume', 'totalTradedValue']
            filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in data]

            # Convert JSON data to a DataFrame
            df = pd.DataFrame(filtered_data)  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_index_calls(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=calls-index-vol'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['OPTIDX']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_index_puts(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=puts-index-vol'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['OPTIDX']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_stock_calls(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=calls-stocks-vol'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['OPTSTK']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_stock_puts(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=puts-stocks-vol'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['OPTSTK']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_contracts_by_oi(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=oi'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['volume']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_contracts_by_volume(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=contracts'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['volume']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_futures_contracts_by_volume(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=futures'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())

            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['volume']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def most_active_options_contracts_by_volume(self):

        try:
            ref_url = 'https://www.nseindia.com/market-data/most-active-contracts'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-derivatives-equity?index=options&limit=20'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['volume']['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def get_insider_trading(self, from_date: str | None = None, to_date: str | None= None):

        try:

            if from_date is None:
                from_date  = datetime.now() - timedelta(days=30)
                from_date_str = from_date.strftime("%d-%m-%Y")
                to_date_str = datetime.now().strftime("%d-%m-%Y")
            else:
                from_date_str = from_date
            if to_date is None:
                to_date_str = datetime.now().strftime("%d-%m-%Y")
            else:
                to_date_str = to_date

            ref_url = 'https://www.nseindia.com/companies-listing/corporate-filings-insider-trading'
            ref = requests.get(ref_url, headers=self.headers)
            url= f'https://www.nseindia.com/api/corporates-pit?index=equities&from_date={from_date_str}&to_date={to_date_str}'
            response = requests.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()
            df = pd.DataFrame(data['data'])

            return df

        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def get_upcoming_results_calendar(self, symbol: str | None = None, from_date_str: str | None = None, to_date_str: str | None = None):

        if from_date_str is None:
            from_date  = datetime.now() - timedelta(days=30)
            from_date_str = from_date.strftime("%d-%m-%Y")
            to_date_str = datetime.now().strftime("%d-%m-%Y")
        if to_date_str is None:
            to_date_str = datetime.now().strftime("%d-%m-%Y")

        # Extracts the events calendar from NSE - Filters only the upcoming Financial results related events
        try:
            ref_url = 'https://www.nseindia.com/companies-listing/corporate-filings-event-calendar'
            ref = requests.get(ref_url, headers=self.headers)
            if symbol is not None:
                url = f"https://www.nseindia.com/api/event-calendar?index=equities&symbol={symbol}&from_date={from_date_str}&to_date={to_date_str}"
            else:
                url = f"https://www.nseindia.com/api/event-calendar?index=equities&from_date={from_date_str}&to_date={to_date_str}"
            response = requests.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()
            df = pd.DataFrame(data)
            events = df[df['purpose'].str.contains('Results', case=False, na=False)]
            if events.empty:
                return None
            return events
        except Exception as e:
            print("Error fetching Corporate Action Data. Check your input")
            return None

    def get_etf_list(self):

        
        try:
            ref_url = 'https://www.nseindia.com/market-data/exchange-traded-funds-etf'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/etf'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON
            # Convert JSON data to a DataFrame
            df = pd.DataFrame(data['data'])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print("Error fetching ETF list. Check your input")
            return None
    
    def large_deals(self, deal_str: str = 'BLOCK_DEALS_DATA'):
        if deal_str not in ['BLOCK_DEALS_DATA', 'BULK_DEALS_DATA', 'SHORT_DEALS_DATA']:
            raise ValueError("Invalid data type. Use 'BLOCK_DEALS_DATA' or 'LARGE_DEALS_DATA'.")
        try:
            ref_url = 'https://www.nseindia.com/market-data/large-deals'
            ref = requests.get(ref_url, headers=self.headers)
            url = 'https://www.nseindia.com/api/snapshot-capital-market-largedeal'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON

            df = pd.DataFrame(data[deal_str])  # Extract the main data list

            if df.empty:
                return None
            else:
                return df
        except Exception as e:
            print(e)
            print("Error fetching Large Deals Data. Check your input")
            return None
        
    #  accepted two arguments, one is self and the other is string 'gainers' or 'loosers'
    def get_gainers_losers_v2(self, index: str):
        
        if index not in ['gainers', 'loosers']:
            raise ValueError("Invalid data type. Use 'BLOCK_DEALS_DATA' or 'LARGE_DEALS_DATA'.")
        try:
            ref_url = 'https://www.nseindia.com/market-data/top-gainers-losers'
            ref = requests.get(ref_url, headers=self.headers)
            url = f'https://www.nseindia.com/api/live-analysis-variations?index={index}'
            response = self.session.get(url, headers=self.headers, cookies=ref.cookies.get_dict())
            data = response.json()  # Convert response to JSON
            return data
        except Exception as e:
            print(e)
            print("Error fetching Large Deals Data. Check your input")
            return None