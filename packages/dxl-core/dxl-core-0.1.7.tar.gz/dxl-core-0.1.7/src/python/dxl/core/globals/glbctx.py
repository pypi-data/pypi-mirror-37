__all__ = ['GlobalContext', 'clear_all']

globals = {}


class GlobalContext:
    @classmethod
    def set(cls, value):
        globals[cls] = value

    @classmethod
    def get(cls):
        return globals.get(cls)

    @classmethod
    def clear(cls):
        try:
            del globals[cls]
        except KeyError:
            pass


def clear_all():
    globals.clear()
