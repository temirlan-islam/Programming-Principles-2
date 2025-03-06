import os
path= r"C:\Users\Admin\Git\Programming-Principles-2\docs"
def checker(path):
    if os.path.exists(path):
        print("Name of file: ", os.path.basename(path))
        print("name of directory: ", os.path.dirname(path))
        return "success"
    
print(checker(path))
