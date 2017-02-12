from functools import wraps


class Utility(object):
    # ==[Basic functions]===============================================================================================
    class Helper(object):
        # this class holds some basic functions which are often used when parsing data

        @staticmethod
        def identity(x):
            return x

        @staticmethod
        def text(x):
            return x.text

        @staticmethod
        def to_int(x):
            try:
                return int(x.text)
            except ValueError:
                return x.text

        @staticmethod
        def to_float(x):
            try:
                return float(x.text)
            except ValueError:
                return x.text

        @staticmethod
        def to_scale(x, scales):
            try:
                if not isinstance(scales, dict):
                    raise Exception('Utility.Helper.to_scale: scale must be dict, is ' +
                                    str(type(scales)) + ' --> ' + str(scales))
                val = Utility.Helper.to_float(x)

                # finding applicable scale
                for size, scl in scales.items():
                    if x.tag == size or x.tag in scl[1]:
                        fac = scl[0][x.attrib['unit']]
                        # print(Utility.Helper.to_float(x) * fac)
                        break
                else:
                    return val

                # applying scale
                return val * fac if isinstance(val, float) else val
            except Exception as err:
                print(err)

    # ==[TOOLS]=========================================================================================================
    @staticmethod
    def curry(func):
        @wraps(func)
        def curried(*args, **kwargs):
            if len(args) + len(kwargs) >= func.__code__.co_argcount:
                return func(*args, **kwargs)

            @wraps(func)
            def new_curried(*args2, **kwargs2):
                return curried(*(args + args2), **dict(kwargs, **kwargs2))

            return new_curried

        return curried
