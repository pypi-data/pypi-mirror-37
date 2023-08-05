#!/usr/bin/env python
import click
import mac_dock

PROG_NAME = 'python -m %s' % "mac_dock.folders.label"


@click.command()
def _cli():
    labels = list(map(lambda i: i.label, mac_dock.folders.items()))
    if labels:
        print("\n".join(labels))


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
