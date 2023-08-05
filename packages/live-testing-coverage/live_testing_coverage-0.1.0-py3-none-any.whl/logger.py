class Logger(object):

    def __init__(self):
        self.log = ''

    def info(self, message):
        self.log += 'COVERAGE INFO-{}\n'.format(message)

    def debug(self, message):
        self.log += 'COVERAGE DEBUG-{}\n'.format(message)

    def terminal_summary(self, terminalreporter):
        terminalreporter.write(self.log)