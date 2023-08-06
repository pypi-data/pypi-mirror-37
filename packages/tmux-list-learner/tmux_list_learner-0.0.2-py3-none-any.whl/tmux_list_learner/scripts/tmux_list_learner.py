#!/usr/bin/env python

import click
import os
import yaml
import sys
import random
import appdirs
from collections import OrderedDict

APPNAME='tmux-list-learner'
APPAUTHOR='flaxandteal'

default_window_lists = [
        {'name': 'network-top', 'items': ['Application', 'Presentation', 'Session', 'Transport', 'Network', 'Data-Link', 'Physical']},
        {'name': 'trad-major-rivers-africa', 'items': ['Nile', 'Niger', 'Senegal', 'Congo', 'Orange', 'Limpopo', 'Zambezi']},
        {'name': 'wonders-of-ancient-world', 'items': ['Pyramid-Giza', 'Gardens-Babylon', 'Zeus-Olympia', 'Artemis-Ephesus', 'Mausoleum-Halicarnassus', 'Colossus-Rhodes', 'Lighthouse-Alexandria']}
]

def load_window_names(overwrite=False):
    appdir = appdirs.user_config_dir(APPNAME, APPAUTHOR)
    os.makedirs(appdir, exist_ok=True)

    list_path = os.path.join(appdir, 'list.yaml')
    if overwrite or not os.path.exists(list_path):
        with open(list_path, 'w') as list_yaml:
            yaml.dump(default_window_lists, list_yaml)

    with open(list_path, 'r') as list_yaml:
        window_lists = yaml.load(list_yaml)

    window_names = OrderedDict([(i['name'], i['items']) for i in window_lists])

    return window_names

@click.command()
@click.argument('server_start')
@click.argument('session_name')
@click.argument('window_index', type=int)
def cli(server_start, session_name, window_index):
    window_names = load_window_names()

    if session_name[-1].isdigit() and int(session_name[-1]) < len(window_names) - 1:
        n = int(session_name[-1])
    else:
        n = random.randint(0, len(window_names) - 1)

    random.seed(server_start)

    keys = list(window_names.keys())
    random.shuffle(keys)
    key = keys[n]

    window_offset = min(window_index, len(window_names[key])) - 1
    window_name = window_names[key][window_offset]

    print(window_name)
