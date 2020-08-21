from enum import Enum


class ConfigFileSection(Enum):
    postgresql = 'postgresql'
    portfolio = 'portfolio'
    trader = 'trader'
