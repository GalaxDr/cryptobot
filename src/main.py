import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import time
import subprocess
import json
import apikeys


print('ccxt version: ', ccxt.__version__)
print('CryptoData v1.0')
print('Made by: GalaxDr')
time.sleep(3)
subprocess.run('cls', shell=True)

exchange = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': apikeys.apikey,
    'secret': apikeys.secret,
})


def load_config():
    print('Loading config.json')
    try:
        with open('../config/config.json', 'r') as arquivo:
            config = json.load(arquivo)
    except FileNotFoundError:
        print('config.json not found! Using default config!')
        config = {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "limit": 100
        }
    return config


def obtain_data():
    config = load_config()
    symbol = config['symbol']
    interval = config['interval']
    limit = config['limit']
    interval_list = []
    if interval[1] == 'm':
        interval_list = [int(interval[0]), 'minutes']
    elif interval[1] == 'h':
        interval_list = [int(interval[0]), 'hours']

    try:
        print('Obtaining price for: ' + symbol + ' in the last '
              + str(limit * interval_list[0]) + ' ' + interval_list[1] + '...')
        server_timestamp = exchange.fetch_time()
        local_timestamp = int(time.time() * 1000)
        timestamp = server_timestamp - (local_timestamp - int(server_timestamp))

        ohlcv = exchange.fetch_ohlcv(symbol, interval, limit=limit, params={'until': timestamp})
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['difference'] = df['close'] - df['open']
        df['difference'] = df['difference'].round(4)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert('America/Sao_Paulo')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print('Error obtaining data: ' + str(e))
        exit()


def desc_stats(df):
    print('Obtaining statistics data...')
    desc_stats1 = df.describe()
    print(desc_stats1)
    input('Press ENTER to continue')


def potential_profit(df):
    df['retorno_percentual'] = df['close'].pct_change() * 100
    df['retorno_percentual'] = df['retorno_percentual'].dropna()
    df['retorno_percentual'] = df['retorno_percentual'].round(4)
    df['retorno_percentual'].plot(figsize=(16, 8))
    plt.xlabel('Timestamp')
    plt.ylabel('Retorno Percentual')
    plt.show()


def moving_mean(df):
    df['media_movel'] = df['close'].rolling(window=10).mean()
    df[['close', 'media_movel']].plot(figsize=(16, 8))
    plt.show()


def closing_price(df):
    df['close'].plot(figsize=(16, 8))
    plt.show()


def return_histograms(df):
    df['retorno_percentual'] = df['close'].pct_change() * 100
    plt.hist(df['retorno_percentual'].dropna(), bins=30, alpha=0.75)
    plt.xlabel('Percentual Return')
    plt.ylabel('Frequency')
    plt.show()


def analise_data(df):
    while True:
        subprocess.run('cls', shell=True)
        print('O que você deseja fazer?')
        print('1 - Obter dados estatísticos')
        print('2 - Obter potencial de lucro')
        print('3 - Obter média móvel')
        print('4 - Obter preço de fechamento')
        print('5 - Obter histogramas de retorno')
        print('6 - Sair')
        opcao = int(input('Digite a opção desejada: '))
        match opcao:
            case 1:
                desc_stats(df)
            case 2:
                potential_profit(df)
            case 3:
                moving_mean(df)
            case 4:
                closing_price(df)
            case 5:
                return_histograms(df)
            case 6:
                exit()
            case _:
                print('Opção inválida!')
        print()


def main():
    df = obtain_data()
    df.to_csv('data/data.csv')
    analise_data(df)


if __name__ == '__main__':
    main()
