# -*- coding: utf-8 -*-
"""
paff.cli - command line stuff
"""

import click

from .settings import Config
from .core import getMD5forDirectory, getNamesforDirectory, getDatesforDirectory
from .core import compareHashesFromDirectory, printLeftovers
from .core import checkPathExistence
from .data import hashData

paff_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.option('--cache', is_flag=True,
              help='Enables caching mode.')
@paff_config
def cli(config, verbose, cache):
    config.verbose = verbose
    config.cache = cache


# ToDo: add different modi, hash compare eveywhere, directory-based compare (file size, name, date, hash...)
@cli.command()
@click.option('--dst', prompt='Destination Path',
              help='Destination path to check for files',
              type=click.Path())
@click.option('--src', prompt='Source Path',
              help='Source path to check for files.',
              type=click.Path())
def compare(dst, src):
    """Compare files based on MD5 hashes."""
    # PATH1 = "/Volumes/Photos/Life/2010-03 Meppen"
    # PATH2 = "/Volumes/ExData/Photo Export/Meppen 2010"

    hashesDst = getMD5forDirectory(dst)
    hashesSrc = getMD5forDirectory(src)

    leftoversDst, leftoversSrc = compareHashesFromDirectory(hashesDst, hashesSrc)

    printLeftovers(src, leftoversSrc)


@cli.command()
@click.option('--dst', prompt='Destination Path',
              help='Destination path to check for files',
              type=click.Path())
@click.option('--src', prompt='Source Path',
              help='Source path to check for files.',
              type=click.Path())
def compareNames(dst, src):
    """Compare files based on names."""
    namesDst = getNamesforDirectory(dst)
    namesSrc = getNamesforDirectory(src)

    leftoversDst, leftoversSrc = compareHashesFromDirectory(namesDst, namesSrc)

    printLeftovers(src, leftoversSrc)
    printLeftovers(dst, leftoversDst)


@cli.command()
@click.option('--dst', prompt='Destination Path',
              help='Destination path to check for files',
              type=click.Path())
@click.option('--src', prompt='Source Path',
              help='Source path to check for files.',
              type=click.Path())
def compareDates(dst, src):
    """Compare files based on names and modified dates."""
    datesDst = getDatesforDirectory(dst)
    datesSrc = getDatesforDirectory(src)

    leftoversDst, leftoversSrc = compareHashesFromDirectory(datesDst, datesSrc)

    printLeftovers(src, leftoversSrc)
    printLeftovers(dst, leftoversDst)


@cli.command()
@paff_config
def sync(dst, src):
    """Synchronizes two different directories based on a comparison algorithm."""
    # TODO: create arguments for different comparison types
    print("Not implemented yet.")



@cli.command()
@paff_config
def verify(config):
    """Verifies all hashes in the hash database. Also allows fixing any issues that come up."""
    if config.verbose:
        click.echo("We are in verbose mode")
    print("Not implemented yet.")


@cli.command()
@paff_config
def stats(config):
    """Displays statistics about previously generated file hashes."""
    if config.verbose:
        click.echo("We are in verbose mode")
    paths = sorted(hashData.getPaths())
    print("Number of paths stored in database:", len(paths))


# TODO: add option to verify hashes before cleanup
@cli.command()
@paff_config
def cleanup(config):
    """Cleanup the hash database. Removes old hashes."""
    # TODO: Create path-sorted list of all hashes.
    # TODO: Check whether files are still there.
    # TODO: Present warning depending on where the files are stored (e.g. /Volumes on MacOS)
    if config.verbose:
        click.echo("We are in verbose mode")
    paths = sorted(hashData.getPaths())

    missing = checkPathExistence(paths)
    print("Missing paths:")
    print(missing)
    print("Not fully implemented yet.")


@cli.command()
@click.option('--path', prompt='Path',
              help='Path to directory that should be hashed and added to database.',
              type=click.Path())
@paff_config
def hash(config, path):
    """Hash all files in directory for the future."""
    if config.verbose:
        click.echo("We are in verbose mode")
    getMD5forDirectory(path)


def main():
    cli()
