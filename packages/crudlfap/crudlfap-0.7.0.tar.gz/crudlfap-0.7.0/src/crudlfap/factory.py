"""
**CRIMINALLY INVASIVE HACKS** in :py:class:`Factory`.
"""
import inspect


class FactoryMetaclass(type):
    """``__getattr__`` that ensures a first argument to getters."""

    def __getattr__(cls, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}'.format(attr[4:], attr))

        getter = getattr(cls, 'get_' + attr)

        if inspect.ismethod(getter):
            return getter()
        else:
            return getter(cls)

    def get_cls(cls):
        return cls  # did it go to far at this point ?


class Factory(metaclass=FactoryMetaclass):
    """Adds clumsy but automatic getter resolving.

    The `__getattr__` override makes this class try to call a get_*() method
    for variables that are not in `self.__dict__`.

    For example, when `self.foo` is evaluated `and 'foo' not in self.__dict__`
    then it will call the `self.get_foo()`

    If `self.get_foo()` returns None, it will try to get the result again from
    `self.__dict__`. Which means that we are going to witness this horrroorr::

        class YourEvil(Factory):
            def get_foo(self):
                self.calls += 1
                self.foo = 13

        assert YourEvil.foo == 13   # crime scene 1
        assert YourEvil.foo == 13   # crime scene 2
        assert YourEvil.calls == 1  # crime scene 3

    For the moment it is pretty clumsy because i tried to contain the
    criminality rate as low as possible meanwhile i like the work it does for
    me !
    """
    def __getattr__(self, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}()'.format(attr[4:], attr))

        getter = getattr(self, 'get_{}'.format(attr), None)

        if getter:
            methresult = getter()
            dictresult = self.__dict__.get(attr, None)
            if methresult is None and dictresult is not None:
                result = dictresult
            else:
                result = methresult
            return result

        # Try class methods
        return getattr(type(self), attr)

    @classmethod
    def clone(cls, **attributes):
        """Return a subclass with the given attributes.

        If a model is found, it will prefix the class name with the model.
        """
        name = cls.__name__
        model = attributes.get('model', getattr(cls, 'model', None))
        if model is None:
            model = getattr(cls, 'model', None)
        if model and model.__name__ not in cls.__name__:
            name = '{}{}'.format(model.__name__, cls.__name__)
        return type(name, (cls,), attributes)
