class IntDescriptor:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        value = int(value)
        assert isinstance(value, int) \
               and value > -1
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        delattr(instance, self.name)


class StringDescriptor:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        assert isinstance(value, str) \
               and len(value.strip()) > 2
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        delattr(instance, self.name)