#!/usr/bin/env python

from stlib import plugins

manager = plugins.Manager()

print(manager.available_plugins)
print(manager.loaded_plugins)
print(manager.has_plugin('steamgifts'))
print(manager.load_plugin('steamgifts'))
print(manager.unload_plugin('steamgifts'))
