import configparser


config = configparser.ConfigParser()
config.read("settings.ini")
api_id = int(config['telegram']['api_id'])
api_hash = config['telegram']['api_hash']
