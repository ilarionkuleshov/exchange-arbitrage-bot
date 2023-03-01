######################################
########## Project Settings ##########
######################################

import os

from dotenv import load_dotenv
from scrapy.utils.log import configure_logging
from scrapy.utils.reactor import install_reactor


load_dotenv()
install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

########## Scrapy Settings ###########

BOT_NAME = "exchange_arbitrage_bot"

SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"
COMMANDS_MODULE = "commands"

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

########### Other Settings ###########

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

DB_USERNAME = os.getenv("DB_USERNAME", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_DATABASE = os.getenv("DB_DATABASE", "")

MARKET_SYMBOL_SEPARATOR = "/"

MIN_PRICE_DIFFERENCE = float(os.getenv("MIN_PRICE_DIFFERENCE", "0.02"))
QUOTE_CURRENCY = os.getenv("QUOTE_CURRENCY", "usdt")
MIN_QUOTE_VOLUME_24H = int(os.getenv("MIN_QUOTE_VOLUME_24H", "50000"))

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")

configure_logging()
