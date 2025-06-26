## How to run
1. Create a python3 virtual environment
```bash
python3 -m venv venv
```

2. Activate the virtual environment
```bash
source venv/bin/activate
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Run the main script
```bash
python src/main.py <main_rules> <token_list>
````

> <main_rules> is the path to the grammar file, e.g. `input/main_rules_with_id.txt`
> <token_list> is the path to the token list file, e.g. `input/token_list_with_ids.txt`


## Output 

In the `output` folder, you will find the following files:
- analysis_result.txt: Contains the analysis result of the parsing process.
- canonical_collection.txt: Contains the canonical collection of items.
- firsts.txt: Contains the FIRST sets of the grammar.
- follows.txt: Contains the FOLLOW sets of the grammar.
- slr_table.txt: Contains the SLR parsing table.

## Input
### Rules format
The rules file should contain one regex per line. Following the rule:
```
<name> :== <regex>
```

E.g.
```
S:== <A>
A:== <A> and <B>
```

### Tokens format
Should contain one token per line, following the rule:
```
<token_name> <token_value>
```

## Processing flow
1. **Argument Parsing**

   * The program expects two command-line arguments: a rules file and a tokens file.
   * If not provided, it exits with usage instructions.
2. **File Reading**
    * Reads the rules and tokens from the specified files.
    * If files are not found, it exits with an error message.
3. **Grammar Analysis**
    * Parses the rules to create a grammar object.
    * Generates FIRST and FOLLOW sets for the grammar.
4. **SLR Parsing Table Generation**
    * Constructs the SLR parsing table based on the grammar.
5. **Parsing Process**
    * Reads the tokens and processes them using the SLR parsing table.
    * Outputs the parsing result to a file.
6. **Output Generation**
    * Writes the analysis result, canonical collection, FIRST sets, FOLLOW sets, and SLR table to respective output files.