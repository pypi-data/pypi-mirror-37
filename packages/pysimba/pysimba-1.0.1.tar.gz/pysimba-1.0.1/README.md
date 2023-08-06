# pysimba

## Getting Started

### Installing

```
pip install pysimba
```

### Creating Client

```
from pysimba import Client

client = Client(app_id=os.getenv('CLIENT_APP_ID'), app_secret=os.getenv('CLIENT_APP_SECRET'), service_url=os.getenv('CLIENT_SERVICE_URL'))
```

### Enable Logging

```
import logging

logging.basicConfig(level=logging.INFO)
```

### Useful Utils

```
from pysimba import get, batch, strptime
```

#### get

Like ```dict.get``` but more ```deep```.

```
get(r, path='simba_insight_wordsdata_get_response.word_data_list.insight_word_data_d_t_o', default=[])
```

#### batch

Batch lets you divide an iterable (currently, last positional argument) of work into pieces.

```
@batch(100)
def summary(texts):
    r = client.call('taobao.simba.insight.wordsdata.get', params={
        'bidword_list': ','.join(texts),
        'start_date': '2018-10-01',
        'end_date': '2018-10-07'
    })
    return get(r, path='simba_insight_wordsdata_get_response.word_data_list.insight_word_data_d_t_o', default=[])

texts = [f'连衣裙 {x}' for x in range(200)]
results = summary(texts)
```

#### strptime

Converting date string to datetime, timezone='Asia/Shanghai'.

```
strptime('2018-10-16 21:00:50')
```

### Calling

```
r = client.call('taobao.simba.campaigns.get', token='CUSTOMER_TOKEN_HERE')
results = get(r, path='simba_campaigns_get_response.campaigns.campaign')
```
