import os
from io import TextIOWrapper

from py_mini_racer import py_mini_racer

class ZmeiReactServer(object):
    def __init__(self):
        super().__init__()

        self.loaded_files = []
        self.loaded_files_mtime = {}

        self.jsi = None

        self.checksum = None

    def reload_interpreter(self):
        self.jsi = py_mini_racer.MiniRacer()

        code = """
        var global = this;
        var module = {exports: {}};
        var setTimeout = function(){};
        var clearTimeout = function(){};var console = {
            error: function() {},
            log: function() {},
            warn: function() {}
        };
        """

        self.jsi.eval(code)

        for filename in self.loaded_files:
            self.loaded_files_mtime[filename] = os.path.getmtime(filename)
            self.eval_file(filename)

    def autreload(self):
        if len(self.loaded_files_mtime) == 0:
            return

        for filename in self.loaded_files:
            if self.loaded_files_mtime[filename] != os.path.getmtime(filename):
                print('Reloading ZmeiReactServer')
                self.reload_interpreter()
                break

    def evaljs(self, code):
        if not self.jsi:
            self.reload_interpreter()

        return self.jsi.eval(code)

        # except JSRuntimeError as e:
        #     message = str(e)
        #
        #     message = '\n' + colored('Error:', 'white', 'on_red') + ' ' + message
        #
        #     print(message)
        #     m = re.search('\(line\s+([0-9]+)\)', message)
        #     if m:
        #         print('-' * 100)
        #         print('Source code:')
        #         print('-' * 100)
        #         row = int(m.group(1)) - 1
        #         source = code.splitlines()
        #
        #         line = colored(source[row], 'white', 'on_red')
        #         print('\n'.join([f'{x+1}:\t{source[x]}' for x in range(max(0, row - 10), row)]))
        #         print(f'{row+1}:\t{line}')
        #         print('\n'.join([f'{x+1}:\t{source[x]}' for x in range(row + 1, min(row + 10, len(source) - 1))]))
        #         print('-' * 100)

    def load(self, filename):
        self.loaded_files.append(filename)

    def eval_file(self, filename):
        with open(filename) as f:
            self.evaljs(f.read())
