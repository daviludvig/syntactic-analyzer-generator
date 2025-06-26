import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from core.utils import get_grammar_from_file


if __name__ == "__main__":
    
    input_file = "inputs/main_rules.txt"
    
    print(get_grammar_from_file(input_file))