commands = {
    'init_db': {
        'short': 'idb',
        'description': 'after deployment, also initialize the database and schema.',
        'const': True,
        'default': False,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    }
}