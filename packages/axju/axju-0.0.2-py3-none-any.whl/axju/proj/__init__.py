from axju.cls import Basic
import os
#import subprocess
import git

class Projects(Basic):
    """ """
    __version__ = '0.0.1'

    def __init__(self, project='', **kwargs):
        super(Projects, self).__init__(**kwargs)
        self.project = project

    def _list(self):
        l = list()
        for entry in os.scandir(self.settings.get('dirs').get('project')):
            if not entry.name.startswith('.') and entry.is_dir():
                l.append((entry.name, entry.path))
                if self.project == entry.name:
                    return [(entry.name, entry.path)]
        return l

    def list(self):
        """list all project in yourproject folder"""
        print('Project folder:', self.settings.get('dirs').get('project'))

        for entry in self._list():
            print(entry[0])

    def pull(self):
        """update all projects with a git repo"""
        for entry in self._list():
            try:
                repo = git.Repo(entry[1])
                repo.remotes.origin.fetch()
                repo.remotes.origin.pull()
                print('[*]', entry[0])
            except:
                print('[!]', entry[0])

    def push(self, commit=''):
        """push all projects with a git repo"""
        for entry in self._list():
            try:
                repo = git.Repo(entry[1])
                if commit:
                    repo.git.add(update=True)
                    repo.git.add(A=True)
                    author = git.Actor(self.settings.get('name'), self.settings.get('email'))
                    repo.index.commit(commit, author=author)
                    repo.index.commit(commit)
                result = repo.remotes.origin.push()[0]
                print('[*]', entry[0], result.summary[:-1])
            except:
                print('[!]', entry[0])
