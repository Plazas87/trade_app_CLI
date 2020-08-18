from .builconfigurations import BuildConfiguration
from .app import Controller
from .orders import BuyOrder, SellOrder
import time
import os


if __name__ == '__main__':
    # TODO create a configuration file for initializing portfolio
    configuration_obj = BuildConfiguration(database='postgresql')
    controller = Controller(configuration_obj, 0.005, 0.03, 0.3)
    controller.run()
    print(controller.portfolio.capital)
    print(controller.trader.max_buy_per_trade)
    buy_order = BuyOrder('NFLX', buy_price=10, quantity=10)
    sell_order = SellOrder('NFLX', sell_price=12, quantity=10)
    print('Open trade')
    controller.open_position(buy_order)
    time.sleep(3)
    print('Close trade')
    controller.close_position(sell_order)
    print(controller.portfolio.capital)
    print(configuration_obj)



