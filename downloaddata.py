import urllib.request, json
import os
import pandas as pd
import datetime as dt


class DataDownload:
    data_source = 'alphavantage'  # alphavantage or kaggle

    def data_download(self, ticker):

        if self.data_source == 'alphavantage':
            # ====================== Loading Data from Alpha Vantage ==================================

            api_key = '9BUDWA6HVN20AKGW'

            # JSON file with all the stock market data for AAL from the last 20 years
            url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s" % (
            ticker, api_key)

            # Save data to this file
            file_to_save = 'stock_market_data-%s.csv' % ticker

            # If you haven't already saved data,
            # Go ahead and grab the data from the url
            # And store date, low, high, volume, close, open values to a Pandas DataFrame
            if not os.path.exists(file_to_save):
                with urllib.request.urlopen(url_string) as url:
                    data = json.loads(url.read().decode())
                    # extract stock market data
                    data = data['Time Series (Daily)']
                    df = pd.DataFrame(columns=['Date', 'Low', 'High', 'Close', 'Open'])
                    for k, v in data.items():
                        date = dt.datetime.strptime(k, '%Y-%m-%d')
                        data_row = [date.date(), float(v['3. low']), float(v['2. high']),
                                    float(v['4. close']), float(v['1. open'])]
                        df.loc[-1, :] = data_row
                        df.index = df.index + 1
                print('Data saved to : %s' % file_to_save)
                df.to_csv(file_to_save)
                return df
            # If the data is already there, just load it from the CSV
            else:
                print('File already exists. Loading data from CSV')
                df = pd.read_csv(file_to_save , index_col=False)
                return df

        else:

            # ====================== Loading Data from Kaggle ==================================
            # You will be using HP's data. Feel free to experiment with other data.
            # But while doing so, be careful to have a large enough dataset and also pay attention to the data normalization
            df = pd.read_csv(os.path.join('Stocks', 'hpq.us.txt'), delimiter=',',
                             usecols=['Date', 'Open', 'High', 'Low', 'Close'])
            print('Loaded data from the Kaggle repository')
            return df

