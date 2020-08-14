from .order import Order
from .order_components import OrderTypes


class SellOrder(Order):
    def __init__(self, ticker, sell_price, buy_price=0, quantity=0):
        Order.__init__(self, ticker, buy_price, sell_price, quantity)
        self._order_type = OrderTypes.sell.name

    @property
    def order_type(self):
        return self._order_type


if __name__ == '__main__':
    sell_order = SellOrder('NFLX', sell_price=10, quantity=10)
    print(sell_order)

