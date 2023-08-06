import os.path


class Domain(object):
    def __init__(self, macros):
        self.macros = os.path.basename(macros)
        self.macros_dir = os.path.abspath(os.path.dirname(macros))
        self.module = None

    def currentmodule(self, name):
        self.module = name
        self.language.module = name
        return ''

    def type(self, typ):
        return self.language.parse_type(typ)

    def return_type(self, typ):
        return self.type(typ)

    def parameter_type(self, typ):
        return self.type(typ)

    def type_description(self, typ):
        return self.type(typ)

    def value(self, value):
        if not hasattr(self.language, 'value_map'):
            return value
        return self.language.value_map.get(value, value)

    def default_value(self, value, typ):
        return self.language.parse_default_value(value, typ)

    def ref(self, obj):
        return self.shorten_ref(obj.fullname, obj)

    def shorten_ref(self, name, obj=None):  # pylint: disable=unused-argument
        name = name.split('.')
        if name[0] == self.module:
            del name[0]
        return '.'.join(name)

    def see(self, obj):
        raise NotImplementedError

    @staticmethod
    def paramref(name):
        return '*%s*' % name

    def code(self, value):
        return '``%s``' % self.value(value)

    @staticmethod
    def math(value):
        return ':math:`%s`' % value
