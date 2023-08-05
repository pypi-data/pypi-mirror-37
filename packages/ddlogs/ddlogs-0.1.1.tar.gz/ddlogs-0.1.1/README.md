ddlogs
=======

[![Version](https://img.shields.io/pypi/v/ddlogs.svg)](https://pypi.python.org/pypi/ddlogs)

# Description

Datadog logs logging handler and utilities.

# Requirements

- Python3.6 or higher
- pip

# Installation

## PyPI

```sh
pip install ddlogs
```

# Usage

```python
import logging
import ddlogs

logger = logging.getLogger('test')
h = ddlogs.DatadogLogsHandler(
    api_key='your-datadog-api-key',     # default: os.environ.get('DD_API_KEY')
    source_category='samplecategory',   # default: "ddlogs"
    source='samplesource',              # default: "python"
    service='sampleservice',            # default: logger.name
    host='localhost')                   # default: gethostname()
h.setFormatter(ddlogs.DictFormatter())
logger.addHandler(h)
logger.error({'foo': 'bar'})
```

# Output
![screenshot](https://raw.githubusercontent.com/marcy-terui/ddlogs/master/images/screenshot.png)

Development
-----------

-   Source hosted at [GitHub](https://github.com/marcy-terui/ddlogs)
-   Report issues/questions/feature requests on [GitHub
    Issues](https://github.com/marcy-terui/ddlogs/issues)

Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1.  Fork the repo
2.  Create your feature branch (`git checkout -b my-new-feature`)
3.  Commit your changes (`git commit -am 'Added some feature'`)
4.  Push to the branch (`git push origin my-new-feature`)
5.  Create new Pull Request

Authors
-------

Created and maintained by [Masashi Terui](https://github.com/marcy-terui) (<marcy9114@gmail.com>)

License
-------

MIT License (see [LICENSE](https://github.com/marcy-terui/ddlogs/blob/master/LICENSE))
