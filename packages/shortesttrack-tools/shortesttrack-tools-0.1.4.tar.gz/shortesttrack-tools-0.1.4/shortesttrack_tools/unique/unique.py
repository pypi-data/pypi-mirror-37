from typing import Type
import threading

from shortesttrack_tools.functional import classproperty


class Unique:
    """
    This class is implemented the Unique pattern (like Singletone, but without extra meta-programming magic)
    and should be subclassed if you don't need to re-initialize some object on every operation.
    Your subclass's object will be initialized only once, but will have all the power you need.

    >>> class Cat(Unique):
    ...     eyes: int = None
    ...     tail: int = None
    ...     objects_counter: int = None
    ...
    ...     @classmethod
    ...     def _do_init(cls):
    ...         cls.eyes = 2
    ...         cls.tail = 1
    ...         if cls.objects_counter is None:
    ...             cls.objects_counter = 0
    ...         cls.objects_counter += 1
    ...         if cls.objects_counter > 1:
    ...             raise Exception('This exception never be happened')
    ...
    >>> class Dog(Unique):
    ...     eyes: int = None
    ...     tail: int = None
    ...     objects_counter: int = None
    ...
    ...     @classmethod
    ...     def _do_init(cls):
    ...         cls.eyes = 2
    ...         cls.tail = 1
    ...         if cls.objects_counter is None:
    ...             cls.objects_counter = 0
    ...         cls.objects_counter += 1
    ...         if cls.objects_counter > 1:
    ...             raise Exception('This exception never be happened')
    ...
    >>> cat = Cat.init()
    >>> Cat._initialized != Dog._initialized
    True
    >>> cat.eyes
    2
    >>> cat.objects_counter
    1
    >>> cat.eyes +=1
    >>> cat.eyes
    3
    >>> another_but_same_cat = Cat.init()
    >>> another_but_same_cat.eyes
    3
    >>> another_but_same_cat.objects_counter
    1
    >>> another_but_same_cat == cat
    True
    >>> id(another_but_same_cat) == id(cat)
    True
    >>> dog = Dog.init()
    >>> dog.eyes
    2
    >>> cat.eyes
    3
    >>> cat3 = Cat.init()
    >>> cat3.eyes
    3
    >>> dog.tail
    1
    >>> dog == cat
    False
    >>> dog.objects_counter
    1
    >>> dog._init_lock != cat._init_lock
    True
    """

    _initialized = False
    _init_lock = None

    def __init__(self):
        raise RuntimeError('The Unique subclass cannot be initialized in this way. '
                           'Do not use __init__ for initialize the Unique object.')

    @classmethod
    def init(cls, *args, **kwargs) -> 'Type[Unique]':
        """
        Use to call this method instead of __init__ (like you do for your regular classes)

        Returns
        -------
        object
            cls itself
        """

        if cls._initialized:
            return cls

        if cls._init_lock:
            init_lock = cls._init_lock
        else:
            init_lock = cls._init_lock = threading.RLock()

        with init_lock:
            if cls._initialized:
                return cls

            cls._do_init(*args, **kwargs)
            cls._finish_init()
            return cls

    @classmethod
    def _do_init(cls, *args, **kwargs):
        """
        This method is the regular classes __init__ method analogue.

        Define your initialized logic in this method of your subclass.

        Notes
        -----
        It will do effect only once, while the first initialization.
        """
        raise NotImplementedError

    @classmethod
    def _finish_init(cls):
        cls._initialized = True

    @classproperty
    def initialized(cls):
        return cls._initialized
