prism_rest_client README
==================

This client library is meant for interacting with REST APIs implemented using
the prism_rest library. It may work with other REST APIs as well, but has not
been tested against such.

Getting Started
---------------

    >>> import prism_rest_client
    >>> api = prism_rest_client.open('http://example.com/api')
    >>>
    >>> distros = dict(((x.name, x.version), x) for x in api.distros)
    >>>
    >>> distro = distros.get(('centos', 6))
    >>>
    >>> pkgs = distro.query('packages', name='bash')
    >>>
    >>> assert pkgs[0].nevra.name == 'bash'
