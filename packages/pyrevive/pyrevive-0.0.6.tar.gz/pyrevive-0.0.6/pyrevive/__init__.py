import json
import requests

VERSION = "0.0.6"
METHODS = [ "GET", "POST", "PATCH" ] # Allowed HTTP methods

def connect(host, key):
    """Initializes Revive API object"""
    return Revive(host, key)

class Revive:
    """
    Revive API parent class.
    """

    def __init__(self, host, key):
        """
        Revive API parent class.  Takes two arguments to initialize:
            host[:port]   : Hostname/IP and optional port
            key           : Revive authorization key found on bottom of deviceSubclasses provided:

        Creates sub-classes:
            revive.rig    : Rig()
            revive.power  : Power()
            revive.config : Config()
            revive.device : Device()
        """

        global url
        global headers

        self.host = host
        self.key  = key
        self.url  = "http://" + host

        self.headers     = { "Authorization": "Bearer " + self.key, "Content-Type": "application/json" }
        self.__version__ = VERSION

        url = "http://" + host
        headers = { "Authorization": "Bearer " + self.key, "Content-Type": "application/json" }

        self.device = self.Device()

        # Preform an auth test to make sure the device key is right
        check = self.device.auth()
        if "message" in check:
            raise Exception(check["code"], check["message"])

        self.rig    = self.Rig()
        self.power  = self.Power()
        self.config = self.Config()


    class Connect:
        """Revive Connect class for use in subclasses"""

        @staticmethod
        def request(method, uri, payload=""):

            # GET, POST, PATCH
            if method not in METHODS:
                raise Exception("Unsupported HTTP method: " + method)

            #print("%s -> %s -> %s -> %s") % (method, url + uri, payload, headers)

            try:
                response = requests.request(method, url + uri, data=payload, headers=headers)
                parsed   = json.dumps(json.loads(response.text), indent=2, sort_keys=True)
            except:
                raise Exception

            return parsed


    class Power(Connect):
        """
        Revive API for power on/off/restart to ports.  Provides methods:
            port - Integer 1-16
                revive.reset(port)
                revive.cycle(port)
                revive.restart(port)
                revive.on(port)
                revive.off(port)
        """

        def reset(self, port):
            """Restart rig"""
            payload = json.dumps({ "port": int(port) })
            request = self.request("POST", "/v1/api/restarter/reset", payload)

            return request

        def restart(self, port):
            """Restart rig"""
            self.reset(port)

        def cycle(self, port):
            """Restart rig"""
            self.reset(port)

        def on(self, port):
            """Power rig ON"""
            payload = json.dumps({ "port": int(port) })
            request = self.request("POST", "/v1/api/restarter/on", payload)

            return request

        def off(self, port):
            """Power rig OFF"""
            payload = json.dumps({ "port": int(port) })
            request = self.request("POST", "/v1/api/restarter/off", payload)

            return request


    # Revive.Device Class
    class Device(Connect):
        """
        Revive API device calls:

            Provides methods:
                revive.device.auth()
                revive.device.id()
                revive.device.hello()
        """

        def auth(self):
            """Check Revive Device key"""
            payload = json.dumps({ "login": True })
            return json.loads(self.request("POST", "/v1/api/device/auth", payload))

        def id(self):
            """Get Revive Device ID"""
            return self.request("GET", "/v1/api/device/id")

        def hello(self):
            """Get Revive Welcome Message"""
            return self.request("GET", "/v1/api/device/hello")


    class Rig(Connect):
        """
        Revive API rig update object.  Provides:
            revive.rig.update(payload)
            revive.rig.get()
        """

        def update(self, payload):
            """
            Updates the port information.  Takes a dictionary as input.  Possible fields are:

                port (int, 1-16, required) - physical port which will be updated. We don't have rig id, instead we use this port number
                name (char)                - Name of the rig
                ip (IP address)            - IP address of the rig, used when mode is set to watchdog
                maintenance (boolean)      - Not used for now
                mode (char, manual|watchdog|api)


                payload = { "port": 1, "name": "RIG #1", "ip": "192.168.1.1", "mode": "watchdog", "maintenance": false }

            """

            # Convert dict to JSON for the PATCH request
            payload = json.dumps(payload)
            request = self.request("PATCH", "/v1/api/rig/update", payload)
            return request

        def get(self, port="all"):
            """
            Revive API rig information fetcher

                Expects:
                    No argument or "all": Pulls info on all ports
                    Integer 1-16: Pulls the information for that port
            """
            # Port must be "all" or an integer 1-16
            if port not in range(1,17) and port != "all":
                error = "Invalid port '%s'.  Valid ports: all, 1-16" % port
                raise Exception(error)

            # Get all port information
            if port == "all":
                api = "/v1/api/rig/get/"

            # Get a single port's information
            else:
                api = "/v1/api/rig/get/" + str(port)

            request  = self.request("GET", api)
            settings = json.loads(request)

            # Set the self.settings to the JSON parsed dictionary
            self.settings = settings["data"]

            return request


    # Revive.Config Class
    class Config(Connect):
        """
        Revive API configuration class

            Creates subclasses:
                revive.config.network
                revive.config.watchdog
        """

        def __init__(self):
            self.settings = self.settings()     # All settings from Revive
            self.network  = self.Network(self)  # revive.config.network class
            self.watchdog = self.Watchdog(self) # revive.config.watchdog class

        def settings(self):
            # GET /v1/api/config/get
            request  = self.request("GET", "/v1/api/config/get")
            settings = json.loads(request)

            # Everything we care about is under data: { }
            return settings["data"]


        # Revive.Config.Network Class
        class Network:
            """
            Revive API network configuration:

                Sets variables:
                    revive.config.network.settings     [dictionary]

                    revive.config.network.mode         [string/rw]
                    revive.config.network.ip           [string/rw]
                    revive.config.network.netmask      [string/rw]
                    revive.config.network.gateway      [string/rw]
                    revive.config.network.primaryDNS   [string/rw]
                    revive.config.network.secondaryDNS [string/rw]
            """

            # Initialize with the network settings pulled from parent class
            def __init__(self, parent):
                self.parent       = parent
                self.settings     = self.parent.settings["network"]

                self.mode         = self.settings["mode"]
                self.ip           = self.settings["ip"]
                self.netmask      = self.settings["netmask"]
                self.gateway      = self.settings["gateway"]
                self.primaryDNS   = self.settings["primaryDNS"]
                self.secondaryDNS = self.settings["secondaryDNS"]

            # Writes all settings back to the Revive via a PATCH request
            # revive.config.network.save()
            def save(self, settings=False):
                """Write all of the network settings back to the device"""

                # Accept either: dhcp or manual
                if self.mode.lower() not in [ "dhcp", "manual" ]:
                    raise Exception("Invalid mode.  Valid modes: dhcp, manual")

                # Simple JSON if we are doing DHCP
                if self.mode.lower() == "dhcp":
                    settings = json.dumps({ "network": { "mode": "dhcp" } })

                # Build out the dict with the settings
                else:
                    settings = {
                        "network": {
                            "mode": "manual",
                            "ip": self.ip,
                            "netmask": self.netmask,
                            "gateway": self.gateway,
                            "primaryDNS": self.primaryDNS,
                            "secondaryDNS": self.secondaryDNS
                        }
                    }

                    # Then convert it to JSON for the PATCH request to the API
                    settings = json.dumps(settings)

                # PATCH to /v1/api/config/update with JSON settings payload
                request = self.parent.request("PATCH", "/v1/api/config/update", settings)

                return request



            # Print out the Revive network settings all pretty like
            def show(self):
                """Show the Revive network settings"""
                print("mode:         " + self.mode)
                print("ip:           " + self.ip)
                print("netmask:      " + self.netmask)
                print("gateway:      " + self.gateway)
                print("primaryDNS:   " + self.primaryDNS)
                print("secondaryDNS: " + self.secondaryDNS)


        class Watchdog:
            """
            Revive API watchdog configuration:

                Sets variables:
                    revive.config.watchdog.settings          [dictionary]

                    revive.config.watchdog.pingInterval      [integer/rw]
                    revive.config.watchdog.firstResetAfter   [integer/rw]
                    revive.config.watchdog.anotherResetEvery [integer/rw]
            """

            # Initialize with the watchdog settings pulled from parent class
            def __init__(self, parent):
                self.parent            = parent
                self.settings          = self.parent.settings["watchdog"]

                self.pingInterval      = self.settings["pingInterval"]
                self.firstResetAfter   = self.settings["firstResetAfter"]
                self.anotherResetEvery = self.settings["anotherResetEvery"]

            # Writes all settings back to the Revive via a PATCH request
            # revive.config.watchdog.save()
            def save(self):
                """Write all of the watchdog settings back to the device"""

                test = { "pingInterval": self.pingInterval, "firstResetAfter": self.firstResetAfter, "anotherResetEvery": self.anotherResetEvery }

                # Test and make sure that all settings are integers
                for key, val in test.iteritems():
                    if not isinstance(val, int):
                        error = "%s value '%s' is not an integer." % (key, val)
                        raise Exception(error)

                # Create a dictionary with the watchdog settings
                settings = {
                    "watchdog": {
                        "pingInterval": int(self.pingInterval),
                        "firstResetAfter": int(self.firstResetAfter),
                        "anotherResetEvery": int(self.anotherResetEvery)
                    }
                }

                # Then convert it to JSON for the PATCH request to the API
                settings = json.dumps(settings)

                # PATCH to /v1/api/config/update with JSON settings payload
                request = self.parent.request("PATCH", "/v1/api/config/update", settings)

                return request



            # Print out the Revive network settings all pretty like
            def show(self):
                """Show the Revive watchdog settings"""
                print("pingInterval:      " + str(self.pingInterval))
                print("firstResetAfter:   " + str(self.firstResetAfter))
                print("anotherResetEvery: " + str(self.anotherResetEvery))


# EOF
