#!/usr/bin/env python
import click
import mac_dock

PROG_NAME = 'python -m %s' % "mac_dock.apps.bundle"


@click.command()
def _cli():
    bundles = list(map(lambda i: i.bundle, mac_dock.apps.items()))
    if bundles:
        print("\n".join(bundles))


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
