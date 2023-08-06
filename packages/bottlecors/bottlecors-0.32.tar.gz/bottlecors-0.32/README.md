BottleCors
===========


`pip install bottlecors` and then

```python
from bottle import Bottle
from bottlecors import add_cors, abort


app = Bottle()

@app.get('/')
def home():
    "This just shows 404 always"
    abort(404, 'msg')

# Cors needs to be added after
# all routes have been added to your app
app = add_cors(app)
```

Features
--------

- Full blown cors
- Sends docstring of function in options body
- Adds only for routes which have already been added
