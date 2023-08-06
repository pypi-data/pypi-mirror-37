import time

from funtime import Store



store = Store().create_lib("hello.World").get_store()

# Insert dogshit
store['hello.World'].store({
    "type": "price",
    "currency": "ETH_USD",
    "timestamp": time.time(),
    "candlestick": {
        "open": 1234,
        "close": 1234.41,
        "other": "etc"
    }
})

runs = store['hello.World'].query({
    "type": "price"
})


# returning some shit
for r in runs:
    print(r)


def create_library():
    pass

def store_items():
    pass

def query_item():
    pass

def access_item():
    pass