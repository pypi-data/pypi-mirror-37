import re

__all__ = ('Base',)


class Base:
    """
    Base request model, containing logic shared between other request models.

    Every model attributed that can be passed in request should have name starts with 'p_'
    """

    regex: str = ""
    __int_fields__: tuple = tuple()
    __str_fields__: tuple = tuple()
    __bool_fields__: tuple = tuple()

    def __init__(self, value=''):
        param_match = re.match(self.regex, value)

        if param_match:
            self.parsed_data = param_match.groupdict()
        else:
            self.parsed_data = dict()

    @property
    def int(self) -> tuple:
        return self.__int_fields__

    @property
    def str(self) -> tuple:
        return self.__str_fields__

    @property
    def bool(self) -> tuple:
        return self.__bool_fields__

    def validate(self):
        for attr in self.int:
            if self.__getattribute__(attr) is None:
                self.__setattr__(attr, 0)

        for attr in self.str:
            if self.__getattribute__(attr) is None:
                self.__setattr__(attr, '')
                continue
            self.__setattr__(attr, self.__getattribute__(attr).strip())

        for attr in self.bool:
            if self.__getattribute__(attr) is None:
                self.__setattr__(attr, False)
                continue

            self.__setattr__(attr, bool(self.__getattribute__(attr)))

        return self

    def __str__(self) -> str:
        return f'{self.parsed_data}'

    def __getattr__(self, item):
        attr_list: tuple = self.int + self.str + self.bool
        if 'p_' + item in attr_list:
            return self.__getattribute__('p_' + item)

        raise AttributeError
