# syntactic-analyzer-generator
A Python-based framework for generating SLR(1) parsers from context-free grammars. Built as part of a university project for the Formal Languages and Compilers course at UFSC, this tool includes implementations of FIRST and FOLLOW sets, canonical collection construction, and SLR parsing table generation.

This educational project is designed to help students understand the principles of compiler design and parsing techniques. It provides a practical implementation of SLR parsing, allowing users to analyze and parse input based on defined grammar rules.

The framework is structured to facilitate easy extension and modification, making it suitable for educational purposes and further research in the field of formal languages and compilers.
1. Parsing the grammar rules and token list.
2. Generating the FIRST and FOLLOW sets.
3. Constructing the canonical collection of items.
4. Creating the SLR parsing table.
5. Executing the parsing process based on the generated table and input tokens.
6. Outputting the results of the parsing process, including any errors encountered.