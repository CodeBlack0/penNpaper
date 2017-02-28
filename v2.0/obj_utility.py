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
                return int(x)
            except ValueError:
                return x

        @staticmethod
        def text_to_int(x):
            return Utility.Helper.to_int(x.text)

        @staticmethod
        def to_float(x):
            try:
                return float(x)
            except ValueError:
                return x

        @staticmethod
        def text_to_float(x):
            return Utility.Helper.to_float(x.text)

        @staticmethod
        def to_scale(x, scale):
            try:
                if not isinstance(scale, tuple):
                    raise Exception('Utility.Helper.to_scale: scale must be tuple (format: ({units: fac}, [synonyms])\
                                    , is ' + str(type(scale)) + ' --> ' + str(scale))
                val = Utility.Helper.text_to_float(x)

                # finding conversionfacor
                fac = scale[0][x.attrib['unit']] if x.tag in scale[1] else 1

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
