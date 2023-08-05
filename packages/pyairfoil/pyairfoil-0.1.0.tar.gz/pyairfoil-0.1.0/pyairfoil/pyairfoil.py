# -*- coding: utf-8 -*-

"""Main module."""


AIRFOIL_TYPES = {}


class AirfoilBase:

    def __init__(self, **kwargs):
        # Register myself as an airfoil class type. Useful in the future when trying to re-load from a dictionary
        if self.__class__.__name__ not in AIRFOIL_TYPES.keys():
            print('Registering {} as new Airfoil Type'.format(self.__class__.__name__))
            AIRFOIL_TYPES[self.__class__.__name__] = self.__class__
        pass

    @property
    def type(self):
        return self.__class__.__name__

    def to_dict(self):
        return {
            'type': self.type
        }

    def __str__(self):
        return 'Airfoil ({})'.format(self.type)


class AirfoilPritchard(AirfoilBase):

    def __init__(self):
        super().__init__()
