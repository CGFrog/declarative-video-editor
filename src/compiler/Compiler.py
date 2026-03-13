from pathlib import Path

def Compiler():
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
    
