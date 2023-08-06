__version__ = '0.1.0'

class KeyedClassMeta(type):
    _KeyedClassMeta__instances = {}
    def __call__(cls, key, *args, **kwargs):
        return KeyedClassMeta.__instances.setdefault(
            (cls, key),
            super().__call__(key, *args, **kwargs)
        )

class KeyedClass:
    _KeyedClass__instances = {}
    def __new__(cls, key):
        return KeyedClass.__instances.setdefault(
            (cls, key),
            super().__new__(cls)
        )
