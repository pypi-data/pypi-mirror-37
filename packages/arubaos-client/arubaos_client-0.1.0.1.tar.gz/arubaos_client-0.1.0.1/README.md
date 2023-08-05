# arubaos_client

Install it via

```bash

pip install arubaos_client

```

## Usage

```python

from arubaos_client import MobilityControllerAPIClient

aruba = MobilityControllerAPIClient(
        username='',
        password='',
        url='https://aruba-ac.example.com:4343',
        proxy="socks5h://localhost:5050",
        verify=False
    )

# Login to the device
aruba.login()

# Logout
aruba.logout()

# Get a List of APs
aruba.aps()

# Get amount of 2g clients
aruba.clients(band='2g')
aruba.clients_2g()

# Get amount of 5g clients
aruba.clients(band='5g')
aruba.clients_5g()

# Get AP by its MAC address
aruba.ap_by_mac("00:00:00:00:00:00")

# Get AP by its name
aruba.ap('ap_name')

# Get CPU load
aruba.cpu_load()

# Get Memory usage
aruba.memory_usage()

```