# dnskeeper-cloudflare
Tool for managing DNS records in cloudflare and storing them locally in JSON.


## Installation:
`sudo pip install dnskeeper`


## Usage:

```
~#: dnskeeper --help
usage: dnskeeper <command> [<args>]
The available dnskeeper commands are:
        config          Create config file for dnskeeper
        diff            Display differences between local state and Cloudflare
        pull            Overwrite local records with current state
        push            Deploy changes to Cloudflare
        show            Show current state in Cloudflare
        validate        Test records file for proper formatting
        version         Display version
Tool for managing Cloudflare DNS, by Liferay
positional arguments:
  command     Subcommand to run
optional arguments:
  -h, --help  show this help message and exit
```

### Subcommands:

Each subcommand has its own parameters that can be shown with a `-h`/`--help` flag

Example:

```
~#: dnskeeper push -h
usage: dnskeeper [-h] [-d] [-o {json,simple,table}] domain
Deploy changes to Cloudflare
positional arguments:
  domain
optional arguments:
  -h, --help            show this help message and exit
  -d, --dry-run         simulates the actions that would occur
  -o {json,simple,table}, --output {json,simple,table}
  ```


