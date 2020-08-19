from .builconfigurations import BuildConfiguration
from .app import Controller
from .orders import BuyOrder, SellOrder
import time
from random import randint


if __name__ == '__main__':
    # # TODO create a configuration file for initializing portfolio
    # configuration_obj = BuildConfiguration(database='postgresql')
    # controller = Controller(configuration_obj, 0.005, 0.03, 0.3)
    # controller.run()
    # print(controller.portfolio.capital)
    # print(controller.trader.max_buy_per_trade)
    # buy_buy_order = Buybuy_Order('NFLX', buy_price=10, quantity=10)
    # sell_buy_order = Sellbuy_Order('NFLX', sell_price=50, quantity=10)
    # print('Open trade')
    # controller.open_position(buy_order)
    # time.sleep(3)
    # print('Close trade')
    # if controller.get_active_trades():
    # controller.close_position(sell_order)
    # print(controller.portfolio.capital)
    # print(configuration_obj)

    configuration_obj = BuildConfiguration(database='postgresql')
    controller = Controller(configuration_obj, 0.005, 0.03, 0.3)
    controller.run()

    stocks = ['NFLX', 'SPY']
    while True:
        print()
        interface = input(
            'Digite la opción que desea ejecutar: 1 para compra, 2 para venta y 0 para salir \nDigite una opción: ')
        if interface == '1':
            try:
                buy_order = BuyOrder(stocks[0], buy_price=randint(1, 50), quantity=randint(1, 10))
                status, order_dict = controller.open_position(buy_order)
                if status:
                    # show information after the order execution
                    print('Trade successfully executed.')
                    print('Se ha ejecutato la orden con las siguientes características:')
                    for key in order_dict.keys():
                        print(' - ' + key + ': ', end='')
                        print(str(order_dict[key]))
                    print('\n')

            except Exception as e:
                print(e, ' - No se puede ejecutar la acción. Hubo un error durante el proceso - ', e.args)

        elif interface == '2':
            print()
            print(' - Cargando portafolio...')
            print('    Connecting to database...')
            print()
            open_trades, active_trades_list = controller.get_open_trades()
            if open_trades:
                print()
                print('Open trades:')
                for key, trade in enumerate(active_trades_list):
                    print(' - ' + str(key) + ': ', end='')
                    print(trade)
                print('\n\n')

                trade_id = int(input('Digite el ID de la orden que desea cerrar: '))
                trade_to_close = controller.get_open_trades_id(trade_id)

                sell_order = SellOrder(trade_to_close[0], sell_price=randint(1, 100), quantity=trade_to_close[1])
                order_status, order_dict = controller.close_position(sell_order, trade_id)
                print()

                if order_status:
                    # show information after the order execution
                    print('Trade successfully executed.')
                    print('Se ha ejecutato la orden con las siguientes características:')
                    for key in order_dict.keys():
                        print(' - ' + key + ': ', end='')
                        print(str(order_dict[key]))
                    print('\n\n')

                print()
                try:
                    print(' - Validando...')
                    query = dbController.selectQuery('openorders', '*', filter_table=str(id))
                    if query is None or query[0][OpenOrderElement.ticker.value] != order[CloseOrderElement.ticker.name]:
                        print('Hay un error en el query o en el id de la orden, por favor revise que el id sea el correcto')
                    elif query[0][OpenOrderElement.quantity.value] < order[CloseOrderElement.CloseCantidad.name]:
                        print('Esta intentando vender mas acciones de las posee. La operación no se ha llevado a cabo')
                    else:
                        print('    Resultado de la validación: OK...')
                        if trader.execute_order(order):
                            dbController.insert(order)
                            value = query[0][OpenOrderElement.quantity.value] - order[CloseOrderElement.CloseCantidad.name]
                            if value > 0:
                                print('    Nueva cantidad de acciones', value)
                                dbController.update_open_orders(str(id), value)
                                var = portafolio.actualizar_capital(order)
                                dbController.update_capital(order[CloseOrderElement.time_stamp.name], var)
                                print()
                                print('    Capital disponible (USD) : {}'.format(var))
                                print()
                            elif value == 0:
                                print('    Cerrar posición completamente', value)
                                dbController.update_open_orders(str(id), value, 'delete')
                                var = portafolio.actualizar_capital(order)
                                dbController.update_capital(order[OpenOrderElement.time_stamp.name], var)
                                print()
                                print('    Capital disponible (USD) : {}'.format(var))
                                print()

                        portafolio.print_portafolio(stocks)
                except Exception as e:
                    print(e, '- Error in main.py: {} method load_open_orders'.format(e.__traceback__.tb_lineno))
