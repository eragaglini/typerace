import os


# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {"ENV": os.environ.get("ENV", "DEVELOPMENT")}
    if config["ENV"] == "DEVELOPMENT":
        from .default_config import SECRET_KEY

        config["SECRET_KEY"] = SECRET_KEY
    else:
        config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        config["RAWG_TOKEN"] = os.environ.get("RAWG_TOKEN")
        config["DEBUG"] = config["ENV"].upper() != "PRODUCTION"

    config["TEMPLATES_AUTO_RELOAD"] = True
    config["SEVER_NAME"] = "0.0.0.0"
    config["PREFERRED_URL_SCHEME"] = "https"
    return config


config = load_config()
