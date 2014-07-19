#helperfunctions
import os
import re

def return_file_years(path):
    """
    Loop through the files specified by the path and parse the top level
    comment, return a dictionary mapping file-name to file years. 
    """

    for directory in os.walk(path):
        print directory
    return 5

def parse_markdown_headers(path):
    """
    Markdown headers are in the form of html comments, <!-- key:value, -->
    Return a dictionary mapping keys to values.  
    """
    return_dict = {}
    with open(path, 'r') as f:
        print f.readline()
    return 

return_file_years("text/background/")
parse_markdown_headers("text/background/backg_0_intro.txt")