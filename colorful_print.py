class ColorfulPrint(object):# {{{

    """Docstring for ColorfulPrint. """

    def __init__(self):
        """nothing needs to be define """
        self.colors = {
            'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
            'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37,
        }

    def trans(self, *args, auto_close=True):
        s = ' '.join(map('{}'.format, args))
        s = s.replace('(##)', '\033[0m')
        s = s.replace('(#)', '\033[0m')
        for color, value in self.colors.items():
            color_tag = '(#%s)'%color
            s_color_tag = '(#%s)'%color[0]
            s = s.replace(color_tag, '\033[1;%d;m'%value).\
                    replace(s_color_tag, '\033[1;%d;m'%value)
        if auto_close:
            s = s + '\033[0m'
        return s

    def err(self, *args):
        return self('(#r)[ERR](#)', *args)

    def log(self, *args):
        return self('(#blue)[LOG](#)', *args)

    def wrn(self, *args):
        return self('(#y)[WRN](#)', *args)

    def suc(self, *args):
        return self('(#g)[SUC](#)', *args)

    def __call__(self, *args):
        print(self.trans(*args))

cp = ColorfulPrint()
# }}}

