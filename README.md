# Mock OPC UA Server

This application allows declaring multiple OPC UA servers with randomly changing variables. To configure this application create a copy of the example config file.

```bash
cp config.json.example config.json
```

Application can be run using:

```bash
python src/main.py
```

## Config file

The following is an explanation of the config file structure.

```jsonc
{
    // Optional schema reference for IDE autocomplete
    "$schema": "./config-schema.json",
    // List of namespace URIs to be referenced in object and variable declarations.
    // Namespaces are referenced using their index, starting from 0.
    "namespaces": [
        "http://example.com"
    ],
    // Create a object for each server you want to create. All servers run on the 0.0.0.0 endpoint.
    "servers": [
        {
            // The port 4840 is default for OPC UA servers, but you must specify other ports for multiple servers.
            "port": 4840,
            // Forms the path of the server endpoint
            "path": "example/server",
            "objects": [
                {
                    "ns": 0,
                    // Specify the browse name for this object
                    "name": "MyObject",
                    "variables": [
                        {
                            "ns": 0,
                            // Specify the browse name for this variable
                            "name": "MyVariable",
                            // Variable values are periodically set to a random value between min and max.
                            "min": 0,
                            "max": 1
                        }
                    ]
                }
            ]
        }
    ]
}
```
