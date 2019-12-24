import sys


def update_module_attributes(object_names, module_name):
    module = sys.modules[module_name]
    for object_name in object_names:
        getattr(module, object_name).__module__ = module_name
