import abc
import threading
from ..config import cnode, view
from .view import create_view

__all__ = ['Sourceable', 'AbstractProxy', 'Configuration', 'ConfigProxy']


class Sourceable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read(self, keys):
        """read Cnode/Cview from a configuration tree ."""
        return

    @abc.abstractmethod
    def write(self, keys, config_obj, is_overwrite=False):
        """add new configuration to a singleton config tree"""
        return


class AbstractProxy(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_proxy(self):
        """ factory create method."""
        return


class Configuration(Sourceable):
    __root = None

    def __init__(self, root_node):
        if not isinstance(root_node, cnode.CNode):
            raise ValueError("root must be Cnode object.")
        self.set_root(root_node)

    def set_root(self, root):
        self.__root = root

    def get_root(self):
        return self.__root

    def read(self, keys) -> view.CView:
        if self.__root is not None:
            cv = view.CView(self.__root)
            return cv.get(keys)

    def get_view(self, path):
        return create_view(self.__root, path)

    def __getitem__(self, keys):
        return self.read(keys)

    def write(self, keys, config_obj: [str, dict, cnode.CNode], is_overwrite=False):
        self.__root.update(keys, config_obj, overwrite_node=is_overwrite)


class ConfigProxy(AbstractProxy):
    """a proxy for configuration."""
    _instance_lock = threading.Lock()
    __configs = {}
    _instance = None

    def __init__(self, root=None, root_id=None):
        self.init_params = [root, root_id]
        if self.init_params[0] is not None and self.init_params[1] is not None:
            self.create_proxy()

    def __new__(cls, *args, **kwargs):
        if ConfigProxy._instance is None:
            with ConfigProxy._instance_lock:
                if ConfigProxy._instance is None:
                    ConfigProxy._instance = object.__new__(cls)
        return ConfigProxy._instance

    @classmethod
    def reset(cls):
        if ConfigProxy._instance is not None:
            ConfigProxy._instance = None
            ConfigProxy.__configs = {}

    def create_proxy(self):
        return self.add_proxy(self.init_params[0], self.init_params[1])

    def add_proxy(self, config_obj: Configuration, config_id: str):
        """assign a name(ID) for every config"""
        if not isinstance(config_obj, Configuration):
            raise ValueError('config_obj must be a Configuration object.')
        if config_id in self.__configs.keys():
            raise ValueError('config_id already exists.')
        self.__configs[config_id] = config_obj

    def write(self, config_id, keys, config_obj, is_overwrite=False):
        return self.__configs[config_id].write(keys, config_obj, is_overwrite=is_overwrite)

    def read(self, config_id, config_key):
        return self.__configs[config_id].read(config_key)

    def __getitem__(self, item):
        return self.__configs[item]

    def get_view(self, item, path):
        return self.__configs[item].get_view(path)

    def get(self, item):
        return self.__configs.get(item)

    def __setitem__(self, config_id, root):
        if config_id in self.__configs.keys():
            if isinstance(root, Configuration):
                self.__configs[config_id] = root
                return
            else:
                raise ValueError('item must be a configuration object.')
        self.add_proxy(root, config_id)
        return

    def __delitem__(self, key):
        if key in self.__configs:
            del self.__configs[key]

    def get_root_node(self, config_id):
        """get configuration's root Cnode corresponding to config_id"""
        if config_id not in self.__configs.keys():
            return None
        return self.__configs[config_id].get_root()

    def set_root_node(self, config_id, root):
        """reset configuration's root Cnode corresponding to config_id"""
        if config_id not in self.__configs.keys():
            raise ValueError('configuration not found .')
        return self.__configs[config_id].set_root(root)
