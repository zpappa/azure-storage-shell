from azss.vars import context


def cd(*args):

    if args[0].startswith("/"):
        context.cwd = args[0]
        print(context.cwd)
    elif args[0].startswith(".."):

    else:
        context.cwd += "/" + args[0]
        print(context.cwd)
