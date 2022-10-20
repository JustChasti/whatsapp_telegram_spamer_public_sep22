import configparser


config = configparser.ConfigParser()
config.read("settings.ini")
finding_delay = int(config['whatsapp']['finding_delay'])
login_delay = int(config['whatsapp']['login_delay'])
