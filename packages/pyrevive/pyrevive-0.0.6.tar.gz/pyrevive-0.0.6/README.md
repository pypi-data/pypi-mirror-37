# PyRevive
## Revive Hardware Restarter API Library
This Python package is meant for interfacing with the Revive Hardware Restarter HTTP API.  Revive is a hardware restarter and monitor for cryptocurrency mining rigs.

You can find out more and buy one [here](https://revolutionrigs.com/revive)

If you find this library helpful, donations are greatly appreciated:

* Ethereum: 0x7472a4812200fc320793a946f027d559e63b164d
* Ethereum Classic: 0x20282a304c20399b6534cef6196a99978cb89588
* Bitcoin: 1LvnfMGfz8xTaZgi25DiRFaJoFvpAPncT5
* Bitcoin Cash: 1Ec3CPq3WPsWT7fQaDGgTYkVPNtMZ3CVaA
* Litecoin: LSZBbS7EsKnjXQ1FKxYuAmR5quzEazXfm1
* Electroneum: etnk3yDpybAEBqz3nq63qmev4thRi9eFH64CVKzZc2w3A7vehpZkGvd97uSWxtmtAwjTnfKEp9Rup3md7nZyu9Q49VzZQKhxWN


### Installing using PIP
```
pip install pyrevive
```

### Installing from source
```
git clone https://github.com/RevolutionRigs/pyrevive.git
cd pyrevive/
pip install .
````

If you do not want to install using pip you may install using setup.py
```
git clone https://github.com/RevolutionRigs/pyrevive.git
cd pyrevive/
python setup.py install
```

### Importing
```
import pyrevive
```

### Connecting
The connect() method takes two arguments: host[:port], authorizationKey
The authorization key can be found on the bottom of your Revive.

```
revive = pyrevive.connect("192.168.1.254", "authorizationKey")
````

### Version
Get the current version of PyRevive

```
print(revive.__version__)
```

### Power
Perform power on, off, reset functions on a Revive port (aka rig)

#### Power on rig 1
```
revive.power.on(1)
````

#### Power off rig 1
```
revive.power.off(1)
````

#### Power cycle rig 1
All cycle/reset/restart methods are aliases of one another and do the same thing

```
revive.power.cycle(1)
revive.power.reset(1)
revive.power.restart(1)
````

#### Power on rigs 1-16
```
for rig in range(1, 17):
    revive.power.on(rig)
```

### Device
Device specific actions and authorization

#### Device Authorization check
```
revive.device.auth()
```

#### Get Device ID
```
revive.device.id()
```
 
#### Device Hello message (currently returns device ID) 
```
revive.device.hello()
```

### Rig
Rig specific methods: get() and update()

#### Rig.Get
The revive.rig.get() method takes an integer (1-16) as the rig/port number or no argument to get information on all port numbers.  Returns a JSON string with the values.  The API is currently broken on Revive and only port 1 is returned, regardless of which port you specify.

```
# Get information about all ports/rigs
res = revive.rig.get()
print(res)

# Get information about port/rig 1
res = revive.rig.get(1)
print(res)
```

#### Rig.Update
Updates the rig (aka port) with the specified information.  It takes a Python dict as an argument.  Possible fields are:

* port (int, 1-16, required) - physical port which will be updated. We don't have rig id, instead we use this port number
* name (char) - name of the rig
* ip (IP address) - IP address of the rig, used when mode is set to watchdog
* mode (char, manual|watchdog|api)
* maintenance (boolean) - not used for now

```
payload = { "port": 3, "name": "RRMS40U", "ip": "192.168.100.101", "mode": "manual", "maintenance": False }
res = revive.rig.update(payload)
print(res)
```

### Config
Retrieves and sets network and watchdog information on the Revive.

#### Config.Network
The revive.config.network object sets the following read-write variables:

```
* revive.config.network.mode
* revive.config.network.ip
* revive.config.network.netmask
* revive.config.network.gateway
* revive.config.network.primaryDNS
* revive.config.network.secondaryDNS
```

##### Viewing
You can view the current settings in two ways.  Using a helper method show():

```
revive.config.network.show()
```

Or each individual setting:

```
print(revive.config.network.mode)
print(revive.config.network.ip)
print(revive.config.network.netmask)
print(revive.config.network.gateway)
print(revive.config.network.primaryDNS)
print(revive.config.network.secondaryDNS)
```

There is also a dictionary on the network object 'settings' that you can view the settings as well:
```
print(revive.config.network.settings)
```

##### Updating
The individual settings are read-write and can be changed and then saved back to the Revive using the save() method:

```
revive.config.network.show()

revive.config.network.ip = "10.1.1.254"
revive.config.network.netmask = "255.255.255.0"
revive.config.network.gateway = "10.1.1.1"
revive.config.network.primaryDNS = "8.8.8.8"
revive.config.network.secondaryDNS = "8.8.4.4"

res = revive.config.network.save()
print(res)

revive.config.network.show()
```

### Config.Watchdog
The Revive watchdog feature has 3 settings you can modify.  The revive.config.watchdog object has three read-write variables:

```
* revive.config.watchdog.settings
* revive.config.watchdog.pingInterval
* revive.config.watchdog.firstResetAfter
* revive.config.watchdog.anotherResetEvery
```

##### Viewing
You can view the current settings in two ways.  Using a helper method show():

```
revive.config.watchdog.show()
```

Or you can view the settings individually:

```
print(revive.config.watchdog.settings)
print(revive.config.watchdog.pingInterval)
print(revive.config.watchdog.firstResetAfter)
print(revive.config.watchdog.anotherResetEvery)
```

There is also a dictionary on the watchdog object 'settings' that you can view the settings as well:
```
print(revive.config.watchdog.settings)
```

##### Updating
The individual settings are read-write and can be changed and then saved back to the Revive using the save() method:

```
revive.config.watchdog.show()

revive.config.watchdog.pingInterval = "5"
revive.config.watchdog.firstResetAfter = "90"
revive.config.watchdog.anotherResetEvery = "120"

res = revive.config.watchdog.save()
print(res)

revive.config.watchdog.show()
```

