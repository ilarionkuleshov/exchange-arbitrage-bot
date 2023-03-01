# Exchange Arbitrage Bot

## Installing
```
cd src/
poetry install
poetry run alembic upgrade head
poetry run scrapy exchange_initializer
```

## Usage
```
cd pm2/
pm2 start pm2.config.js
```