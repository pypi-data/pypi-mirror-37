"""Contains command group for task queues."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import click
from .resource import (
    generic_get_command,
    generic_list_command,
)
from .utils import(
    list_options,
)

TASK_QUEUE_ATTRS = (
    'id',
    'user',
    'name',
    'private',
    'active',
    'description',
)


@click.group()
def task_queues():
    """Command group to interface with task queues."""
    pass


@task_queues.command(name='get')
@click.argument(
    'id',
    nargs=1,
    type=click.INT,)
@click.pass_context
def get_task_queue(ctx, id):
    """Get task queue based on ID."""
    generic_get_command(
        'task_queues',
        TASK_QUEUE_ATTRS,
        ctx,
        id,
    )


@task_queues.command(name='list')
@list_options
@click.pass_context
def list_task_queues(ctx, filters, filters_file):
    """List task queues matching filter parameters."""
    generic_list_command(
        'task_queues',
        TASK_QUEUE_ATTRS,
        ctx,
        filters,
        filters_file,
    )
