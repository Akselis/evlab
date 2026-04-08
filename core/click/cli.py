import click

import core.ansible.inventory as inv
import core.dock.container as dops


@click.group()
def cli():
    pass


@cli.group()
def lab():
    pass


@lab.command()
@click.option("--name", required=True, help="Name for the container.")
@click.option("--host", default="localhost", help="Host IP.")
def init(name, host):
    i = inv.EvLabInventory()
    i.group_insert(name)
    host_vars = {"ansible_host": host} if host is not None else None
    host_vars = {"ansible_connection": "local"} if host == "localhost" else host_vars
    if host is not None and host_vars is not None:
        i.host_insert_update(host, name, host_vars=host_vars)


@cli.group()
def service():
    pass


@service.command()
@click.option("--host", default="localhost", help="Target host from inventory.")
@click.option("--image", required=True, help="Docker image to pull/run.")
@click.option("--name", required=True, help="Name for the container.")
def start(host, image, name):
    click.echo(f"Running {image} on {host}...")
    res = dops.start_container(host, image, name)

    if res:
        click.secho("Success!", fg="green")
    else:
        click.secho("Failed. Check the output above for details.", fg="red")


@service.command()
@click.option("--host", default="localhost", help="Target host from inventory.")
@click.option("--name", required=True, help="Name for the container.")
def stop(host, name):
    click.echo(f"Stopping container {name} on {host}...")
    res = dops.stop_container(host, name)

    if res:
        click.secho("Success!", fg="green")
    else:
        click.secho("Failed. Check the output above for details.", fg="red")
