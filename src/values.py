import json


def load_config():
    try:
        with open('../config/config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print('Config file not found! Using default config')
        config = {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "limit": 100
        }
        with open('../config/config.json', 'w') as file:
            json.dump(config, file, indent=4)

    return config


def save_config(config):
    with open('../config/config.json', 'w') as file:
        json.dump(config, file, indent=4)


def alter_param():
    config = load_config()
    try:
        print('What do you want to change?')
        print('1 - Symbol ' + config['symbol'])
        print('2 - Interval ' + config['interval'])
        print('3 - Limit ' + str(config['limit']))
        case = input()
        match case:
            case '1':
                config['symbol'] = input('Type a new symbol: ')
            case '2':
                config['interval'] = input('Type a new  interval: ')
            case '3':
                config['limit'] = int(input('Type a new  limit: '))
            case _:
                print('Invalid option!')
        print()
        save_config(config)
    except KeyboardInterrupt:
        print('\nClosing...')
        exit()


alter_param()
