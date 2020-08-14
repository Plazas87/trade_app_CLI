from .app import Controller
from .orders import BuyOrder
import os


if __name__ == '__main__':
    # TODO create a configuration file for initializing portfolio
    controller = Controller(1000, 0.005, 0.03, 0.3)
    controller.run()
    print(controller.portfolio.capital)
    print(controller.trader.max_buy_per_trade)
    buy_order = BuyOrder('NFLX', buy_price=10, quantity=10)
    controller.open_long_position(buy_order)
    print(controller.portfolio.capital)



