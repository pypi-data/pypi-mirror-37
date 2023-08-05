# -*- coding: utf-8 -*-

"""Console script for aiscalator."""
import sys
import click
import json
import os
import logging.config

from platform import uname
from yaml import safe_load
from . import __version__
from .utils import find
from .docker_command import docker_run_lab, docker_run_papermill


def setup_logging(default_path='logging.yaml', env_key='LOG_CFG'):
    """Setup logging configuration
    """
    path = default_path
    loglevel = os.getenv('AISCALATOR_LOG_LEVEL', logging.INFO)
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = safe_load(f.read())
        logging.config.dictConfig(config)
        if loglevel != logging.INFO:
            logging.root.setLevel(loglevel)
    else:
        logging.basicConfig(level=loglevel)
    logging.debug("Starting " + os.path.basename(__name__) +
                  " version " + __version__ + " on " +
                  " ".join(uname()))


def setup_app_config():
    """Setup application configuration"""
    pass


@click.group()
def main():
    """
    Command Line Interface to Aiscalate your data pipelines
    """
    setup_logging('resources/config/logging.yaml')
    setup_app_config()
    pass


# TODO implement a class to handle more complex configurations
# (example: different formats, merge multiple files etc)
def parse_config(conf):
    try:
        j = json.loads(conf)
    except json.decoder.JSONDecodeError:
        try:
            with open(conf, "r") as f:
                j = json.load(f)
        except Exception as err2:
            logging.error("Invalid configuration file")
            raise err2
    logging.debug("Configuration file = " +
                  json.dumps(j, indent=4))
    return j


@main.command()
@click.argument('conf')
@click.argument('notebook')
# TODO add parameters override from CLI
def edit(conf, notebook):
    """Open an environment to edit step's code"""
    step = find(parse_config(conf)['step'], notebook)
    if step is not None:
        click.echo(docker_run_lab(step))


@main.command()
@click.argument('conf')
@click.argument('notebook')
# TODO add parameters override from CLI
def run(conf, notebook):
    """Run step's code without GUI"""
    # TODO run multiple notebooks
    # we have to stage notebooks with same dockerfile together,
    # merge their requirements so that groups of notebooks can be
    # run together in the same container sequentially
    step = find(parse_config(conf)['step'], notebook)
    if step is not None:
        click.echo(docker_run_papermill(step))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
