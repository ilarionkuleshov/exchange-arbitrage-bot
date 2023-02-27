######################################
########## Project Settings ##########
######################################

import os

from dotenv import load_dotenv
from scrapy.utils.log import configure_logging


load_dotenv()

########## Scrapy Settings ###########

BOT_NAME = "exchange_arbitrage_bot"

SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"
COMMANDS_MODULE = "commands"

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

########### Other Settings ###########

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

DB_USERNAME = os.getenv("DB_USERNAME", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_DATABASE = os.getenv("DB_DATABASE", "")

MARKET_SYMBOL_SEPARATOR = "/"

configure_logging()
