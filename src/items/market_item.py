from scrapy import Item, Field


class MarketItem(Item):
    exchange_id = Field()
    symbol = Field()
    price = Field()
    quote_volume_24h = Field()
