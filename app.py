from storage import *

subscribe(12345)
subscribe(67890)

print(load_subscribers())

unsubscribe(12345)

print(load_subscribers())