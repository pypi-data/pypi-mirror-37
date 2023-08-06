# tmux-list-learner

## Purpose

This is a tool to help you learn lists during day-to-day software development. When creating new tmux windows, each will be given the name of a list item, such as wonders of the ancient world. For each session, the list will be randomly chosen, but each window name (once you create it) within a list will appear in a consistent ordering.

Note that spaces are not currently supported.

## Install

To use this, install `tmux-list-leaner` so it can be accessed in your path:

    python3 setup.py install --user

Next, add the lines in `tmux.conf.append` to your `~/.tmux.conf`

A default set of things to learn is created in your user config directory on first run. On Linux, this is `~/.config/tmux-list-learner/list.yaml`
