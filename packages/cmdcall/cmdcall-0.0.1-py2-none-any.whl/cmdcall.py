#!/usr/bin/env python

import sys
import inspect

def parse_args(args, parse_int=False):
    if len(args) == 0:
        raise RuntimeError("no function name specified")

    fn_name = args[0]
    positional_args = []
    kwargs = {}

    i = 1
    while i < len(args):
        arg = args[i]
        if arg.startswith("--"):
            if arg == "--":
                positional_args.extend(args[i + 1:])
                break
            else:
                if i == len(args) - 1:
                    raise RuntimeError(
                            "args formate error, expect value arg followed by arg starts with --. Args after `--` are treat as positional args")
                kwargs[arg[2:]] = args[i + 1]
                i += 2
        else:
            positional_args.append(arg)
            i += 1
    return fn_name, positional_args, kwargs


def handle(module, args=sys.argv[1:], parse_int=False):
    """ main entry of cmdcall module, call this handle with module you want to be able to call """
    all_fns = dict(inspect.getmembers(module, inspect.isfunction))

    fn_name, positional_args, kwargs = parse_args(args, parse_int=parse_int)

    if fn_name not in all_fns:
        raise RuntimeError("no {} found in module {}, available: {}".format(
            fn_name, module.__file__, all_fns.keys()))

    return all_fns[fn_name](*positional_args, **kwargs)

if __name__ == '__main__':
    pass
