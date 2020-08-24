from datetime import datetime

import psycopg2 as db
from configparser import ConfigParser
from trade_app.orders import OrderComponents, OrderTypes, TradeComponents
from trade_app.config import DataBaseConnection


class DatabaseController:
    # Singleton implementation
    """Clase que controla la conexión a la base de datos. Esta clase ira creciendo hasta que sea completamente funcional
        y pueda ejecutar todos los comandos SQL"""

    def __init__(self, db_config_obj):
        self._user = db_config_obj[DataBaseConnection.user.name]
        self._password = db_config_obj[DataBaseConnection.password.name]
        self._address = db_config_obj[DataBaseConnection.address.name]
        self._port = db_config_obj[DataBaseConnection.port.name]
        self._database = db_config_obj[DataBaseConnection.database.name]

    def __new__(cls, name=None, params=None):
        if not hasattr(cls, 'instance'):  # Si no existe el atributo “instance”
            cls.instance = super(DatabaseController, cls).__new__(cls)  # lo creamos
        return cls.instance

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if isinstance(value, str):
            self._user = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if isinstance(value, str):
            self._address = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if isinstance(value, int):
            self._port = value

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        if isinstance(value, str):
            self._database = value

    def connect(self, process_information='put some here'):
        try:
            # connect to the PostgreSQL server
            conn = None
            conn = db.connect(user=self.user,
                              password=self._password,
                              host=self.address,
                              port=self.port,
                              database=self.database)
            return conn
        except Exception as e:
            # logging.error('Unable to connect' + str(e))
            return None

    def close_connection(self, connection):
        """Termina la conexión con la base de datos. Esta función de ser llamada siempre despues de cualquier
        operación en la base de datos"""
        try:
            connection.close()
        except Exception as e:
            print('Unable to close the connection -', e, ': ', e.__traceback__.tb_frame)
            return None

    def save_order(self, order, info=None):
        conn = self.connect(process_information=info)
        if conn is not None:
            try:
                query = "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor = conn.cursor()
                data = tuple(order.values())
                cursor.execute(query, data)

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)
                return False
            else:
                conn.commit()
                cursor.close()
                self.close_connection(conn)
            return True

    def load_open_orders(self):
        """Este método se encarga de poner en memoria las ordenes abiertas en el portafokio de modo que el usuario pueda
        verlas en la pantalla cada vez que vaya a abrir o cerrar una orden"""
        conn = self.connect()
        strquery = 'SELECT * FROM openorders'
        with conn:
            cur = conn.cursor()
            try:
                cur.execute(strquery)
                query = cur.fetchall()
                dict_query = self.__query_to_dict(query)
                return dict_query
            except Exception as e:
                print(e, '- Error in model.py: {} method load_open_orders'.format(e.__traceback__.tb_lineno))
                return None

    def save_capital(self, capital, info=None):
        conn = self.connect(process_information=info)
        if conn is not None:
            try:
                query = "INSERT INTO capital (timestamp, capital) VALUES (%s, %s)"
                cursor = conn.cursor()
                data = (datetime.now(), capital)
                cursor.execute(query, data)

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)
                return False
            else:
                conn.commit()
                cursor.close()
                self.close_connection(conn)
            return True

    def get_capital(self):
        conn = self.connect()
        if conn is not None:
            try:
                query = "SELECT capital FROM capital ORDER BY timestamp DESC LIMIT 1"
                cursor = conn.cursor()
                cursor.execute(query)
                data_query = cursor.fetchall()[0][0]

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)

            else:
                cursor.close()
                self.close_connection(conn)
            return data_query

    def validate_initial_capital(self):
        conn = self.connect()
        if conn is not None:
            try:
                query = "SELECT count(capital) FROM capital"
                cursor = conn.cursor()
                cursor.execute(query)
                data_query = cursor.fetchall()[0][0]

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)

            else:
                cursor.close()
                self.close_connection(conn)
            return data_query

    def open_trade(self, trade_dict):
        conn = self.connect()
        if conn is not None:
            try:
                query = "INSERT INTO openorders VALUES" \
                        " (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor = conn.cursor()
                data = tuple(trade_dict.values())
                cursor.execute(query, data)

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)
                return False
            else:
                conn.commit()
                cursor.close()
                self.close_connection(conn)
            return True

    def get_trades(self, ticker):
        conn = self.connect()
        if conn is not None:
            try:
                query = "SELECT ticker, buy_price, quantity, " \
                        "time_stamp, order_id, status, result " \
                        "FROM openorders " \
                        "WHERE ticker = (%s) AND status = true " \
                        "ORDER BY time_stamp DESC"

                data = (ticker,)
                cursor = conn.cursor()
                cursor.execute(query, data)
                data_query = cursor.fetchall()

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)

            else:
                cursor.close()
                self.close_connection(conn)
            return data_query

    def get_order_by_id(self, id):
        conn = self.connect()
        if conn is not None:
            try:
                query = "SELECT ticker, quantity, trade_id FROM openorders WHERE order_id = (%s)"
                data = (id,)
                cursor = conn.cursor()
                cursor.execute(query, data)
                data_query = cursor.fetchall()[0]

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)
                return False, []

            else:
                cursor.close()
                self.close_connection(conn)
            return True, data_query

    def get_trade_by_id(self, id):
        conn = self.connect()
        if conn is not None:
            try:
                query = "SELECT cost, sell_price, quantity FROM openorders WHERE trade_id = (%s) " \
                        "AND status = true"
                data = (id,)
                cursor = conn.cursor()
                cursor.execute(query, data)
                data_query = cursor.fetchall()[0]
                data_query = {OrderComponents.cost.name: data_query[0],
                              OrderComponents.sell_price.name: data_query[1],
                              OrderComponents.quantity.name: data_query[2]}

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)
                return False, {}

            else:
                cursor.close()
                self.close_connection(conn)
            return True, data_query

    def update_trade_by_id(self, trade_to_update, trade_id):
        conn = self.connect()
        if conn is not None:
            try:
                query = "UPDATE openorders SET sell_price = %s, profit = %s, result = %s, status = %s " \
                        "WHERE trade_id = %s;"
                data = (trade_to_update[OrderComponents.sell_price.name],
                        trade_to_update[TradeComponents.profit.name],
                        trade_to_update[TradeComponents.result.name],
                        trade_to_update[TradeComponents.status.name],
                        trade_id)
                cursor = conn.cursor()
                cursor.execute(query, data)

            except Exception as e:
                # logging.error(
                #     'Error: PostgreSQL connection has been closed but an Exception has been raised - {0}'.format(e))
                print(e)
                cursor.close()
                self.close_connection(conn)
                return False

            else:
                conn.commit()
                cursor.close()
                self.close_connection(conn)

            return True


if __name__ == '__main__':
    query = DatabaseController('postgresql')
    var = query.selectQuery('users', '*', filter_table='acpr87@gmail.com')
    if var:
        print(type(var))
        print('True')
    else:
        print(False)
    print(var)
    print(query)
