# from orders import Order, OpenOrderElement, CloseOrderElement, OrderTypes
from random import randint, random


class Portafolio:
    _portafolio = {}
    _portafolio_closed_orders = {}
    _capital = 0
    # dtQuery = DatabaseController()

    def __init__(self, initial_value):
        self._capital = initial_value if initial_value >= 0 else 0

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

    # metodo de la clase Portafolio
    # def open_position(self, executed_order=None):
    #     try:
    #         print(' - Validando...')
    #         print('    Connecting to the PostgreSQL database...')
    #         temp_var = self.dtQuery.selectQuery('capital', 'capital')
    #         print('    Capital disponible para ejecutar la orden (USD) : {}'.format(temp_var[0][0]))
    #         if temp_var[0][0] > 0:
    #             inv = executed_order[OpenOrderElement.buy_price.name] * executed_order[
    #                 OpenOrderElement.quantity.name]
    #             if temp_var[0][0] >= inv:
    #                 print('    - Resultado de la validación: la orden se puede ejecutar')
    #                 return True
    #             else:
    #                 print('    - Resultado de la validación: no dispone de capital para ejecutar la orden; no se ha enviado la orden')
    #                 return False
    #     except Exception as e:
    #         print(e, '- Error in portafolio.py: {} method open_positon'.format(e.__traceback__.tb_lineno))

    def increase_capital(self, value):
        if isinstance(value, float) and value >= 0:
            self.capital += value

    def decrease_capital(self, value):
        if isinstance(value, float) and value >= 0:
            tmp_capital = self.capital
            tmp_capital -= value
            if tmp_capital < 0:
                print('No tiene suficiente capital para realaizar la operación')

            else:
                self.capital = tmp_capital

    # def actualizar_capital(self, executed_order):
    #     try:
    #         capital = self.dtQuery.selectQuery('capital', '*')
    #         if executed_order[OpenOrderElement.order_type.name] == OrderTypes.Compra.name:
    #             inv = capital[0][2] - (
    #                     executed_order[OpenOrderElement.buy_price.name] * executed_order[OpenOrderElement.quantity.name])
    #             return inv
    #         elif executed_order[CloseOrderElement.order_type.name] == OrderTypes.Venta.name:
    #             inv = capital[0][2] + (
    #                     executed_order[CloseOrderElement.SellPrice.name] * executed_order[CloseOrderElement.CloseCantidad.name])
    #             return inv
    #
    #     except Exception as e:
    #         print(e, '- Error in portafolio.py: {} method actualizar_capital'.format(e.__traceback__.tb_lineno))
    #         return None

    # def print_portafolio(self, stocks): # agregar un vallidación para cuando la tabla de open orders este abierta
    #     try:
    #         print('Portafolio:')
    #         self._portafolio = {}
    #         for load_order in self.dtQuery.load_open_orders():
    #             keys = list(self._portafolio.keys())
    #             if load_order[OpenOrderElement.ticker.name] in keys:
    #                 self.portafolio[load_order[OpenOrderElement.ticker.name]].append(load_order)
    #             else:
    #                 self.portafolio[load_order[OpenOrderElement.ticker.name]] = []
    #                 self.portafolio[load_order[OpenOrderElement.ticker.name]].append(load_order)
    #
    #         for ticker in self.portafolio.keys():
    #             print('Open orders in {}'.format(ticker))
    #             for order_ in self.portafolio[ticker]:
    #                 print(order_)
    #     except Exception as e:
    #         print(e, '- Error in portafolio.py: {} method print_pottafolio'.format(e.__traceback__.tb_lineno))
    #         print('La orden que está buscando no se encuentra abierta, por favor revise el id de la orden')


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
