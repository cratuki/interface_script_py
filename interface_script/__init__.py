import inspect
import shlex

from .parser import parse_line_to_tokens


class LineFinder:
    "At the end of a line, this triggers a callback."

    def __init__(self, cb_line):
        self.cb_line = cb_line
        self.sb = []

    def accept(self, c):
        if c == '\n':
            line = ''.join(self.sb).strip()
            self.cb_line(line)
            self.sb = []
        else:
            self.sb.append(c)


class InterfaceScriptParser(object):

    def __init__(self, handler):
        self.handler = handler

        self.signal_consumer = SignalConsumer(
            handler=self.handler)
        # on_interface(iname, vfields) -> None
        self.cb_interface = self.signal_consumer.on_interface
        # on_signal(iname, values) -> None
        self.cb_signal = self.signal_consumer.on_signal

        self.finder = LineFinder(self._on_line)
        self.interfaces = {}

    def parse(self, s):
        for c in s:
            self.finder.accept(c)

    def _on_line(self, line):
        tokens = parse_line_to_tokens(line)
        if not tokens:
            return
        if tokens[0] == 'i':
            self._handle_interface(tokens)
        else:
            if tokens[0] == '.':
                tokens = tokens[1:]
            self._handle_signal(tokens)

    def _handle_interface(self, tokens):
        if len(tokens) < 2:
            raise Exception("Invalid vdef %s"%str(tokens))
        iname = tokens[1]
        vfields = tokens[2:]
        if iname in self.interfaces:
            # it's fine to have multiple definitions, but they must
            # be consistent.
            current = self.interfaces[iname]
            if vfields != current:
                m = "inconsistent vdefs %s %s"%(
                    str(current),
                    str(vfields))
                raise Exception(m)
        else:
            self.interfaces[iname] = vfields
            self.cb_interface(iname, vfields)

    def _handle_signal(self, tokens):
        iname = tokens[0]
        if iname not in self.interfaces:
            raise Exception("no interface defined for %s"%iname)
        vfields = self.interfaces[iname]
        values = tokens[1:]
        if len(vfields) != len(values):
            raise Exception("wrong number of args. i %s %s. got %s"%(
                iname, str(vfields), str(values)))
        self.cb_signal(iname, values)


class SignalConsumer(object):

    def __init__(self, handler):
        self.handler = handler

    def on_interface(self, iname, vfields):
        method_name = 'on_%s'%iname
        if method_name not in dir(self.handler):
            raise Exception('no handler [%s]'%method_name)
        method = getattr(self.handler, method_name)
        argspec = list(inspect.signature(method).parameters.keys())
        if argspec != vfields:
            raise Exception('inconsistent spec for %s got:%s method:%s'%(
                iname, str(argspec), str(vfields)))

    def on_signal(self, iname, values):
        method_name = 'on_%s'%iname
        if method_name not in dir(self.handler):
            raise Exception('no handler [%s]'%method_name)
        method = getattr(self.handler, method_name)
        method(*values)
