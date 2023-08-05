from rada_package_moiseieiva.descriptors import IntDescriptor, StringDescriptor


class MetaDescriptors(type):
    def __new__(cls, clsname, bases, dct):
        new_dict = {}
        for name, value in dct.items():
            if name == 'int_types':
                for x in value:
                    new_dict[x] = IntDescriptor()
            elif name == 'str_types':
                for x in value:
                    new_dict[x] = StringDescriptor()
            else:
                new_dict[name] = value
        return type.__new__(cls, clsname, bases, new_dict)