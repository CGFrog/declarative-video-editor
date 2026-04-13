from pathlib import Path
from src.compiler.lexer.Lexer import Lexer

class Compiler():
    def compile(output : str):
        print("Compiling...\n" + output)
        generateFolders()        

    def generateFolders():
        """
        Generates folders that hold the output video files and the intermediary video files that create the final output.
        """
        folder_path = Path("output")
        folder_path.mkdir(parents=True, exist_ok=True)
        folder_path = Path("cache")
        folder_path.mkdir(parents=True, exist_ok=True)
    
