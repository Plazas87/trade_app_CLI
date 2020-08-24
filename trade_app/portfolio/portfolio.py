from trade_app.orders import OrderComponents, TradeComponents, TradeStatus, TradeResults
from trade_app.config.config_portfolio import ConfigPortfolio


class Portafolio:
    # _portafolio = {}
    # _portafolio_closed_orders = {}
    # _capital = 0
    # # dtQuery = DatabaseController()

    def __init__(self, config_obj, is_initial=False):

        if is_initial:
            self._capital = int(config_obj[ConfigPortfolio.initial_capital.name]) if int(
                config_obj[ConfigPortfolio.initial_capital.name]) >= 0 else 0.0

        else:
            self._capital = config_obj

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

    # TODO: This method needs to change ir order to enable partial close orders
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
    pass
