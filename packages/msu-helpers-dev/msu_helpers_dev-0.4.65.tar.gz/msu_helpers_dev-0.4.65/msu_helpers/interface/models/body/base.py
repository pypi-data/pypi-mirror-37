__all__ = ('BaseBodyModel',)


class BaseBodyModel:
    """BaseQueryModel request model, containing logic shared between other request models."""

    __int_fields__: tuple = tuple()
    __str_fields__: tuple = tuple()
    __bool_fields__: tuple = tuple()

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
        return f'{self.__dict__}'

    @property
    def attributes(self):
        return self.int + self.str + self.bool

    @classmethod
    def deserialize(cls, data: dict):
        model = cls()
        for attr in model.attributes:
            model.__setattr__(attr, data.get(attr, None))
        model.validate()
        return model
