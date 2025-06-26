import os
import shutil

OUTPUT_PATH_DIR = "outputs"
SEPARATOR = ":=="

def get_file_lines(file_path: str) -> list[str]:
    """Lê um arquivo e retorna uma lista de linhas não vazias, sem espaços extras."""   
    with open(file_path, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]  # remove linhas vazias e espaços
    return linhas

def file_exists(file_path: str) -> bool:
    """Verifica se um arquivo existe."""
    return os.path.isfile(file_path)

def get_tokens_from_file(file_path: str) -> list[tuple[str, ...]]:
    
    def clean_token(token: str) -> str:
        if token.startswith("<"):
            return token[1:-1]
        if token.endswith(">"):
            return token[0:-1]
        return token
    
    if not file_exists(file_path):
        raise FileNotFoundError(f"O arquivo {file_path} não existe.")

    tokens = []
    for line in get_file_lines(file_path):
        raw_tokens = line.split()
        clean_tokens = [clean_token(token) for token in raw_tokens]
        tokens.append(tuple(clean_tokens))

    return tokens

def get_grammar_from_file(file_path:str) -> list[str]:

    if not file_exists(file_path):
        raise FileNotFoundError(f"O arquivo {file_path} não existe.")
    
    grammar = []
    for line in get_file_lines(file_path):
        grammar.append(line)
    
    return grammar


def prepare_output_directory(path: str = OUTPUT_PATH_DIR) -> None:
    """
    Garante que o diretório de saída exista e esteja limpo:
    - Se não existir, cria.
    - Se existir, remove todos os arquivos e subdiretórios recursivamente.
    
    Args:
        path (str): Caminho do diretório a preparar.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        for filename in os.listdir(path):
            if filename == ".gitkeep":
                continue
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

def write_in_file(file_path: str, content: str) -> None:
    """
    Escreve o conteúdo em um arquivo especificado.
    
    Args:
        file_path (str): Caminho do arquivo onde o conteúdo será escrito.
        content (str): Conteúdo a ser escrito no arquivo.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content + '\n')

def get_non_terminals(grammar: set[str]) -> set[str]:

    non_terminals = set()
    for prod in grammar:
        cabeca,corpo = prod.split(SEPARATOR)
        non_terminals.add(cabeca)

    return non_terminals


def format_canonical_collection(estados, transicoes) -> str:
    output = []

    # Estados (coleção canônica)
    for i, estado in enumerate(estados):
        output.append(f"\nEstado I{i}:")
        for tok in estado:
            regra = ' '.join(
                str(token.value) for token in tok.regex if token.value is not None
            )
            output.append(f"  {tok.name}: {regra}")

    # Transições (GOTO)
    output.append("\nTransições (GOTO):")
    for (origem, simbolo), destino in transicoes.items():
        output.append(f"  GOTO(I{origem}, {simbolo}) = I{destino}")

    return "\n".join(output)
