import python_hosts
import click
import sys

SITES = [
    "www.facebook.com",
    "twitter.com",
    "www.reddit.com",
    "www.instagram.com",
    "www.goodreads.com",
    "9gag.com",
    "yts.ag",
    "www.snapchat.com",
    "vk.com",
    "www.4chan.com",
    "www.buzzfeed.com",
    "www.flickr.com",
    "news.ycombinator.com",
    "ispovesti.com",
    "blic.rs",
    "www.hltv.org",
    "www.twitch.tv",
]

HOSTSPATH = None
if sys.platform in ("win32", "cygwin"):
    HOSTSPATH = "C:/Windows/System32/drivers/etc/hosts"
else:
    HOSTSPATH = "/etc/hosts"


@click.group()
def cli():
    pass


@click.command(help="Block all sites from the curated list of sites.")
def curated():
    hosts = python_hosts.Hosts(HOSTSPATH)
    for site in SITES:
        new_entry = python_hosts.HostsEntry(
            entry_type="ipv4", address="127.0.0.1", names=[site]
        )
        hosts.add([new_entry])

    try:
        hosts.write()
    except python_hosts.exception.UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(help="Block a single site, defined by the positional argument.")
@click.argument("site")
def single(site):
    hosts = python_hosts.Hosts(HOSTSPATH)
    new_entry = python_hosts.HostsEntry(
        entry_type="ipv4", address="127.0.0.1", names=[site]
    )

    hosts.add([new_entry])

    try:
        hosts.write()
    except python_hosts.exception.UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(
    help="Unblock sites from the curated list of sites. Optionally, unblock a single site."
)
@click.option(
    "-s",
    "--site",
    default=None,
    help="Specify the site to unblock. The command will unblock the specified site only.",
)
def unblock(site):
    hosts = python_hosts.Hosts(HOSTSPATH)

    if site is None:
        for s in SITES:
            hosts.remove_all_matching(name=s)
    else:
        hosts.remove_all_matching(name=site)

    try:
        hosts.write()
    except python_hosts.exception.UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(help="Prints a list of curated sites that will be blocked by default.")
def ls():
    print("The following is a list of curated sites.\n")
    for site in SITES:
        print(site)


cli.add_command(curated)
cli.add_command(single)
cli.add_command(unblock)
cli.add_command(ls)

if __name__ == "__main__":
    cli()
