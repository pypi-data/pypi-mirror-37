# mothership-client

The official Python client for [Mothership](https://mothership.cloud).

## Installation
```
pip3 install mothership-client
```

## Requirements
- Python 3

## Usage
Since most configuration values are needed during intial bootstrap of an app, this
module should probably be one of the first things your code imports.

Import the module, then initialize it using your environment key.

```
import mothership.client
config = mothership.client.init({
  'key': '<config-key>'
});
```

Then simply reference your config like: `config['someKey']`;

When you need config in another module, simply import the `mothership` module and 
call `mothership.get()` to grab the entire config:

```
import mothership
config = mothership.get();
```

For more info, see [our documentation](https://docs.mothership.cloud).
