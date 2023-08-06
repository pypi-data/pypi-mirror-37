import shelve
from os import path
from inspect import isclass


class State:
    def __init__(self, state_plugin=None, local_state_path=None):
        if isclass(state_plugin):
            self.state_plugin = state_plugin()

            for func in "get_state", "set_state":
                if func not in dir(self.state_plugin):
                    raise ValueError("Missing get_state or set_state functions in state_plugin")

            if not callable(self.state_plugin.get_state) or not callable(self.state_plugin.set_state):
                raise ValueError("get_state or set_state in state_plugin are not functions")
        else:
            self.state_plugin = None

            if local_state_path is None:
                self.local_state_path = path.join(path.expanduser("~"), "fabrica-state")
            else:
                self.local_state_path = local_state_path

            self.state = shelve.open(self.local_state_path)

    def set_state(self, key, value):
        if self.state_plugin is not None:
            self.state_plugin.set_state(key, value)
        else:
            self.state[key] = value

    def get_state(self, key):
        if self.state_plugin is not None:
            return self.state_plugin.get_state(key)
        else:
            return self.state.get(key, None)
