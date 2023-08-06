# unifi_client

Install it via

```bash

pip install unifi_client

```

## Usage

```python

from unifi_client import AirMaxAPIClient

unifi = AirMaxAPIClient(
    url="https://air.max.example.com",
    username="username",
    password="password",
    verify=False,
    proxy="socks5h://localhost:5050"
    )

unifi.login() # Login to device

unifi.statistics() # Get all the statistics from device

unifi.logout() # Logout from device
```