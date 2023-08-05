from axju.cls import Basic

class Alias(Basic):
    """Some alias."""

    def __init__(self, **kwargs):
        super(Alias, self).__init__(**kwargs)

        self.alias = self.get('alias', {})

    def run(self, name):
        """execute the alias"""
        if name not in self.alias:
            print('Alias "{}" not found'.format(name))
            return False

        for cmd in self.alias[name]['linux']:
            subprocess.call([cmd, ], shell=True)#self.alias[name]['linux'], shell=True)

    def show(self):
        for arg in self.alias:
            print(arg)
