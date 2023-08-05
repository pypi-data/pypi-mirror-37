import sys
import inspect
import types
from ..check.mixin import _check_attr_method_map
from ..error.check_error import CheckError


class check_dec(object):

    def __init__(self, f, fields, reraise=False, *args,
                 **kwargs):
        self.func = f
        self.fields = fields
        self.reraise = reraise

    def __call__(self, *args, **kwargs):
        res = self.func(*args, **kwargs)
        return res

    def __get__(self, instance, cls):
        return types.MethodType(self, instance, cls)


class check(object):
    """
    Decorator aimed to map attributes with check methods
    that will then validate the values of those attributes in the loading time.
    The parameters of the decorated function are dynamicly introspected.
    The first param will always be the value of the field defined in the
    decorator that triggered the validation call.
    Any successive parameter will be looked for by name in the object created
    from the `add` method and its value will be sent to the validation method.
    Keyword parameters are allowed, and if they are not found in the object
    the default value will then persist.

    E.G:
        @check(['attr1'], reraise=True, sequence=32)
        def validation_method(val, attr2, attr3=False):
            if attr1 == 'A' and attr2 == 'B' and attr3:
                raise CustomException('Error!')
            else:
                return False

    @param fields: List of attribute names the defined method will check.
    @type  fields: list
    @param reraise: Wheter the custom CheckError or the Exception itself should
                    be raised if an exception is found in the validation.
    @type  reraise: bool
    @param sequence: Numeric key used to sort the execution of the validation
                     methods (From lower to greater). The default is 10.
    @type  sequence: int
    @return: Newly defined method pointer.
    @rtype : function
    """

    def __init__(self, fields=[], reraise=False, sequence=10):
        if not fields or not all(map(lambda x: isinstance(x, str),
                                     fields)):
            msg = ("Check decorator should receive a list of " +
                   "attributes to check.\nGot %s instead" % fields)
            raise CheckError(message=msg)
        self.reraise = reraise
        self.fields = fields
        self.sequence = sequence

    def __call__(self, func, *args, **kwargs):
        ins = check_dec(func, self.fields, self.reraise, *args, **kwargs)
        for f in self.fields:
            if sys.version_info[0] == 2:
                inspected_args = inspect.getargspec(ins.func)
            else:
                inspected_args = inspect.getfullargspec(ins.func)
            all_args = inspected_args[0]
            kw_defaults = inspected_args[3] or []
            cut_index = - len(kw_defaults) or len(all_args) + 1
            args = all_args[:cut_index]
            kwargs = all_args[cut_index:]
            _check_attr_method_map[f] = [ins, (args, kwargs),
                                         self.sequence]
        return ins
