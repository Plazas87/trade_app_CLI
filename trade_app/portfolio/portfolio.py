from trade_app.orders import OrderComponents, TradeComponents, TradeStatus, TradeResults
from random import randint



class Portafolio:
    _portafolio = {}
    _portafolio_closed_orders = {}
    _capital = 0
    # dtQuery = DatabaseController()

    def __init__(self, initial_value):
        self._capital = int(initial_value) if int(initial_value) >= 0 else 0

    @property
    def portafolio(self):
        return self._portafolio

    @portafolio.setter
    def portafolio(self, executed_order):
        self.open_position(executed_order)

    @property
    def capital(self):
        return self._capital

    @capital.setter
    def capital(self, value):
        if isinstance(value, float) and value >= 0:
            self._capital = value

    def increase_capital(self, value):
        if isinstance(value, float):
            self.capital += value

    def decrease_capital(self, value):
        if isinstance(value, float) and value >= 0:
            tmp_capital = self.capital
            tmp_capital -= value
            if tmp_capital < 0:
                print('No tiene suficiente capital para realaizar la operación')

            else:
                self.capital = tmp_capital

    def calculate_profit(self, trade, sell_price):
        trade[OrderComponents.sell_price.name] = sell_price

        sell = sell_price * trade[OrderComponents.quantity.name]
        profit = sell - trade[OrderComponents.cost.name]

        trade[TradeComponents.profit.name] = profit

        return trade

    def update_status(self, trade, quantity):
        if trade[OrderComponents.quantity.name] == quantity:
            trade[TradeComponents.status.name] = TradeStatus.closed.value

        return trade

    def update_result(self, trade):
        if trade[TradeComponents.profit.name] >= 0:
            trade[TradeComponents.result.name] = TradeResults.positive.value

        else:
            trade[TradeComponents.result.name] = TradeResults.negative.value

        return trade


if __name__ == '__main__':
    stocks = ['NFLX', 'SPY']
    portafolio = Portafolio(750)
    print('Portafolio creado')
    for n in range(5):
        time.sleep(1)
        if randint(0, 1) == 0:
            order = Order(stocks[0], 100, randint(1, 100))
            order = order.order_to_dict()
            portafolio.open_position(order)
