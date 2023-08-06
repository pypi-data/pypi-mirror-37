# AlphaVantageAPI
*An Opinionated AlphaVantage API Wrapper in Python 3.7*

Access to the AlphaVantage requires a free API key, that can be found at http://www.alphavantage.co/support/#api-key.


## Description
This API was designed to simplify the process of aquiring *free* financial data for retail traders and investors from the financial markets.  While it does require Pandas, Pandas' methods help simplify saving data requests into a variety of file formats such as: csv (default), json, pkl, html, and txt.  If the openpyxl module is also installed, it can be saved as an Excel file: xlsx.

* Main Features
    * Returns a Pandas DataFrame.
    * Simplifies column names i.e. "1. open" -> "open".
    * Available export formats: csv (default), json, pkl, html, txt, xlsz (optional).
    * A help method to reduce looking up 'required' and 'optional' parameters for each function.
    * A call_history method to return all successful API calls



# Installation
## Required
```shell
pip install pandas
```

## Typical installation:
```shell
pip install alphaVantage-api
```

## With Excel file support:
```shell
pip install alphaVantage-api openpyxl
```

## For the most up to date version
<!-- Source installation: -->
```shell
git clone https://github.com/twopirllc/AlphaVantageAPI.git
pip install -e alphaVantage-api
```

# API Details
## Constructor Parameter Defaults
    api_key: str     = None
    premium: bool    = False
    output_size: str = 'compact'
    datatype: str    = 'json'
    export: bool     = False
    export_path: str = '~/av_data'
    output: str      = 'csv'
    clean: bool      = False
    proxy: dict      = {}


## Constructor Parameter Descriptions

#### api_key : *str*
* Default: None.  If None, then do not forget to set your environment variable AV_API_KEY to API key. Otherwise set it in the class constructor.  If you have a Premium API key, do not forget to set the premium property to True as well.
#### premium : *bool*
* Default: False.  Got premium?  Excellent!  You do not need to wait  15.02 seconds between each API call.
#### output_size : *str*
* Default: 'compact'. The other option is 'full'.  See AlphaVantage API documentation for more details.
#### datatype : *str*
* Default: 'json'. This is the preferred request type.  See AlphaVantage API documentation for more details.
#### export : *bool*
* Default: False.  Set it to True if you want to save the file locally according to the export_path property.
#### export_path : *bool*
* Default: *'~/av_data'*.  Or set it to a path you can write to.
#### output : *str*
* Default: 'csv'.  Other options are 'json', 'pkl', 'html', and 'txt'.  If openpyxl is installed, then you can use 'xlsz'.
#### clean : *bool*
* Default: False. Simplifies the column header names for instance: "1. open" -> "open".
#### proxy : *dict*
* Default: {}.  See requests API documentation for more details.


# Examples

## Initialization
```python
from alphaVantageAPI.alphavantage import AlphaVantage

# Initialize the AlphaVantage Class with default values
av = AlphaVantage(
        api_key=None,
        premium=False,
        output_size='compact',
        datatype='json',
        export=False,
        export_path='~/av_data',
        output='csv',
        clean=False,
        proxy={}
    )
```

## Free API Key
```python
# Your FREE API calls are throttled by 15.02 seconds. 
av = AlphaVantage(premium=False)
```

## Premium API Key
```python
# No API call throttling.
av = AlphaVantage(premium=True)
```  

## Save locally
```python
# Cleans and save requests to the default export_path in 'csv' format
av = AlphaVantage(export=True, output='csv', clean=True)
```

## Display Current settings
```python
print(av)
```

## Help
```python
# Help: lists all the functions AlphaVantage API supports
print(av.help())

# Print 'function' aliases
print(av.help('aliases'))

# Help with a specific API function
print(av.help('TIME_SERIES_DAILY'))

# Help with an indicator
print(av.help('BBANDS'))
```


## Data Acquisition Methods
```python
# FX / Currency
# fx(from_currency:str, to_currency:str = 'USD')
fx_usd_cad_df = av.fx(from_currency='USD', to_currency='CAD')


# Sectors
sectors_df = av.sectors()


## Digital/Crypto
# digital(symbol:str, market:str = 'USD', function:str = 'CD')
digital_btc_usd_df = av.digital(symbol='BTC', market='USD', function='CD')


## Intraday
# Intervals as integers or strings
# intraday(symbol:str, interval=5)
msft_I5_df = av.intraday(symbol='MSFT', interval=5)
msft_I60_df = av.intraday(symbol='MSFT', interval='60min')


## Generic Equity/ETF calls
# data(function:str, symbol:str = None, **kwargs)
# Daily
msft_D_df = av.data(symbol='MSFT', function='D')

# Daily Adjusted
msft_DA_df = av.data(symbol='MSFT', function='DA')


# List of symbols Daily
symbols = ['AAPL', 'MSFT', 'XLK']
tech_list = av.data('D', symbols)  # returns list of DataFrames


## Indicators
# SMA close 20 Indicator
msft_SMA_20_df = av.data(symbol='MSFT', function='SMA', series_type='close', time_period=20)

# Daily Stochastic Indicator
msft_STOCH_df = av.data('STOCH', symbols[1], interval='daily', series_type='close')
```

## Call History
```python
# Returns all successfull calls to the API
history_list = av.call_history()

# Pretty display of Call History
history_df = pd.DataFrame(history_list)[['symbol', 'function', 'interval', 'time_period']]
print(history_df)
```

# Contributing
Contributions are welcome and I am open to new ideas or implementations.

# Inspiration
Check out additional *AlphaVantage API* Python Wrappers by:

Romel Torres: https://github.com/RomelTorres/alpha_vantage

portfoliome: https://github.com/portfoliome/alphavantage