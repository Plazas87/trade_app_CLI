#! usr/bin/env python3

from configparser import ConfigParser
import logging
from trade_app.config import ConfigEnum


class BuildConfiguration:
    """Esta clase se encarga de leer el archivo de configuración genral, las parametros leidos son almacenados como
    propiedades del objeto que sera luego instanciado en la clase controller"""
    def __init__(self, database='postgresql'):
        # logging.info("Built main configuration object")
        param = self._config()
        self.user = param[database][ConfigEnum.user.name]
        self._password = param[database][ConfigEnum.password.name]
        self.address = param[database][ConfigEnum.address.name]
        self.port = param[database][ConfigEnum.port.name]
        self.database = param[database][ConfigEnum.database.name]

        # Built configuration for capital
        self.initial_capital = param['portfolio']['initial_capital']
        # TODO:

    @staticmethod
    def _config(filename='./trade_app/config/configpostgres.ini', specific_section=None):
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

    def __str__(self):
        return f'User: {self.user} - ' \
               f'Password: {self._password} - ' \
               f'Address: {self.address} - ' \
               f'Port: {self.port} - ' \
               f'Database connection: {self.database}'


if __name__ == '__main__':
    c = BuildConfiguration()
    print(c)


