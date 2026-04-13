from pathlib import Path
from src.compiler.lexer.Lexer import Lexer

class Compiler():
    def compile(output : str):
        generateFolders()        

    def generateFolders():
        """
        Generates folders that hold the output video files and the intermediary video files that create the final output.
        """
        folder_path = Path("output")
        folder_path.mkdir(parents=True, exist_ok=True)
        folder_path = Path("cache")
        folder_path.mkdir(parents=True, exist_ok=True)
    
def compile_code(content):
    print(content)
    lex = Lexer(content)
    token_stream = lex.build_tokens()
    for token in token_stream:
        print(token.toString())