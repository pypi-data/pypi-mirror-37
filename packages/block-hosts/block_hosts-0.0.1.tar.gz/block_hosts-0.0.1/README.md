# Block

Block is a simple Python-based command line utility for blocking access to web-sites in order to stop you from procrastinating, because you can't do it by yourself. Relies on modifying the hosts file.

## Installing

Under construction.

## Usage

The simplest and most common usage of Block is to block all sites in a curated list. To do this, run the following command in the console:

```
$ block curated
```

and to unblock, run:

```
$ block unblock
```

To block a single web site, run:

```
$ block website_url
```

where *website_url* refers to, you guessed it, the URL of the website you want to block. To reverse the action, run

```
$ block unblock website_url
```

Note: modifying the hosts file requires administrator privileges, so make sure that the terminal is in elevated mode.