ref = {
    'operator': {
        '^': {'precedence': 3, 'associativity': 'right'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'},
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
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
        'log_': {'ftype': 'log'},

        'arcsin': {'ftype': 'inv trig'},
        'arccos': {'ftype': 'inv trig'},
        'arctan': {'ftype': 'inv trig'},
        'arccosec': {'ftype': 'inv trig'},
        'arcsec': {'ftype': 'inv trig'},
        'arccot': {'ftype': 'inv trig'},

        'sin': {'ftype': 'trig'},
        'cos': {'ftype': 'trig'},
        'tan': {'ftype': 'trig'},
        'cosec': {'ftype': 'trig'},
        'sec': {'ftype': 'trig'},
        'cot': {'ftype': 'trig'},

        

    }
}
