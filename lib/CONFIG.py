ref = {
    'operator': {
        '^': {'precedence': 3},
        '*': {'precedence': 2},
        '/': {'precedence': 2},
        '+': {'precedence': 1},
        '-': {'precedence': 1},
    },

    'brackets': {
        '(': ')', 
    },

    'const': ['pi', 'e'],

    'dtype': {
        'leaf': 'leaf',
        'optr': 'operator',
        'fn': 'function',
        'complex': 'complex'
    },

    'function': {
        'log_': {},

        'sin': {},
        'cos': {},
        'tan': {},
        'cosec': {},
        'sec': {},
        'cot': {}
    }
}
