import json
from functions import binance_parser, kucoin_parser

try:
    with open("tickers.txt", "r", encoding="utf-8") as tickers_file:
        tickers_list = tickers_file.readlines()
        tickers = [ticker.strip().upper() for ticker in tickers_list]
except FileNotFoundError:
    print('ОШИБКА: Не найден файл с тикерами (tickers.txt')

b_error = binance_parser(tickers)
k_error = kucoin_parser(tickers)
if b_error is None and k_error is None:
    try:
        with open("json/kucoin.json", "r", encoding="utf-8") as kucoin_json:
            kucoin_data = json.load(kucoin_json)
    except:
        iserror = 'Ошибка чтения JSON от Kucoin'
    try:
        with open("json/binance.json", "r", encoding="utf-8") as binance_json:
            binance_data = json.load(binance_json)
    except:
        iserror = 'Ошибка чтения JSON от Binance'

    ticker_counter = 0 # снова мои любимые переменные для подсчета. по-другому не придумал(
    price_dif_threshold = 0.0001 # хотел сделать отдельный файл settings.py, но не стал тк мало вводных настроек

    try:
        for b_ticker in binance_data:
            if b_ticker in kucoin_data:
                price_binance = float(binance_data[b_ticker])
                price_kucoin = float(kucoin_data[b_ticker])
                if price_binance >= price_kucoin:
                    price_dif = price_binance - price_kucoin
                else:
                    price_dif = price_kucoin - price_binance
                if (price_dif / price_binance) > price_dif_threshold:
                    print(f'{b_ticker}\n Разница: {round(price_dif,5)} ({round((price_dif / price_binance * 100),2)}%) \n Binance: {price_binance} \n Kucoin: {price_kucoin}\n ******')
                    ticker_counter += 1
            else:
                print(f'{b_ticker} пара не найдена на Kucoin')
        if ticker_counter == 0:
            print(f'Нет токенов со спредом больше чем {price_dif_threshold * 100}%')
    except:
        print(iserror)
else:
    if b_error is None:
        print(k_error)
    else:
        print(b_error)