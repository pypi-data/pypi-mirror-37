#!/usr/bin/env python
import click
import mac_dock

PROG_NAME = 'python -m %s' % "mac_dock.folders.rm"


@click.command()
@click.argument('path', nargs=-1)
def _cli(path):
    if not path:
        path = list(map(lambda i: i.path, mac_dock.folders.items()))
    mac_dock.folders.rm(path)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
