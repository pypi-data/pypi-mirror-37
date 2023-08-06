from .lowlevel import *
from .pattern import Pattern
import os

floats = {}


class Lifetree(object):

    def __init__(self, session, memory=1000, n_layers=1):

        self.session = session
        lifelib = session.lifelib
        self.lifelib = lifelib
        self.ptr = lifelib('CreateLifetree', memory, n_layers)
        self.n_layers = n_layers

    def load(self, filename, compressed='deduce', tempfile='tempfile'):

        filename = os.path.abspath(filename)

        if not os.path.isfile(filename):
            raise OSError("%s does not exist or is not a regular file" % filename)

        if compressed == 'deduce':
            compressed = (filename[-3:] == '.gz')

        if compressed:
            import gzip
            import shutil
            with gzip.open(filename, 'rb') as f_in:
                with open(tempfile, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            pptr = self.lifelib('CreatePatternFromFile', self.ptr, tempfile)
            try:
                os.remove(tempfile)
            except OSError:
                pass
        else:
            pptr = self.lifelib('CreatePatternFromFile', self.ptr, filename)

        return Pattern(self.session, pptr, self)

    def viewer(self, filename=None, width=480, height=480,
                lv_config='#C [[ THEME 6 GRID GRIDMAJOR 0 ]]'):

        if filename is None:
            filename = self.session.newfloat('viewer') + '.html'


    def pattern(self, rle, rule=None, tempfile='tempfile'):

        tempfile = os.path.abspath(tempfile)

        if ('=' in rle) or ('[' in rle):
            # Headerful RLE/MC; save and reload:
            with open(tempfile, 'w') as f:
                f.write(rle)
            pptr = self.lifelib('CreatePatternFromFile', self.ptr, tempfile)
            try:
                os.remove(tempfile)
            except OSError:
                pass
        else:
            # Headerless RLE:
            if rule is None:
                if len(self.session.rules) == 1:
                    rule = self.session.rules[0]
                else:
                    raise TypeError("For headerless RLE, rule must be specified unless session has a unique rule")

            rule = rule.lower()

            self.session.verify_rule(rule)
            pptr = self.lifelib('CreatePatternFromRLE', self.ptr, rle, rule)

        return Pattern(self.session, pptr, self)

    def __del__(self):

        self.lifelib('DeleteLifetree', self.ptr)

class Session(object):

    def newfloat(self, name):

        if name not in floats:
            floats[name] = 0

        floats[name] += 1
        return ('%s%d' % (name, floats[name]))

    def __init__(self, soname, rules=['b3s23'], local_bash=None, local_python='python'):

        self.rules = list(rules)
        self.lifelib = WrappedLibrary(soname, local_bash=local_bash, local_python=local_python)

    def lifetree(self, *args, **kwargs):

        return Lifetree(self, *args, **kwargs)

    def verify_rule(self, rule):

        if (len(rule) > 7) and (rule[-6:] == 'istory'):
            rule = rule[:-7]

        if rule not in self.rules:
            raise ValueError("Rule %s is not in the configured rules %s for this session" % (rule, self.rules))

