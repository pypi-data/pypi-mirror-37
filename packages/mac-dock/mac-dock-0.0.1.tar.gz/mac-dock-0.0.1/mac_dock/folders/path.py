#!/usr/bin/env python
import click
import mac_dock

PROG_NAME = 'python -m %s' % "mac_dock.folders.path"


@click.command()
def _cli():
    paths = list(map(lambda i: i.path, mac_dock.folders.items()))
    if paths:
        print("\n".join(paths))


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
