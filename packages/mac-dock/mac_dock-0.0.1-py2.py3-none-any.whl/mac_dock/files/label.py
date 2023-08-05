#!/usr/bin/env python
import click
import mac_dock

PROG_NAME = 'python -m %s' % "mac_dock.files.label"


@click.command()
def _cli():
    labels = list(map(lambda i: i.label, mac_dock.files.items()))
    if labels:
        print("\n".join(labels))


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
