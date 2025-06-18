import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core.define_first as define_first


"""
"v" for 'or' / "a" for 'and' / "n" for 'not
Problema identificado: quando o terminal tem 2 letras (ex: id), só pega a primeira letra
"""
grammar = {
    "E": ["TE'"],
    "E'": ["vTE'", "&"],
    "T": ["FT'"],
    "T'": ["aFT'", "&"],
    "F": ["nF", "id"]
}

firsts = define_first.define_first(grammar)
for nt, f in firsts.items():
    print(f"FIRST({nt}) = {f}")