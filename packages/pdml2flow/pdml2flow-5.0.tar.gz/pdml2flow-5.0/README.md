# pdml2flow [![PyPI version](https://badge.fury.io/py/pdml2flow.svg)](https://badge.fury.io/py/pdml2flow) 
_Aggregates wireshark pdml to flows, with plugins_

| Branch  | Build  | Coverage |
| ------- | ------ | -------- |
| master  | [![Build Status master]](https://travis-ci.org/Enteee/pdml2flow) | [![Coverage Status master]](https://coveralls.io/github/Enteee/pdml2flow?branch=master) |
| develop  | [![Build Status develop]](https://travis-ci.org/Enteee/pdml2flow) | [![Coverage Status develop]](https://coveralls.io/github/Enteee/pdml2flow?branch=develop) |

## Prerequisites
* [python]:
  - 3.4
  - 3.5
  - 3.5-dev
  - 3.6
  - 3.6-dev
  - 3.7-dev
  - nightly
* [pip](https://pypi.python.org/pypi/pip)

## Installation
```shell
$ sudo pip install pdml2flow
```

## Usage
```shell
$ pdml2flow -h
usage: pdml2flow [-h] [--version] [-f FLOW_DEF_STR] [-t FLOW_BUFFER_TIME]
                 [-l DATA_MAXLEN] [-s] [-c] [-a] [-m] [-d] [+json [args]]
                 [+xml [args]]

Aggregates wireshark pdml to flows

optional arguments:
  -h, --help           show this help message and exit
  --version            Print version and exit
  -f FLOW_DEF_STR      Fields which define the flow, nesting with: '.'
                       [default: ['vlan.id', 'ip.src', 'ip.dst', 'ipv6.src',
                       'ipv6.dst', 'udp.stream', 'tcp.stream']]
  -t FLOW_BUFFER_TIME  Lenght (in seconds) to buffer a flow before writing the
                       packets [default: 180]
  -l DATA_MAXLEN       Maximum lenght of data in tshark pdml-field [default:
                       200]
  -s                   Extract show names, every data leaf will now look like
                       { raw : [] , show: [] } [default: False]
  -c                   Removes duplicate data when merging objects, will not
                       preserve order of leaves [default: False]
  -a                   Instead of merging the frames will append them to an
                       array [default: False]
  -m                   Appends flow metadata [default: False]
  -d                   Debug mode [default: False]

Plugins:
  +json [args]         usage: JSON output [-h] [-0] optional arguments: -h,
                       --help show this help message and exit -0 Terminates
                       lines with null character
  +xml [args]          usage: XML output [-h] [-0] optional arguments: -h,
                       --help show this help message and exit -0 Terminates
                       lines with null character
```

## Example
Sniff from interface and write json:
```shell
$ tshark -i interface -Tpdml | pdml2flow +json
```

Read a .pcap file
```shell
$ tshark -r pcap_file -Tpdml | pdml2flow +json
```

Aggregate based on ethernet source and ethernet destination address
```shell
$ tshark -i interface -Tpdml | pdml2flow -f eth.src -f eth.dst +json
```

Pretty print flows using [jq]
```shell
$ tshark -i interface -Tpdml | pdml2flow +json | jq
```

Post-process flows using [FluentFlow]
```shell
$ tshark -i interface -Tpdml | pdml2flow +json | fluentflow rules.js
```

## Plugins

### Create a New Plugin

[![asciicast](https://asciinema.org/a/208963.png)](https://asciinema.org/a/208963)

## Utils

The following utils are part of this project

### pdml2frame
_Wireshark pdml to frames, with plugins_

```shell
$ pdml2frame -h
usage: pdml2frame [-h] [--version] [-s] [-d] [+json [args]] [+xml [args]]

Converts wireshark pdml to frames

optional arguments:
  -h, --help    show this help message and exit
  --version     Print version and exit
  -s            Extract show names, every data leaf will now look like { raw :
                [] , show: [] } [default: False]
  -d            Debug mode [default: False]

Plugins:
  +json [args]  usage: JSON output [-h] [-0] optional arguments: -h, --help
                show this help message and exit -0 Terminates lines with null
                character
  +xml [args]   usage: XML output [-h] [-0] optional arguments: -h, --help
                show this help message and exit -0 Terminates lines with null
                character
```

[python]: https://www.python.org/
[wireshark]: https://www.wireshark.org/
[dict2xml]: https://github.com/delfick/python-dict2xml
[jq]: https://stedolan.github.io/jq/
[FluentFlow]: https://github.com/t-moe/FluentFlow

[Build Status master]: https://travis-ci.org/Enteee/pdml2flow.svg?branch=master
[Coverage Status master]: https://coveralls.io/repos/github/Enteee/pdml2flow/badge.svg?branch=master
[Build Status develop]: https://travis-ci.org/Enteee/pdml2flow.svg?branch=develop
[Coverage Status develop]: https://coveralls.io/repos/github/Enteee/pdml2flow/badge.svg?branch=develop
