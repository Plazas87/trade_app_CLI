import os
print(os.getcwd())
from .portfolio import Portafolio
from .trader import Trader
from .orders import OrderComponents
from random import randint
from configparser import ConfigParser


class Controller:
    def __init__(self, capital, max_lost_per_trade, max_lost_per_day, max_buy_per_trade):
        self.portfolio = Portafolio(capital)
        self.trader = Trader(max_lost_per_trade, max_lost_per_day, max_buy_per_trade)
        # self.dbController = DatabaseController()
        self.status = False
        print('Your trader ID para esta sesión is:', self.trader.id_trader)

    def run(self):
        self.status = True

    def check_user(self, user, pwrd):
        user_query = self.dbController.selectQuery('users', '*', filter_table=user)
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

    def open_long_position(self, buy_order):
        try:
            status, order_dict = self.trader.prepare_trade(buy_order)
            if status:
                if self.validate_buying_power(order_dict):
                    if self.trader.execute_order(order_dict):
                        print(f'Capital before execute the order: {self.portfolio.capital}')
                        self.portfolio.decrease_capital(order_dict[OrderComponents.cost.name])
                        print('Trade successfully executed.')
                        print(f'Capital before execute the order: {self.portfolio.capital}')

            else:
                print(f'The trade is not valid - STATUS: {status}')

        except Exception as e:
            pass

    def validate_buying_power(self, order):
        cost = order[OrderComponents.buy_price.name] * order[OrderComponents.quantity.name]
        if cost > 0.0:
            if cost <= (self.trader.max_buy_per_trade * self.portfolio.capital):
                return True

            else:
                return False
        else:
            return False

    # def open_position(self, open_order):
    #     try:
    #         order = open_order.order_to_dict()
    #         print()
    #         print('Se ha creado la orden con las siguientes características:')
    #         for key in order.keys():
    #             print(' - ' + key + ': ', end='')
    #             print(str(order[key]))
    #
    #         print()
    #         if self.portfolio.open_position(order):
    #             if self.trader.executeOrder(order):
    #                 self.dbController.insert(order)
    #                 # self.portafolio.print_portafolio(stocks)
    #                 var = self.portfolio.actualizar_capital(order)
    #                 if var is not None:
    #                     self.dbController.update_capital(order[OpenOrderElement.time_stamp.name], var)
    #                     print()
    #                     print('    Capital disponible (USD) : {}'.format(var))
    #                     print()
    #         else:
    #             pass
    #     except Exception as e:
    #         print(e, ' - No se puede ejecutar la acción. Hubo un error durante el proceso - ', e.args )

    # def close_position(self):
    #     print()
    #     print(' - Cargando portafolio...')
    #     print('    Connecting to the PostgreSQL database...')
    #     print()
    #     # portafolio.print_portafolio(stocks)
    #     print()
    #     id = int(input('Digite el ID de la orden que desea cerrar: '))
    #     ticker = input('Digite el ticker de la orden: ')
    #     close_order = SellOrder(ticker, id, OrderTypes.Venta.name, randint(1, 100), 5)
    #     order = close_order.order_to_dict()
    #     print()
    #     print('Se ha creado la orden con las siguientes características:')
    #     for key in order.keys():
    #         print(' - ' + key + ': ', end='')
    #         print(str(order[key]))
    #
    #     print()
    #     try:
    #         print(' - Validando...')
    #         query = self.dbController.selectQuery('openorders', '*', filter_table=str(id))
    #         if query is None or query[0][OpenOrderElement.ticker.value] != order[CloseOrderElement.ticker.name]:
    #             print('Hay un error en el query o en el id de la orden, por favor revise que el id sea el correcto')
    #         elif query[0][OpenOrderElement.quantity.value] < order[CloseOrderElement.CloseCantidad.name]:
    #             print('Esta intentando vender mas acciones de las posee. La operación no se ha llevado a cabo')
    #         else:
    #             print('    Resultado de la validación: OK...')
    #             if self.trader.execute_order(order):
    #                 self.dbController.insert(order)
    #                 value = query[0][OpenOrderElement.quantity.value] - order[CloseOrderElement.CloseCantidad.name]
    #                 if value > 0:
    #                     print('    Nueva cantidad de acciones', value)
    #                     self.dbController.update_open_orders(str(id), value)
    #                     var = self.portfolio.actualizar_capital(order)
    #                     self.dbController.update_capital(order[CloseOrderElement.time_stamp.name], var)
    #                     print()
    #                     print('    Capital disponible (USD) : {}'.format(var))
    #                     print()
    #                 elif value == 0:
    #                     print('    Cerrar posición completamente', value)
    #                     self.dbController.update_open_orders(str(id), value, 'delete')
    #                     var = self.portfolio.actualizar_capital(order)
    #                     self.dbController.update_capital(order[OpenOrderElement.time_stamp.name], var)
    #                     print()
    #                     print('    Capital disponible (USD) : {}'.format(var))
    #                     print()
    #
    #             # self.portafolio.print_portafolio(stocks)
    #     except Exception as e:
    #         print(e, '- Error in main.py: {} method load_open_orders'.format(e.__traceback__.tb_lineno))


if __name__ == '__main__':
    from .orders import BuyOrder
    controller = Controller(1000, 0.005, 0.03, 0.3)
    controller.run()
    print(controller.portfolio.capital)
    print(controller.trader.max_buy_per_trade)
    buy_order = BuyOrder('NFLX', buy_price=10, quantity=10)
    controller.open_long_position(buy_order)
    print(controller.portfolio.capital)

