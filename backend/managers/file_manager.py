from pathlib import Path
from config.config import SEARCH_DIRS

class FileManager:

    search_dirs = SEARCH_DIRS

    def search(self, query):

        query = query.lower()

        matches = []

        for directory in self.search_dirs:

            if not directory.exists():
                continue

            try:

                for file in directory.rglob("*"):

                    try:

                        if query in file.name.lower():
                            matches.append(str(file))
                            print(f"Found match: {file}")

                    except Exception:
                        print(f"Error processing file: {file}")
                        continue

            except Exception:
                print(f"Error accessing directory: {directory}")
                continue

        return matches
    
if __name__ == "__main__":
    fm = FileManager()
    # print(fm.search_dirs)
    results = fm.search("ABZU")
    print(results)