import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from core.utils import get_tokens_from_file


if __name__ == "__main__":
    input_file = "inputs/tokens.txt"
    
    print(get_tokens_from_file(input_file))

