""" 
Exemplo provisório enquanto não construímos a tabela SLR
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import core.LR_parsing as lr_parsing

""" Gramática 
(0) S' → S
(1) S → S or A
(2) S → A
(3) A → A and B
(4) A → B
(5) B → not B
(6) B → ( S )
(7) B → true
(8) B → false

"""



ACTION = {
    (0, 'not'):   ('shift', 4),
    (0, '('):     ('shift', 5),
    (0, 'true'):  ('shift', 6),
    (0, 'false'): ('shift', 7),

    (1, 'or'):    ('shift', 8),
    (1, '$'):     ('accept',),

    (2, 'or'):    ('reduce', 'S', ['A']),
    (2, ')'):     ('reduce', 'S', ['A']),
    (2, 'and'):   ('shift', 9),
    (2, '$'):     ('reduce', 'S', ['A']),

    (3, 'or'):    ('reduce', 'A', ['B']),
    (3, 'and'):   ('reduce', 'A', ['B']),
    (3, ')'):     ('reduce', 'A', ['B']),
    (3, '$'):     ('reduce', 'A', ['B']),

    (4, 'not'):   ('shift', 4),
    (4, '('):     ('shift', 5),
    (4, 'true'):  ('shift', 6),
    (4, 'false'): ('shift', 7),

    (5, 'not'):   ('shift', 4),
    (5, '('):     ('shift', 5),
    (5, 'true'):  ('shift', 6),
    (5, 'false'): ('shift', 7),

    (6, 'and'):   ('reduce', 'B', ['true']),
    (6, 'or'):    ('reduce', 'B', ['true']),
    (6, ')'):     ('reduce', 'B', ['true']),
    (6, '$'):     ('reduce', 'B', ['true']),

    (7, 'and'):   ('reduce', 'B', ['false']),
    (7, 'or'):    ('reduce', 'B', ['false']),
    (7, ')'):     ('reduce', 'B', ['false']),
    (7, '$'):     ('reduce', 'B', ['false']),

    (8, 'not'):   ('shift', 4),
    (8, '('):     ('shift', 5),
    (8, 'true'):  ('shift', 6),
    (8, 'false'): ('shift', 7),

    (9, 'not'):   ('shift', 4),
    (9, '('):     ('shift', 5),
    (9, 'true'):  ('shift', 6),
    (9, 'false'): ('shift', 7),

    (10, 'and'):  ('reduce', 'B', ['not', 'B']),
    (10, 'or'):   ('reduce', 'B', ['not', 'B']),
    (10, ')'):    ('reduce', 'B', ['not', 'B']),
    (10, '$'):    ('reduce', 'B', ['not', 'B']),

    (11, 'or'):   ('shift', 8),
    (11, ')'):    ('shift', 14),

    (12, 'or'):   ('reduce', 'S', ['S', 'or', 'A']),
    (12, ')'):   ('reduce', 'S', ['S', 'or', 'A']),
    (12, '$'):    ('reduce', 'S', ['S', 'or', 'A']),
    (12, 'and'):    ('shift', 9),

    (13, 'and'):  ('reduce', 'A', ['A', 'and', 'B']),
    (13, 'or'):   ('reduce', 'A', ['A', 'and', 'B']),
    (13, ')'):    ('reduce', 'A', ['A', 'and', 'B']),
    (13, '$'):    ('reduce', 'A', ['A', 'and', 'B']),

    (14, 'and'):  ('reduce', 'B', ['(', 'S', ')']),
    (14, 'or'):   ('reduce', 'B', ['(', 'S', ')']),
    (14, ')'):    ('reduce', 'B', ['(', 'S', ')']),
    (14, '$'):    ('reduce', 'B', ['(', 'S', ')']),
}

GOTO = {
    (0, 'S'): 1,
    (0, 'A'): 2,
    (0, 'B'): 3,

    (4, 'B'): 10,

    (5, 'S'): 11,
    (5, 'A'): 2,
    (5, 'B'): 3,

    (8, 'A'): 12,
    (8, 'B'): 3,

    (9, 'B'): 13,
}


entrada = {0: 'not', 1: '(', 2: 'true', 3: 'or', 4:'false', 5:')', 6:'and', 7:'true', 8:'$'}
lr_parsing.LR_parsing(entrada,ACTION,GOTO,0)