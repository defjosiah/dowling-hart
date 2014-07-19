#helperfunctions
import os

def return_file_years(path):
    """
    Loop through the files specified by the path and parse the top level
    comment, return a dictionary mapping file-name to file years. 
    """
    name_year = {}
    for root, dirs, files in os.walk(path):
        print root, dirs, files
        files = [f for f in files if not f[0] == '.']
        for entry in files:
            name_year[entry] = parse_markdown_headers(root + "/" + entry)
    return name_year

def parse_markdown_headers(path):
    """
    Markdown headers are in the form of html comments, <!-- key:value, -->
    Return a dictionary mapping keys to values.  
    """
    return_dict = {}
    with open(path, 'r') as f:
        key_val = f.readline()[4:-4].rstrip().split(",")
        for key in key_val:
            temp = key.split(":")
            return_dict[temp[0].strip()] = temp[1]
    return return_dict