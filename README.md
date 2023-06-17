# gungnir

<div align="center">

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GeekMasher/gungnir)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/geekmasher/gungnir/python-package.yml?style=for-the-badge)](https://github.com/GeekMasher/gungnir/actions/workflows/python-package.yml?query=branch%3Amain)
[![GitHub Issues](https://img.shields.io/github/issues/geekmasher/gungnir?style=for-the-badge)](https://github.com/GeekMasher/gungnir/issues)
[![GitHub Stars](https://img.shields.io/github/stars/geekmasher/gungnir?style=for-the-badge)](https://github.com/GeekMasher/gungnir)
[![Python Versions](https://img.shields.io/pypi/pyversions/gungnir?style=for-the-badge)](https://pypi.org/project/gungnir/)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

</div>

## Overview

Gungnir is a Homelab Automation Bot to Guard your very own Asgard from the dangerous world of out of date components.

## Usage

### CLI

**Requirements:**

- Python 3.9+
- [Syft](https://github.com/anchore/syft) (generate bill of materials)


**Help:**

```bash
python -m gungnir --help
```

```
Gungnir - Homelab Automation Bot to Guard your very own Asgard

options:
  -h, --help            show this help message and exit
  --debug               Enable Debug mode
  --banner              Show banner
  --version             Show version
  --container           Enable container mode
  --disable-banner      Disable banner
  --hostname HOSTNAME   Hostname (mainly for containers)
  -t TOKEN, --token TOKEN
                        DependencyTrack Token
  -i INSTANCE, --instance INSTANCE
                        DependencyTrack Instance
```

### Docker-Compose

Download the [`docker-compose.yml` example](./docker-compose.yml) and run with the following command:

```bash
docker-compose up
```

**Environment Variable:**

```env
DEPENDENCYTRACK_URL=http://localhost:9090
DEPENDENCYTRACK_TOKEN=ABCD...
```

## License

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE) for the full terms.

## Support

Please create issues for any feature requests, bugs, or documentation problems.

## Acknowledgement

- @GeekMasher - Author and Maintainer

