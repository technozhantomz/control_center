# Gateways API
REST API for BitShares blockchain gateway

[![License]][LICENSE]
[![Telegram]][Telegram join]
![build](https://github.com/fincubator/control_center/workflows/build/badge.svg)
[![Code style: black]][black code style]

REST API for BitShares gateways system between [Booker] and [BitSharesUI]

## Install
### Linux (Ubuntu 18.04)
#### Install with Docker
##### Requirements
* [Docker]
* [Docker Compose]

Install dependencies
```shell script
$ sudo apt install git docker.io docker-compose
```

Clone the repository:
```shell script
$ git clone https://github.com/fincubator/control_center
$ cd control_center/
$ cp .env.example .env
```

Start the services by running the command:
```shell script
$ sudo docker-compose up --build
```

# License
Control Center is released under the GNU Affero General Public License v3.0. See
[LICENSE.md] for the full licensing condition


[License]: https://img.shields.io/github/license/fincubator/control_center
[LICENSE]: LICENSE
[CONTRIBUTING.md]: CONTRIBUTING.md
[Telegram]: https://img.shields.io/badge/Telegram-fincubator-blue?logo=telegram
[Telegram join]: https://t.me/fincubator
[Docker]: https://www.docker.com
[Docker Compose]: https://www.docker.com
[Booker]: https://github.com/fincubator/booker
[BitSharesUI]: https://github.com/bitshares/bitshares-ui
[Code style: black]: https://img.shields.io/badge/code%20style-black-000000.svg
[black code style]: https://github.com/psf/black