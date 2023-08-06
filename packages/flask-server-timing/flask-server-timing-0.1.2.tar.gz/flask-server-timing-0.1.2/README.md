# Flask Server-Timing Header Extension

A Flask extension to easily add the Server-Timing header to allow supported browsers to show backend performance metrics.

From the [Mozilla Developer site](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing):

> The Server-Timing header communicates one or more metrics and descriptions for a given request-response cycle. It is used to surface any backend server timing metrics (e.g. database read/write, CPU time, file system access, etc.) in the developer tools in the user's browser


The Server-Timing specification is a [W3C draft](https://www.w3.org/TR/server-timing)

## Installation

```
pip install flask-server-timing
```

Python versions 2.7 and 3.x are supported with Flask from version 0.10.1.

## Browser Support

Generally all newer, major browsers - excluding IE and Safari - support visualizing the Server-Timing header. For an up-to-date list with specific versions see the [Mozilla Developer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing#Browser_compatibility) site

## Usage

```python
from flask import Flask
import time

# Import extension
from from server_timing import Timing

app = Flask(__name__)

# To initialize the extension simply pass the app to it. If the app is in debug
# mode or the force_debug parameter is True an after-request handler will be added
# to write the actual header.
t = Timing(app, force_debug=True)


@app.route("/examples")
def examples():
    # explicitly calling start and stop before and after - keys need to be identical
    t.start('done and done')
    time.sleep(0.3)
    t.stop('done and done')

    # context manager support to avoid having to call start and stop explicitly
    with t.time('context'):
        time.sleep(0.2)

    # decorated with name being the key
    named_decoration()
    # decorated without name so the function is the key
    unnamed_decoration()

@t.timer(name='named')
def named_decoration():
    time.sleep(0.4)

@t.timer
def unnamed_decoration():
    time.sleep(0.5)


app.run(host="0.0.0.0",port=8080)
```

The `example/` directory also contains the following file showing how to time functions in other modules:

```python
import time

# before this file is imported make sure the extension has been initialized with the Flask app
from server_timing import Timing as t


@t.timer
def include():
    time.sleep(0.1)
```
