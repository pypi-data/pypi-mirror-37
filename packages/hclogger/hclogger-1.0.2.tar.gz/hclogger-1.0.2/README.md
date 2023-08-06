## Hierarchical Colored Logger Module for Python

HCLogger is a logging module using [Termcolor](https://pypi.org/project/termcolor/) and a hierarchical format to improve readability.

Note: this module was designed to deal with concurrency. However, it is encouraged to store thread logs into different log files.

![HCLogger capture](hclogger/tests/function_test.png)

### Installation

Not yet in PyPi.

### Usage

As simple as it could be:

```python
from HCLogger import Logger

logger = Logger(filename='fname.log', verbose=False)
logger.debug('This is a debug message.')
```

Output:

![Debug output](hclogger/tests/debug_message.png)

The hierarchy is added to functions. In order to add hierarchy on of the following alternatives must be used:

```python
# The manual call
logger.manual_log_func(func, args*)

# The decorated call
@logger.log_func
def func(args):
	...

func()
```

Output:

![Function logging](hclogger/tests/function_log.png)

Putting it all together:

![Demo capture](hclogger/tests/demo_capture.png)

## Future work

 - [ ] Add to PyPi
 - [ ] Create web view
