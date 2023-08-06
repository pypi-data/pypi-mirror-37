class network_allowed:
    def __init__(self, *args):
        if args:
            # FIXME: We can probably do better
            raise SyntaxError(
                'Please call the decorator as follows:\n\n'
                '@network_allowed()\n'
                'def {args[0].__name__}:\n'
                '    ...'.format(args=args))

    def __call__(self, func):
        func._network_allowed = True

        return func


class read_only:
    def __init__(self, *dirs):
        self._dirs = list(dirs)

    def __call__(self, func):
        try:
            func._read_only_dirs.extend(self._dirs)

        except AttributeError:
            # First time the function is decorated by this
            func._read_only_dirs = self._dirs

        return func
