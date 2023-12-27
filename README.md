# Trading Bot


## Used MACD and MA strategy # Invest_IQ

## Need to have a env 

### Mac
```
python3 -m venv .venv
```

### Window
```
py -3 -m venv .venv
```

## Activate the environment 

### Mac
```
.venv/bin/activate
```

### Window 
```
.venv\Scripts\activate
```

## need to make a config.py file for your API keys

```python
BASE_URL= ''
API_KEY = ""
SECRET = ""

#need this to access the lumibot API
ALPACA_CONFIG = {
#Put your own Alpaca key here:
"API_KEY": '',
#Put your own Alpaca secret here:
"API_SECRET": "",
#If you want to go live, you must change this
"ENDPOINT": "https://paper-api.alpaca.markets/",
}
```

you will need to add your API keys in here 

## github and website for Alpaca

https://github.com/alpacahq/alpaca-py?tab=readme-ov-file#trading-api-keys
<br>
https://alpaca.markets/sdks/python/trading.html