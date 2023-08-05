# Rainbow Bridge Logger

A wrapper for the native logging module of Python.

## Usage

```python
from rainbow import RainbowLogger

# __name__ will get the current context
# but you can pass any text you want, for identification
logger = RainbowLogger(__name__)

logger.info('my info')
logger.warning('my warn')
logger.error('my error')
logger.debug('my debug')
```

Which should output the following:

![Output for logger](/res/rainbow-logger-output.png)

## Todo

- [ ] Improve possible arguments to be passed
- [ ] Add capability for custom formats and coloring
- [ ] Improve pathing for module
- [ ] Allow easy integration with other frameworks that uses logging
- [ ] Publish to pip to be usable anywhere
- [ ] Create installation section
- [x] Improve README
- [x] Create usage section

## Author

- Almer T. Mendoza
