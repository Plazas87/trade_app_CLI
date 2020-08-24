from .builconfigurations import BuildConfiguration
from .app import Controller
from .orders import BuyOrder, SellOrder
from random import randint


if __name__ == '__main__':
    configuration_obj = BuildConfiguration()
    controller = Controller(configuration_obj.config_obj, 0.005, 0.03, 0.3)
    controller.run()

    stocks = ['NFLX', 'SPY']
    while True:
        print()
        interface = input(
            'Digite la opción que desea ejecutar: 1 para compra, 2 para venta y 0 para salir \nDigite una opción: ')
        if interface == '1':
            try:
                buy_order = BuyOrder(stocks[0], buy_price=randint(1, 40), quantity=randint(1, 10))
                print(f'Order cost: {buy_order.buy_price * buy_order.quantity}')
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
            ticker = input('Digite el ticker de la posición que quiere cerrar: ')
            open_trades, active_trades_list = controller.get_open_trades_ticker(ticker)
            if open_trades:
                print()
                print('Open trades:')
                for key, trade in enumerate(active_trades_list):
                    print(' - ' + str(key) + ': ', end='')
                    print(trade)
                print('\n')

                trade_id = int(input('Digite el ID de la orden que desea cerrar: '))
                status, trade_to_close = controller.get_open_trades_id(trade_id)

                if status:
                    sell_order = SellOrder(trade_to_close[0], sell_price=randint(20, 100), quantity=trade_to_close[1])
                    order_status, order_dict, profit = controller.close_position(sell_order, trade_to_close[2])
                    print()

                else:
                    print('Wrong ID')

                if order_status:
                    # show information after the order execution
                    print('Trade successfully executed.')
                    print(f'Profit: {profit}')
                    print('Se ha ejecutato la orden con las siguientes características:')
                    for key in order_dict.keys():
                        print(' - ' + key + ': ', end='')
                        print(str(order_dict[key]))
