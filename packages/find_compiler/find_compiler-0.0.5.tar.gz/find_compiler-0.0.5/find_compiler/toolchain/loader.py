"""
https://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
"""

import imp
import os
import click

def get_plugins(out, folder=None, desc=None, main=None):
    folder = folder or "./plugins"
    desc = desc or folder
    main = main or "__init__"
    plugins = {}
    files = os.listdir(folder)
    for i in files:
        location = os.path.join(folder, i)
        if not os.path.isdir(location) or not main + ".py" in os.listdir(location):
            continue
        info = imp.find_module(main, [location])
        plugin = imp.load_module(i, *info)
        plugins[i] = plugin
        out.trace("Registering %s plugin: %s" % (click.style(desc, fg="yellow"), click.style(i, fg="green")))
    return plugins
