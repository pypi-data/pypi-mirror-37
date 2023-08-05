from django.utils.decorators import classproperty


class Members:
    # noinspection PyPep8Naming
    @classproperty
    def ALL(self):
        return tuple(
            v for k, v in self.__dict__.items()
            if not k.startswith('__') and isinstance(v, str)
        )

    # noinspection PyPep8Naming
    @classproperty
    def CHOICES(self):
        return (
            (choice, choice)
            for choice in self.ALL
        )
