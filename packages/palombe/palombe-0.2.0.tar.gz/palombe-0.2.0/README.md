# Palombe [![PyPI version](https://badge.fury.io/py/palombe.svg)](https://badge.fury.io/py/palombe)

Palombe lets you send and receive messages synchronously through different processes using named pipes

## Quick example

```javascript
import palombe;

palombe.send("foo", "bar");
print(palombe.receive("foo")); // bar
```
