from .portfolio import Portafolio
from .trader import Trader
from .orders import OrderComponents, OrderTypes
from .models import DatabaseController
from random import randint
from configparser import ConfigParser


class Controller:
    def __init__(self, config_obj, max_lost_per_trade, max_lost_per_day, max_buy_per_trade):
        # Initializes database controller for session
        self._dbController = DatabaseController('postgresql')

        # initializes capital for session
        if self.validate_initial_capital():
            self.portfolio = Portafolio(config_obj.initial_capital)
            self.set_capital(config_obj.initial_capital)

        else:
            self.portfolio = Portafolio(self.get_capital())

        # Initializes trader for session
        self.trader = Trader(max_lost_per_trade, max_lost_per_day, max_buy_per_trade)

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
            order_status, order_dict = self.trader.prepare_order(buy_order)
            trade_status, trade_dict = self.trader.prepare_trade(buy_order)
            if order_status and trade_status:
                if self.validate_buying_power(order_dict):
                    print(f'    Capital before execute the order (USD): {self.portfolio.capital}')

                    if self.trader.execute_order(order_dict):
                        self.update_capital(order_dict)

                        if self._dbController.save_order(order_dict):
                            self._dbController.open_trade(trade_dict)

                            print(f'    Available capital for trade (USD): {self.portfolio.capital}')

                            return True, order_dict

                else:
                    print('Not enough capital to trade')
                    return False, []
            else:
                print(f'The trade is not valid - STATUS: {order_status == trade_status}')
                return False, []

        except Exception as e:
            print(e)
            return False, []

    def close_position(self, sell_order, trade_id):
        open_trades, trade_list = self.get_open_trades()

        if open_trades:
            try:
                order_ready, order_dict = self.trader.prepare_order(sell_order)
                if order_ready:
                    # open_trades, trade_list = self.get_open_trades(order_dict)
                    # if open_trades:
                    #     for index, trade in enumerate(trade_list):
                    #         print(f'{index}. {trade}')

                    print(f'Capital before execute the close order: {self.portfolio.capital}')
                    if self.trader.execute_order(order_dict):
                        # TODO: revisar como actualizar el capital y como actualizar el trade en la tabla opentrades
                        self._dbController.save_order(order_dict)
                        self.trader.update_trade_to_close()
                        self.update_capital(order_dict)
                        self._dbController.update_trade_by_id(order_dict, trade_id)

                        print('Trade successfully executed.')
                        print(f'Capital after execute the close order: {self.portfolio.capital}')

                        return True, order_dict
                else:
                    print(f'The trade is not valid - STATUS: {order_ready}')
                    return False, []

            except Exception as e:
                return False, []

        else:
            print('There is no open trades to close')
            return False, []

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

    # TODO: check if there is an open trade with a given ID
    def get_open_trades(self):
        trade_list = self._dbController.get_trades()
        if len(trade_list) == 0:
            return False, trade_list

        else:
            return True, trade_list

    def validate_initial_capital(self):
        is_initial = self._dbController.validate_inital_capital()

        if is_initial:
            return False
        else:
            return True

    def update_capital(self, order):
        if order[OrderComponents.order_type.name] == OrderTypes.buy.name:
            self.portfolio.decrease_capital(order[OrderComponents.cost.name])
            self.set_capital(self.portfolio.capital)

        elif order[OrderComponents.order_type.name] == OrderTypes.sell.name:
            self.portfolio.increase_capital(order[OrderComponents.cost.name])
            self.set_capital(self.portfolio.capital)

    def set_capital(self, capital):
        return self._dbController.save_capital(capital)

    def get_capital(self):
        capital = self._dbController.get_capital()
        return capital

    def get_active_trades(self):
        self.get_open_trades()

    def get_open_trades_id(self, id):
        trade = self._dbController.get_trade_by_id(id)
        return trade


if __name__ == '__main__':
    from .orders import BuyOrder

    controller = Controller(1000, 0.005, 0.03, 0.3)
    controller.run()
    print(controller.portfolio.capital)
    print(controller.trader.max_buy_per_trade)
    buy_order = BuyOrder('NFLX', buy_price=10, quantity=10)
    controller.open_position(buy_order)
    print(controller.portfolio.capital)
