from axju.cls import Basic
from axju.__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __url__, __version__
)

import json

__all__ = [
    '__title__', '__summary__', '__url__', '__version__', '__author__',
    '__email__', '__license__', '__copyright__',
]

class AxJu(Basic):
    """This package is designt to optimize my workflow. Maybe you have the same
    and this will help you."""
    __version__ = '0.0.1'

    def _format(self, name):
        return "\nHello I am {},\na software developer from germany. Thane you for install my package.".format(name)

    def me(self):
        """Shows some informations about me"""
        print(self._format(__author__))

    def you(self):
        """If you change the settings, it shows informations about you"""
        print(self._format(self.settings.get('name', __author__)))

    def setup(self):
        """Create the setting file in your home folder"""
        with open(self.SETTINGS_FILE, 'w') as outfile:
            json.dump(self.default_settings, outfile, indent=4)
