
class STDockerfile:
    def __init__(self):
        self._dockerfile = ''

    def base(self, arg):
        self._dockerfile += 'FROM {}\n'.format(arg)

    def workdir(self, arg):
        self._dockerfile += 'WORKDIR {}\n'.format(arg)

    def add(self, arg1, arg2):
        self._dockerfile += 'ADD {} {}\n'.format(arg1, arg2)

    def cmd(self, arg):
        self._dockerfile += 'CMD {}\n'.format(arg)

    def env(self, name, arg):
        self._dockerfile += 'ENV {} {}\n'.format(name, arg)

    def port(self, arg):
        self._dockerfile += 'PORT {}\n'.format(arg)

    def run(self, arg):
        self._dockerfile += 'RUN {}\n'.format(arg)

    def expose(self, arg):
        self._dockerfile += 'EXPOSE {}\n'.format(arg)

    def to_string(self):
        return self._dockerfile

