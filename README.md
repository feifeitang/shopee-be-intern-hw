# Market Size Calculator

## Goals
- Discover which market demand has a high frequency and is enough to support the operation of the product line
- Identify which market is almost saturated and not suitable for investing money

## Data source
- Collect data from shopee.tw through web crawler
- Fetch item & shop data like itemid, shopid, item price etc.

## Data storage
![](https://i.imgur.com/ZuDW82U.png)

## System architecture
1. client input keyword
2. server check keyword info
    - if keyword exist and its create_time < 1 month, get clusters' gross income of the keyword from database
    - if keyword dose not exist or its create_time >= 1 month, do crawler again then calculate market size
        - use Celery to run long running crawler task
3. server send result to client with LINE Notify

## Script to run
- activate virtual environment: ```make venv-activate```
- freeze dependencies: ```make freeze-reqs```
- install packages ```install-pkgs```
- run Celery worker server: ```make start-worker```
- run Flask application: ```make dev```