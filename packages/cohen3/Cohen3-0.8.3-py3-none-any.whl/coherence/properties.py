"""
Implement a kind of observer pattern for lists and dictionaries.

The ListProperty and DictProperty classes allow to track any change occurred
in his data and trigger a external callback.

Examples
--------
Simple example of a ListProperty and DictProperty usage::

    class House(object):
        def __init__(self):
            self.people = ListProperty([])
            self.location = DictProperty({})
            print("House is ready to receive people.")

        def someone_arrived(self, who, where):
            print(who + " has arrived!")
            self.people.append(who)
            self.location[who] = where

        def someone_leaves(self, who):
            print(who + " has left!")
            self.people.remove(who)
            if who in self.location:
                del self.location[who]

        def someone_moves(self, who, where):
            print(who + " has moved to " + where)
            self.location[who] = where

    def print_total_people(d):
        print('The House has {} people inside'.format(len(d)))

    def print_where_are(d):
        print('where are the people:')
        for k, v in d.items():
            print('\t-> {} is inside {}'.format(k, v))
    r = House()
    r.people.bind(data=print_total_people)
    r.location.bind(data=print_where_are)
    r.someone_arrived('Marta', 'living room')
    r.someone_arrived('John', 'kitchen')
    r.someone_moves('John', 'living room')
    r.someone_leaves('John')
"""
from collections import UserList, UserDict


class Event:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


class Observable:
    def __init__(self):
        self.observers = set()
        self._binds = {}

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.add(observer)

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def emmit(self, name, **kwargs):
        event = Event(name, self)

        for key, value in kwargs.items():
            setattr(event, key, value)

        for eventObserver in self.observers:
            eventObserver(event)


class BindAbleProperties:
    def __init__(self):
        self._binds = {}

    def _add_bind(self, prop, call):
        if prop not in self._binds:
            self._binds[prop] = [call]
        else:
            if call not in self._binds[prop]:
                self._binds[prop] = self._binds[prop].append(call)

    def bind(self, **kwargs):
        for k, c in kwargs.items():
            if k not in self.__dict__:
                if callable(getattr(self, k)):
                    raise Exception(
                        'Cannot bind a callable method, only properties!')
                else:
                    raise Exception(
                        'Cannot bind a property that does not exist')
            self._add_bind(k, c)

    def unbind(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._binds:
                if v in self._binds[k]:
                    self._binds[k] = self._binds[k].remove(v)

    def emmit_property_change(self, prop, val):
        if prop in self._binds:
            for c in self._binds[prop]:
                c(val)


class IntProperty(int, BindAbleProperties):
    """
    This is a custom property representing an integer, which can trigger some
    callback when his data change.

    """

    def __new__(cls, value):
        obj = super(IntProperty, cls).__new__(cls, value)
        obj.data = value
        return obj


class ListProperty(UserList, BindAbleProperties):
    """
    This is a custom list which can trigger some callback when his data change.


    Examples
    --------



    """
    data = []

    def __init__(self, initlist=None):
        BindAbleProperties.__init__(self)
        super(ListProperty, self).__init__(initlist)

    def append(self, item):
        """ Append object to the end of the list. """
        super(ListProperty, self).append(item)
        self.emmit_property_change('data', self.data)

    def clear(self, *args, **kwargs):
        """ Remove all items from list. """
        super(ListProperty, self).clear()
        self.emmit_property_change('data', self.data)

    def extend(self, *args, **kwargs):
        """ Remove all items from list. """
        super(ListProperty, self).extend(*args, **kwargs)
        self.emmit_property_change('data', self.data)

    def insert(self, *args, **kwargs):
        """ Insert object before index. """
        super(ListProperty, self).insert(*args, **kwargs)
        self.emmit_property_change('data', self.data)

    def pop(self, *args, **kwargs):
        """
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """
        super(ListProperty, self).pop(*args, **kwargs)
        self.emmit_property_change('data', self.data)

    def remove(self, *args, **kwargs):
        """
        Remove first occurrence of value.

        Raises ValueError if the value is not present.
        """
        super(ListProperty, self).remove(*args, **kwargs)
        self.emmit_property_change('data', self.data)

    def reverse(self, *args, **kwargs):
        """ Reverse *IN PLACE*. """
        super(ListProperty, self).reverse()

    def sort(self, *args, **kwargs):
        """ Stable sort *IN PLACE*. """
        super(ListProperty, self).sort(*args, **kwargs)
        self.emmit_property_change('data', self.data)


class DictProperty(UserDict, BindAbleProperties):
    """
    Dictionary that remembers insertion order and the ability to trigger some
    callback when his data change.
    """

    def __init__(self, *args, **kwargs):
        BindAbleProperties.__init__(self)
        nargs = [self]
        [nargs.append(i) for i in args]
        UserDict.__init__(*nargs, **kwargs)

    def clear(self):
        super(DictProperty, self).clear()
        self.emmit_property_change('data', self)

    def popitem(self):
        key_value = super(DictProperty, self).popitem()
        self.emmit_property_change('data', self)
        return key_value

    def pop(self, key, default=None):
        value = super(DictProperty, self).pop(key, default)
        self.emmit_property_change('data', self)
        return value

    def __setitem__(self, key, value):
        self.data[key] = value
        self.emmit_property_change('data', self)

    def __delitem__(self, key):
        del self.data[key]
        self.emmit_property_change('data', self)

    def update(self, *args, **kwds):
        super(DictProperty, self).update(*args, **kwds)
        self.emmit_property_change('data', self)


if __name__ == '__main__':
    class House(object):
        def __init__(self):
            self.people = ListProperty([])
            self.location = DictProperty({})
            print("House is ready to receive people.")

        def someone_arrived(self, who, where):
            print(who + " has arrived!")
            self.people.append(who)
            self.location[who] = where

        def someone_leaves(self, who):
            print(who + " has left!")
            self.people.remove(who)
            if who in self.location:
                del self.location[who]

        def someone_moves(self, who, where):
            print(who + " has moved to " + where)
            self.location[who] = where

    def print_total_people(d):
        print('The House has {} people inside'.format(len(d)))

    def print_where_are(d):
        print('where are the people:')
        for k, v in d.items():
            print('\t-> {} is inside {}'.format(k, v))
    r = House()
    r.people.bind(data=print_total_people)
    r.location.bind(data=print_where_are)
    r.someone_arrived('Marta', 'living room')
    r.someone_arrived('John', 'kitchen')
    r.someone_moves('John', 'living room')
    r.someone_leaves('John')

    # def print_test_bind_method(d):
    #     print('print_test_bind_method: {}'.format(d))
    # r.people.bind(pop=print_test_bind_method)
