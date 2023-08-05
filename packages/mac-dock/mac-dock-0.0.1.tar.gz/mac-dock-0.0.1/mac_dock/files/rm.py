#!/usr/bin/env python
import click
import mac_dock

PROG_NAME = 'python -m %s' % "mac_dock.files.rm"


@click.command()
@click.argument('path', nargs=-1)
def _cli(path):
    if not path:
        path = list(map(lambda i: i.path, mac_dock.files.items()))
    mac_dock.files.rm(path)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
