# ebayfeed

[![Build Status](https://travis-ci.org/alessandrozamberletti/ebayfeed.svg?branch=master)](https://travis-ci.org/alessandrozamberletti/ebayfeed)
[![codecov](https://codecov.io/gh/alessandrozamberletti/ebayfeed/branch/master/graph/badge.svg)](https://codecov.io/gh/alessandrozamberletti/ebayfeed)
[![PyPI version](https://badge.fury.io/py/ebayfeed.svg)](https://badge.fury.io/py/ebayfeed)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Download item feeds from the new eBay RESTful APIs.

**NOTE:** As of Oct.2018 Feed API is supported only on:
* EBAY-DE - eBay Germany (ebay.de)
* EBAY-GB - eBay Great Britain (ebay.co.uk)
* EBAY-US - eBay USA (ebay.com)

Package will be updated as soon as [other](https://developer.ebay.com/api-docs/static/rest-request-components.html#Marketpl) marketplaces are added.
More info [here](https://developer.ebay.com/api-docs/buy/feed/overview.html#API).

# Installation
To install, use `pip` or `easy_install`:

```bash
$ pip install --upgrade ebayfeed
```
or
```bash
$ easy_install --upgrade ebayfeed
```

# Examples

Get all items for 'Travel' (3252) category and convert them to pandas dataframe:
```python
import ebayfeed
from pandas import read_table
from pandas.compat import StringIO

# download tsv feed
credentials = ebayfeed.Credentials(client_id, client_secret)
feed = ebayfeed.get_feed(credentials, 3252, ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.EBAY_US)

# convert to dataframe
df = read_table(StringIO(tsv_feed.splitlines()))
```

Get items listed on 2018-10-03 for 'Toys & Hobbies' (220) category:
```python
import ebayfeed

# download tsv feed
credentials = ebayfeed.Credentials(client_id, client_secret)
feed = ebayfeed.get_feed(credentials, 220, ebayfeed.SCOPE_NEWLY_LISTED, ebayfeed.EBAY_US, date='20181003')
```

Get OAuth 2.0 access token for buy.item.feed scope (cached until expiration):
```python
import ebayfeed

credentials = ebayfeed.Credentials(client_id, client_secret)
access_token = credentials.access_token
```

Connect to eBay sandbox APIs:
```python
import ebayfeed

sandbox_api = ebayfeed.Api(env=ebayfeed.ENVIRONMENT_SANDBOX)
credentials = ebayfeed.Credentials(client_id, client_secret, api=sandbox_api)
```

# References
* eBay API documentation: https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed
* eBay categories map: https://www.isoldwhat.com/
