# -*- coding: utf-8 -*-

COLORS = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
          'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

def pretty_label(inStr):
    """
        Makes a pretty version of our column names
        "zone_1" -> "Zone 1"
        "zone_2"-> "Zone 2
        ...
        "zone_strength" -> "Strength"
    """
    import re
    pattern = re.compile("zone_[12345]{1}|zone_1,2")
    if pattern.match(inStr):
        out = inStr
    else:
        out = inStr[5:]
    return out.replace("_", " ").capitalize()
    
