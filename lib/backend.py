def make_backend(backend_class=None, **args):
    if not backend_class:
        print 'Derp'
        raise Exception('Herp')

    return backend_class(**args)
