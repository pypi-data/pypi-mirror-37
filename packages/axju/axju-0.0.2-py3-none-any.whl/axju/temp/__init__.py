from axju.cls import Basic

class Templates(Basic):
    """docstring for ProjectTemplates."""

    def __init__(self, **kwargs):
        super(ProjectTemplates, self).__init__(**kwargs)

        self.settings = kwargs.get('settings', {})

    def __templates(self):
        return self.settings.get('templates', [])

    def show(self):
        """Show the posible templates."""
        for t in self.__templates():
            print(t)
