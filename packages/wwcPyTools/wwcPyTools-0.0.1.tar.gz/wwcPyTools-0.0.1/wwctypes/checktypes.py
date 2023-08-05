from python_tools import colors
from collections import defaultdict
from functools import wraps

__arg_types_list = defaultdict(list)
__ret_types_list = defaultdict(list)


def check_type(in_=(None,), out=(type(None),)):
    def to_tuple_or_list(arg):
        if not (isinstance(arg, tuple) or isinstance(arg, list)):
            arg = (arg, )
        return arg

    out = to_tuple_or_list(out)
    in_ = to_tuple_or_list(in_)

    def to_red_string(string):
        res = '{color}{bold}{string}{end}'\
            .format(color=colors.FAIL, bold=colors.BOLD, string=string, end=colors.ENDC)
        return res

    def th_or_st(i):
        if i == 1:
            return '1st'
        elif i == 2:
            return '2nd'
        elif i == 3:
            return '3rd'
        else:
            return '{}th'.format(i)

    def my_isinstance(obj, type_):
        return type(obj) == type_

    def get_func(func):
        return 'In FUNC: "{}" '   \
            .format(func.__qualname__)

    def __check_type(real_types, func, check_arg, __types_list_record, __arg_right_list_record, *args):
        res = False
        arg_match = False
        global __arg_types_list
        global __ret_types_list
        func_name = func.__qualname__
        if check_arg:
            __types_list = __arg_types_list
        else:
            __types_list = __ret_types_list

        for types_list in __types_list[func_name]:
            if len(types_list) == len(args):
                arg_match = True
                break 

        if arg_match is False:
            if check_arg:
                print(to_red_string(get_func(func)
                                    + '\n\tArgument length is different'))
            else:
                print(to_red_string(get_func(func)
                                    + '\n\tReturn length is different'))
            return False

        name = 'arg' if check_arg else 'return value'
        if check_arg:
            __types_list = __arg_types_list
            # __types_list_record = __arg_types_list_record
        else:
            __types_list = __ret_types_list
            # __types_list_record = __ret_types_list_record

        for try_i, types in enumerate(__types_list[func_name]):
            if len(args) != len(types):
                __types_list_record[func_name].append({try_i: to_red_string('In FUNC {} '
                                                                            'return length is wrong'.format(func_name))})
                break
            for i, arg_i in enumerate(args):
                if not my_isinstance(arg_i, types[i]):
                    __types_list_record[func_name].append({try_i: to_red_string(get_func(func)
                                                                                + '\n\t{i} {} "{arg_i}" should be '
                                                                                '{real_t}'.format(name, i=th_or_st(i+1), arg_i=arg_i, real_t=types[i]))})
                    break
            else:
                if check_arg:
                    __arg_right_list_record[func_name].append(try_i)
                    res = True
                else:
                    # check if return type and arg type match
                    for right_items in __arg_right_list_record[func_name]:
                        if right_items == try_i:
                            return True

        return res

    def __check(func):
        func_name = func.__qualname__
        __arg_types_list[func_name].append(in_)
        __ret_types_list[func_name].append(out)
        __arg_types_list[func_name].reverse()
        __ret_types_list[func_name].reverse()

        @wraps(func)
        def wrapper(*args):
            global __arg_types_list
            global __ret_types_list
            __arg_types_list_record = defaultdict(list)
            __arg_right_list_record = defaultdict(list)
            __ret_types_list_record = defaultdict(list)

            argtype_true = __check_type(
                in_,  func, True, __arg_types_list_record, __arg_right_list_record, *args)
            if not argtype_true:
                for wrong_types in __arg_types_list_record[func_name]:
                    for k, v in wrong_types.items():
                        print('{} try: \n\t{}'.format(th_or_st(k+1), v))

                raise TypeError(to_red_string('FUNC "{}" argument type is wrong'
                                              .format(func.__qualname__)))
            res = func(*args)
            res_ = to_tuple_or_list(res)
            ret_true = __check_type(
                out, func, False, __ret_types_list_record, __arg_right_list_record, *res_)
            if not ret_true:
                for wrong_types in __ret_types_list_record[func_name]:
                    for k, v in wrong_types.items():
                        print('{} try: \n\t{}'.format(th_or_st(k+1), v))
                raise TypeError(to_red_string('FUNC "{}" return type is wrong'
                                              .format(func.__qualname__)))

            return res
        return wrapper
    return __check
