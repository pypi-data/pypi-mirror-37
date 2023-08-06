# nats-publish

Minimal go-nats protocol publish-only client written in python.

## Example

```py
from nats_publish import NatsPublish

np = NatsPublish(conn_options={
            "hostname": "demo.nats.io",
            "port": 4222,
        })
np.publish('hello world')
```