from datetime import datetime

import psycopg2 as db
from configparser import ConfigParser
from trade_app.orders import OrderComponents, OrderTypes
from trade_app.config import ConfigEnum


class DatabaseController:
    # Singleton implementation
    """Clase que controla la conexión a la base de datos. Esta clase ira creciendo hasta que sea completamente funcional
        y pueda ejecutar todos los comandos SQL"""
    def __init__(self, db):
        params = self._config()
        self.user = params[db][ConfigEnum.user.name]
        self._password = params[db][ConfigEnum.password.name]
        self.address = params[db][ConfigEnum.address.name]
        self.port = params[db][ConfigEnum.port.name]
        self.database = params[db][ConfigEnum.database.name]

    def __new__(cls, name=None, params=None):
        if not hasattr(cls, 'instance'):  # Si no existe el atributo “instance”
            cls.instance = super(DatabaseController, cls).__new__(cls)  # lo creamos
        return cls.instance

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
                query = "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor = conn.cursor()
                data = tuple(order.values())
                # error_row = []
                cursor.execute(query, data)
                # cursor.execute(query, (order[OrderComponents.id.name],
                #                        order[OrderComponents.time_stamp.name],
                #                        order[OrderComponents.year.name],
                #                        order[OrderComponents.month.name],
                #                        order[OrderComponents.day.name],
                #                        order[OrderComponents.hour.name],
                #                        order[OrderComponents.minute.name],
                #                        order[OrderComponents.ticker.name],
                #                        order[OrderComponents.buy_price.name],
                #                        order[OrderComponents.sell_price.name],
                #                        order[OrderComponents.quantity.name],
                #                        order[OrderComponents.order_type.name],
                #                        order[OrderComponents.trader_id.name],
                #                        order[OrderComponents.cost.name]))

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

    # def update_capital(self, time_stamp, value):
    #     try:
    #         conn = self.connect()
    #         with conn:
    #             cursor = conn.cursor()
    #             cursor.execute("INSERT INTO capital (timestamp, capital) VALUES (%s,%s)", (time_stamp, value))
    #     except sqlite3.IntegrityError as e:
    #         print(e, '- Error in model.py: {} method update_capital'.format(e.__traceback__.tb_lineno))

    # def update_open_orders(self, id_, value=0, operation='update'):
    #     """Esta función se encarga de actualizar los valores de la cantidad de acciones en el portadolio.
    #     Esta función debe llamarse siempre que se ejecute una orden de venta"""
    #     if operation == 'update':
    #         try:
    #             conn = self.connect()
    #             strquery = 'UPDATE openOrders SET cantidad= %s WHERE id= %s'
    #             values = (value, id_)
    #             with conn:
    #                 cursor = conn.cursor()
    #                 cursor.execute(strquery, values)
    #         except sqlite3.IntegrityError as e:
    #             print(e)
    #             print('No se puede modificar el capital en la base de datos')
    #
    #     elif operation == 'delete':
    #         try:
    #             conn = self.connect()
    #             strquery = 'DELETE FROM openOrders WHERE id= %s'
    #             values = (id_,)
    #             with conn:
    #                 cursor = conn.cursor()
    #                 cursor.execute(strquery, values)
    #                 # print('se ha elimiado la orden {} que estaba abierta'.format(id_))
    #         except sqlite3.IntegrityError as e:
    #             print(e)
    #             print('No se puede modificar el capital en la base de datos')

    def selectQuery(self, table_name, *columns, filter_table=None):
        """Este método se encarga de realizar las consultas a todas las tablas de la base de datos del proyecto. Es lo
        suficientemente versatil como para entender varios tipos de consultas a las diferentes tablas"""
        query = []
        cursor = ''
        conn = ''
        str_query = ''
        if table_name == 'buyorders' or table_name == 'sellorders' or table_name == 'openorders':
            if columns[0] == '*' and filter_table is None:
                str_query = 'SELECT * FROM {0}'.format(table_name)

            elif columns[0] != '*' and filter_table is None:
                selected_columns = ', '.join(columns)
                str_query = 'SELECT ' + selected_columns + ' FROM {0}'.format(table_name)

            elif columns[0] == '*' and filter_table is not None:
                str_query = "SELECT * FROM {0} WHERE id='{1}'".format(table_name, filter_table)

            elif columns[0] != '*' and filter_table is not None:
                selected_columns = ', '.join(columns)
                str_query = "SELECT " + selected_columns + " FROM {0} WHERE id='{1}'".format(table_name, filter_table)

        elif table_name == 'capital':
            if (columns[0] == '*' or columns[0] == 'capital') and filter_table is None and table_name == 'capital':
                str_query = 'SELECT {0} FROM {1} ORDER BY id_capital DESC'.format(columns[0], table_name)

        elif table_name == 'users':
            if columns[0] == '*' and filter_table is not None:
                str_query = "SELECT {0} FROM {1} WHERE usuario='{2}'".format(columns[0], table_name, filter_table)

        if str_query != '':
            try:
                conn = self.connect()
                if conn is not None:
                    cursor = conn.cursor()
                    cursor.execute(str_query)
                    query = cursor.fetchall()
            except Exception as e:
                print(e)
                cursor.close()
                self.close_connection(conn)
                print("PostgreSQL connection has been closed but an Exception has been raised")
                return None
            else:
                cursor.close()
                self.close_connection(conn)
                print("PostgreSQL connection is closed")
                return query

        else:
            return None

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

    def __query_to_dict(self, query):
        """Esta función se encarga de transformar los objetos producidos por la clase order en diccionarios. Esta función
        es opcional; su uso node siempre se requiere"""
        lst = []
        for row in query:
            dict_order = {OrderComponents.time_stamp.name: row[OrderComponents.time_stamp.value],
                          OrderComponents.id.name: row[OrderComponents.id.value],
                          OrderComponents.ticker.name: row[OrderComponents.ticker.value],
                          OrderComponents.order_type.name: row[OrderComponents.order_type.value],
                          OrderComponents.buy_price.name: row[OrderComponents.buy_price.value],
                          OrderComponents.quantity.name: row[OrderComponents.quantity.value]}
            lst.append(dict_order)
        return lst

    def _config(self, filename='./trade_app/config/configpostgres.ini', section='postgresql'):
        """Configura los parámetros para la conexión con la base de datos a través de la lectura de un
                archivo de configuración de extención .ini"""
        conf = ConfigParser()
        try:
            conf.read(filename)
            config_file_dict = {}
            tmp = {}
            for sect in conf.sections():
                params = conf.items(sect)
                for param in params:
                    tmp[param[0]] = param[1]

                config_file_dict[sect] = tmp
                tmp = {}

            return config_file_dict

        except Exception as e:
            print(e)

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

    def validate_inital_capital(self):
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
