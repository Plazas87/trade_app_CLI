from enum import Enum


class OrderComponents(Enum):
    time_stamp = 0
    id = 1
    year = 2
    month = 3
    day = 4
    hour = 5
    minute = 6
    ticker = 7
    buy_price = 8
    sell_price = 9
    quantity = 10
    cost = 11
    order_type = 12
    trader_id = 13


class TradeComponents(Enum):
    trade_id = 0
    profit = 1
    result = 2
    status = 3


class TradeResults(Enum):
    positive = 'P'
    negative = 'N'
    waiting = 'W'


class TradeStatus(Enum):
    working = True
    closed = False


class OrderTypes(Enum):
    buy = 0
    sell = 1
    trade = 2
