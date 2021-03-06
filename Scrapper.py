import argparse
import os

import utils

from yapsy.PluginManager import PluginManager

PLUGIN_BASE_DIR_DEV = "modules"
PLUGIN_BASE_DIR = "/opt/slackscrapper/modules"


def _available_module() -> list:
    return [module for module in os.listdir(PLUGIN_BASE_DIR) if module[0] != "_"]


def _plugin_loader(arg_module: str, my_plugin_manager: PluginManager):
    load = arg_module if arg_module in _available_module() else None
    if load is None:
        utils.error("No module {module} found. Does the plugin you want exist and contains no typos ?",
                    name="module", lst=_available_module())
    my_plugin_manager.setPluginPlaces([os.path.join(PLUGIN_BASE_DIR, arg_module)])
    my_plugin_manager.collectPlugins()


def _actioning(arg_action: str, my_plugin_manager: PluginManager):
    plugin = utils.simplify_list(my_plugin_manager.getAllPlugins())
    if arg_action in plugin.plugin_object.actions():
        func = getattr(plugin.plugin_object, arg_action)
        func()
    else:
        utils.error("No action {action} found. Does your action exists and contains no typos ?",
                    name="action", lst=plugin.plugin_object.actions())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="slackscrapper")
    required = parser.add_argument_group("required named arguments")
    required.add_argument("-m", "--module", help="The name of the module you want to call.", required=True)
    required.add_argument("-a", "--action", help="The name of the action you want to call.", required=True)
    args = parser.parse_args()

    plugin_manager = PluginManager()
    _plugin_loader(args.module, plugin_manager)
    _actioning(args.action, plugin_manager)
