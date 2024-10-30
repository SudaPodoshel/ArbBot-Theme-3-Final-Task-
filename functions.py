import requests
import json

errors_dict = {}
def error_checker():
    try:
        with open("json/errors.json", "r", encoding="utf-8") as errors_json:
            global errors_dict
            errors_dict = json.load(errors_json)
            return errors_dict
    except FileNotFoundError:
        errors_dict = "file not found"
        return errors_dict

def binance_parser(tickers):
    host = 'https://api.binance.com/api'
    prefix = '/v3/ticker/price'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    symbols = 'USDT","'.join(ticker for ticker in tickers)
    binance_data = requests.request('GET', host + prefix + '?symbols=["' + symbols + 'USDT"]', headers=headers)
    if binance_data.status_code == 200:
        binance_dict = {}
        binance_allTickers = binance_data.json()
        with open("json/binance.json", "w", encoding="utf-8") as binance_json:
            for ticker in tickers:
                for token in binance_allTickers:
                    symbol = token["symbol"]
                    price = token["price"]
                    if symbol == f"{ticker}USDT":
                        binance_dict[f'{ticker}USDT'] = price
            binance_json.write(json.dumps(binance_dict, indent=4))
    else:
        if error_checker() != "file not found":
            if str(binance_data.status_code) in errors_dict.keys():
                iserror = f"ОШИБКА ПАРСИНГА BINANCE: {binance_data.status_code} // {(errors_dict[str(binance_data.status_code)])}"
                return iserror
            else:
                iserror = f"ОШИБКА ПАРСИНГА BINANCE: {binance_data.status_code}"
                return iserror
        else:
            iserror = f"ОШИБКА ПАРСИНГА BINANCE: {binance_data.status_code} (+на найден справочник с ошибками. проверьте /json/errors.json)"
            return iserror

def kucoin_parser(tickers):
        host = 'https://api.kucoin.com'
        prefix = '/api/v1/market/allTickers'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        kucoin_data = requests.request('GET', host + prefix, headers=headers)
        kucoin_allTickers = kucoin_data.json()

        if kucoin_data.status_code == 200:
            kucoin_dict = {}
            with open("json/kucoin.json", "w", encoding="utf-8") as kucoin_json:
                for ticker in tickers:
                    for token in kucoin_allTickers["data"]["ticker"]:
                        symbol = token["symbol"]
                        price = token["last"]
                        if symbol == f"{ticker}-USDT":
                            kucoin_dict[f'{ticker}USDT'] = price
                kucoin_json.write(json.dumps(kucoin_dict, indent=4))
        else:
            if error_checker() != "file not found":
                if str(kucoin_data.status_code) in errors_dict.keys():
                    iserror = f"ОШИБКА ПАРСИНГА KUCOIN: {kucoin_data.status_code} // {(errors_dict[str(kucoin_data.status_code)])}"
                    return iserror
                else:
                    iserror = f"ОШИБКА ПАРСИНГА KUCOIN: {kucoin_data.status_code}"
                    return iserror
            else:
                iserror = f"ОШИБКА ПАРСИНГА KUCOIN: {kucoin_data.status_code} (+на найден справочник с ошибками. проверьте /json/errors.json)"
                return iserror