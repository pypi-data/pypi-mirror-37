import python_hosts
import click
import sys

SITES = ['facebook', 'twitter', 'reddit', 'instagram']
PREFIX = 'www'
SUFIX = 'com'

HOSTSPATH = None
if sys.platform in ('win32', 'cygwin'):
    HOSTSPATH = 'C:/Windows/System32/drivers/etc/hosts'
else:
    HOSTSPATH = '/etc/hosts'

@click.group()
def cli():
    pass

@click.command()
def curated():
    hosts = python_hosts.Hosts(HOSTSPATH)
    for site in SITES:
        names = ['.'.join((site, SUFIX)), '.'.join((PREFIX, site, SUFIX))]
        for name in names:
            new_entry = python_hosts.HostsEntry(entry_type='ipv4', address='127.0.0.1', names=[name])
            hosts.add([new_entry])
        
    hosts.write()

@click.command()
def unblock():
    hosts = python_hosts.Hosts(HOSTSPATH)
    for site in SITES:
        names = ['.'.join((site, SUFIX)), '.'.join((PREFIX, site, SUFIX))]
        for name in names:
            hosts.remove_all_matching(name=name)

    hosts.write()

cli.add_command(curated)
cli.add_command(unblock)

if __name__ == '__main__':
    cli()