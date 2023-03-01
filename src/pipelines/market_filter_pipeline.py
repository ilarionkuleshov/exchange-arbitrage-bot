from scrapy import Spider, Item
from scrapy.exceptions import DropItem

from interfaces import MarketSymbol


class MarketFilterPipeline:
    quote_currency: str
    min_quote_volume_24h: int

    def open_spider(self, spider: Spider) -> None:
        if not hasattr(spider, "session_settings"):
            raise Exception("Spider must have a `session_settings` attribute")
        settings = spider.session_settings
        self.quote_currency = MarketSymbol("", settings.quote_currency).quote_currency
        self.min_quote_volume_24h = settings.min_quote_volume_24h

    def process_item(self, item: Item, spider: Spider) -> Item:
        if (
            MarketSymbol.from_str(item["symbol"]).quote_currency != self.quote_currency
            or item["quote_volume_24h"] < self.min_quote_volume_24h
        ):
            raise DropItem("Market does not meet the requirements")
        else:
            return item
