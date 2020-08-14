from ..orders import OrderComponents, OrderTypes
from random import randint
from datetime import datetime
from ..custom_exceptions import CreateOrderException


class Trader:

    def __init__(self, max_lost_per_trade, max_lost_per_day, max_buy_per_trade):
        self.platform_confirmation = False
        self.id_trader = Trader.generate_id()
        self.max_lost_per_trade = max_lost_per_trade
        self.max_lost_per_day = max_lost_per_day
        self.max_buy_per_trade = max_buy_per_trade

    def prepare_trade(self, buy_order):
        try:
            order = self.order_to_dict(buy_order)
            order['trader_id'] = self.id_trader
            cost = order[OrderComponents.buy_price.name] * order[OrderComponents.quantity.name]
            order['cost'] = cost

            return True, order

        except Exception as e:
            print(e, "Can't create the order: ", e.args)
            return False, 0

            # if self.portafolio.open_position(order):
            #     if self.trader.executeOrder(order):
            #         self.dbController.insert(order)
            #         # self.portafolio.print_portafolio(stocks)
            #         var = self.portafolio.actualizar_capital(order)
            #         if var is not None:
            #             self.dbController.update_capital(order[OpenOrderElement.time_stamp.name], var)
            #             print()
            #             print('    Capital disponible (USD) : {}'.format(var))
            #             print()
            # else:
            #     pass

    def execute_order(self, order_dict):
        if order_dict[OrderComponents.order_type.name] == OrderTypes.buy.name:
            try:
                print('    La orden de compra número {0} de {1} ha sido enviada a TOS'.format(order_dict[OrderComponents.id.name],
                                                                                              order_dict[OrderComponents.ticker.name]))

                self.platform_confirmation = True
                return self.platform_confirmation

            except Exception as e:
                print(e, '- Error in trader.py: {} method executeOrder'.format(e.__traceback__.tb_lineno))
                return False

        elif order_dict[OrderComponents.order_type.name] == OrderComponents.sell.name:
            try:
                print('    La orden de venta número {0} de {1} ha sido enviada a TOS'.format(order_dict[OrderComponents.id.name],
                                                                                             order_dict[OrderComponents.ticker.name]))
                # enviar llamada a la plataforma de TOS
                return True
            except Exception as e:
                print(e, '- Error in trader.py: {} method executeOrder'.format(e.__traceback__.tb_lineno))
                return False

    #
    #     elif order[CloseOrderElement.order_type.name] == OrderTypes.Venta.name:
    #         try:
    #             print('    La orden de venta número {0} de {1} ha sido enviada a TOS'.format(order[CloseOrderElement.id.name],
    #                                                                                          order[CloseOrderElement.ticker.name]))
    #             # enviar llamada a la plataforma de TOS
    #             return True
    #         except Exception as e:
    #             print(e, '- Error in trader.py: {} method executeOrder'.format(e.__traceback__.tb_lineno))
    #             return False
    #
    #     else:
    #         print('No se ha podido enviar la orden a TOS')
    #         return False

    @staticmethod
    def generate_id():
        return str(datetime.now().day) + str(datetime.now().month) + str(datetime.now().year) + str(randint(1, 10000))

    @staticmethod
    def order_to_dict(order):
        order_dict = {OrderComponents.id.name: order.id,
                      OrderComponents.time_stamp.name: order.timestamp,
                      OrderComponents.year.name: order.year,
                      OrderComponents.month.name: order.month,
                      OrderComponents.day.name: order.day,
                      OrderComponents.hour.name: order.hour,
                      OrderComponents.minute.name: order.minute,
                      OrderComponents.ticker.name: order.ticker,
                      OrderComponents.buy_price.name: order.buy_price,
                      OrderComponents.sell_price.name: order.sell_price,
                      OrderComponents.quantity.name: order.quantity,
                      OrderComponents.order_type.name: order.order_type}
        return order_dict

    @staticmethod
    def print_order(order):
        for key, value in order.items():
            print(f'{key}: {value}')

    # def validate_buying_power(self, cost):
    #     if cost > 0:
    #         if cost > self.max_buy_per_trade:
    #             return False
    #
    #         else:
    #             return True
    #
    #     else:
    #         return False


if __name__ == '__main__':
    buy_order = BuyOrder('NFLX', buy_price=10, quantity=3)
    portfolio = Portafolio(1000)
    trader = Trader(0.005, 0.03, 0.03, portfolio.capital)
    trader.prepare_trade(buy_order)
