import platform, os

def join_list(list, insert=None):
    str = ""
    
    if insert == None:
        insert = ""
    
    for i in list:
        str = str +  (i + insert)
        
    return str

def flip_slashes(path):
    new_path = ""
    
    for chr in path:
        if chr == "\\":
            new_path += "/"
        else:
            new_path += chr
            
    return new_path

def refine_path(path):
    char_count = 0
    refined_path = ""
    
    for char in path:
        char_count += 1
        
        if char_count != len(path):
            refined_path = refined_path + char
        else:
            if char != "/":
                refined_path = refined_path + char
            
    return refined_path

def move_back(path):
    
    path = path.split("/")
    new_path = ""
    
    count = 0
    for directory in path:
        count += 1
        if count != len(path):
            new_path += (directory + "/")
            
    return refine_path(new_path)

def get_appdatafolder():
    currentOs = platform.system()
    
    if currentOs == "Windows":
        return os.getenv('APPDATA') + "\.privatus-launcher"
    if currentOs == "Linux":
        return os.path.expanduser('~') +  + "/.privatus-launcher"
    
def get_program_path():
    currentOs = platform.system()
    
    if currentOs == "Windows":
        program_path = r"C:/Program Files/privatus"
        
        if not os.path.exists(program_path):
            os.makedirs(program_path)
        
        return program_path
    if currentOs == "Linux":
        return os.path.expanduser('~')
    
def get_file_extension(file):
    """
    Gets the file extension of a given file(string)
    
    Note:
    Does not work with multiple dots in the given text
    """
    
    file = file.strip(".")
    
    if len(file) > 1:
        return file[1]
    else:
        raise "The given file(string) does not have an extension(dot must be used)"