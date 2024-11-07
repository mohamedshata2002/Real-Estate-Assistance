from dotenv import dotenv_values

config = dotenv_values(".env")

lang_smith = config["lang_smith"]
google = config["google"]
voice =  config["voice"]