from enum import Enum
class PluginType(Enum):
    Dev = 0
    RT = 1
    Safecast = 2

def type2name(pt):
    if pt == PluginType.Dev:
        return "Radiation Toolbox (DEV)"
    elif pt == PluginType.RT:
        return "Radiation Toolbox"
    else: # Safecast
        return "Safecast"

PLUGIN_TYPE = PluginType.Dev
PLUGIN_NAME = type2name(PLUGIN_TYPE)
