from .portfolio import Portafolio
from .trader import Trader
from .orders import OrderComponents, OrderTypes, TradeComponents
from .models import DatabaseController
from .config import ConfigFileSection
import math
from random import randint
from configparser import ConfigParser


class Controller:
    def __init__(self, config_obj, max_lost_per_trade, max_lost_per_day, max_buy_per_trade):
        # Initializes database controller for session
        self._dbController = DatabaseController(config_obj[ConfigFileSection.postgresql.name])

        # initializes capital for session
        if self.validate_initial_capital():
            self.portfolio = Portafolio(config_obj[ConfigFileSection.portfolio.name], is_initial=True)
            self._set_capital(self.portfolio.capital)

        else:
            self.portfolio = Portafolio(self.get_capital())

        # Initializes trader for session
        self.trader = Trader(config_obj[ConfigFileSection.trader.name])

        self.status = False
        print('Your trader ID para esta sesión is:', self.trader.id_trader)

    def run(self):
        self.status = True

    def check_user(self, user, pwrd):
        user_query = self._dbController.selectQuery('users', '*', filter_table=user)
        return self._validate_user(user, pwrd, user_query)

    def _validate_user(self, user, pwrd, user_query):
        if user_query:
            user_query = user_query[0]
            if user in user_query:
                if pwrd in user_query:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def open_position(self, buy_order):
        try:
            # order_status = self.trader.prepare_order(buy_order)
            trade_status, trade_dict, order_dict = self.trader.prepare_trade(buy_order)

            if trade_status:
                if self.validate_buying_power(order_dict):
                    print(f'    Capital before execute the order (USD): {self.portfolio.capital}')

                    if self.trader.execute_order(order_dict):
                        self.update_capital(order_dict)

                        if self._dbController.open_trade(trade_dict):
                            self._dbController.save_order(order_dict)

                            print(f'    Available capital for trade (USD): {self.portfolio.capital}')

                            return True, order_dict

                else:
                    print('Not enough capital to trade')
                    print(f'    Available capital for trade (USD): {self.portfolio.capital}')

                    return False, []
            else:
                print(f'The trade is not valid - STATUS: {trade_status}')
                return False, []

        except Exception as e:
            print(e)
            return False, []

    def close_position(self, sell_order, trade_id):
        try:
            # order_ready, order_dict = self.trader.prepare_order(sell_order)
            orders_status, trade_dict, order_dict = self.trader.prepare_trade(sell_order, trade_id=trade_id)
            if orders_status:

                print(f'Capital before execute the close order: {self.portfolio.capital}')
                if self.trader.execute_order(order_dict):
                    self._dbController.save_order(order_dict)

                    status, trade_to_update = self._dbController.get_trade_by_id(trade_id)
                    if status:
                        trade_to_update = self.portfolio.calculate_profit(trade_to_update,
                                                                          sell_order.sell_price)

                        trade_to_update = self.portfolio.update_result(trade_to_update)
                        trade_to_update = self.portfolio.update_status(trade_to_update,
                                                                       sell_order.quantity)

                        self.update_capital(order_dict, trade_to_update)
                        self._dbController.update_trade_by_id(trade_to_update, trade_id)

                        print('Trade successfully executed.')
                        print(f'Capital after execute the close order: {self.portfolio.capital}')

                    return True, order_dict, trade_to_update[TradeComponents.profit.name]
            else:
                print(f'The trade is not valid - STATUS: {orders_status}')
                return False, []

        except Exception as e:
            print(e)
            return False, []

    def validate_buying_power(self, order):
        cost = order[OrderComponents.buy_price.name] * order[OrderComponents.quantity.name]
        if cost > 0.0:
            max_buy_per_trade = (self.trader.max_buy_per_trade * self.portfolio.capital)
            if cost <= max_buy_per_trade:
                return True

            else:
                return False
        else:
            return False

    # TODO: check if there is an open trade with a given ID
    def get_open_trades_ticker(self, ticker):
        trade_list = self._dbController.get_trades(ticker=ticker)
        if len(trade_list) == 0:
            return False, trade_list

        else:
            return True, trade_list

    def validate_initial_capital(self):
        is_initial = self._dbController.validate_initial_capital()

        if is_initial:
            return False
        else:
            return True

    def update_capital(self, order, trade=None):
        if order[OrderComponents.order_type.name] == OrderTypes.buy.name:
            self.portfolio.decrease_capital(order[OrderComponents.cost.name])
            self._set_capital(self.portfolio.capital)

        elif order[OrderComponents.order_type.name] == OrderTypes.sell.name:
            value = trade[TradeComponents.profit.name]
            self.portfolio.increase_capital(value)
            self._set_capital(self.portfolio.capital)

    def _set_capital(self, capital):
        return self._dbController.save_capital(capital)

    def get_capital(self):
        capital = self._dbController.get_capital()
        return capital

    def get_active_trades(self):
        self.get_open_trades_ticker()

    def get_open_trades_id(self, id):
        status, trade = self._dbController.get_order_by_id(id)
        if status:
            return True, trade

        else:
            False, trade


if __name__ == '__main__':
    from .orders import BuyOrder

    controller = Controller(1000, 0.005, 0.03, 0.3)
    controller.run()
    print(controller.portfolio.capital)
    print(controller.trader.max_buy_per_trade)
    buy_order = BuyOrder('NFLX', buy_price=10, quantity=10)
    controller.open_position(buy_order)
    print(controller.portfolio.capital)
