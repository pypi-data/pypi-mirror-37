import os, json

class Basic(object):
    """This is the basic class for all my tools"""

    SETTINGS_FILE = os.path.join(os.path.expanduser('~'), '.axju')

    default_settings = {
        'name': 'Axel Juraske',
        'email': 'axel.juraske@short-report.de',
        'www': 'axel.short-report.de',
        'dirs': {
            'project': '~/projects',
            'backup': '~/backups',
        },
        'progs': {
            'git': {},
            'thundbird': {},
            'atom': {
                'linux':[ {'cmd': ['sudo add-apt-repository ppa:webupd8team/atom', 'sudo apt update', 'sudo apt install atom']}],
                'win': [{'exe': 'https://atom.io/download/windows_x64'}],
            },
        },
        'templates': {
            'pyPackage': [
                {'file': 'README.rst', },
                {'file': 'setup.py', 'content': """ """},
                {'file': '{{ packege_name }}/__init__.py'}
            ]
        },
        'alias': {
            'update': {'linux': ['sudo apt update', 'sudo apt upgrade -y', 'sudo apt autoremove -y']},
        }
    }

    def __init__(self, **kwargs):
        self.settings = kwargs.get('settings', self.default_settings)

        if kwargs.get('load', False) and os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE) as data_file:
                self.settings = json.load(data_file)
