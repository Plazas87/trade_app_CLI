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



class OrderTypes(Enum):
    buy = 1
    sell = 2


if __name__ == '__main__':
    pass
