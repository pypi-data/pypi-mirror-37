### Class EventManager: 

provide event sending and listening.
use a hashable key to identify an event.

```python
def f(data):
    print data

manager = EventManager()
manager.start() # start listen

manager.addListener(key='evnet_key', listener=f)

manager.sendEvent(key='evnet_key', data={msg:'hello'})


# other methods
manager.removeListener(key='evnet_key', f)
manager.stop() # stop listen
manager.clear() # clear event
```


