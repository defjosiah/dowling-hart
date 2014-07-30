#helperfunctions
import os
import markdown
import codecs
from flask import render_template
from jinja2 import Template

class UtilityFunc:
    """
    This is a blanket class that will be used for smart generation and
    computation, e.g. only generating the name_year object when it has 
    changes, etc. It is mostly flags and "generate" methods that will
    call the methods contained in the utility class outside of this 
    UtilityFunc 
    """

    def __init__(self):
        #background render and info
        self.backg_render = None
        self.backg_struct = None

        #explore render and info
        self.expl_render = None
        self.expl_struct = None
        self.expl_answer = []

    def generate_file_years(self, path, page):
        if page == "backg":
            self.backg_struct = return_file_years(path)
        elif page == "expl":
            self.expl_struct = return_file_years(path)
        else:
            print "error, error, error"

    def generate_explore_answer(self, groups):
        """
        Return a list of groups number of tuples, where each tuple contains
        the average of the closest years, and the document names for that
        section for the specified timeline section. [(avg, (document1, doc2))]
        """
        a = (1893 - 1837)*1.0 / 162 * (100 - 16) + 8
        b = (1997 - 1837)*1.0 / 162 * (100 - 16) + 8
        self.expl_answer = [(a, ("expl_1_mem", "expl_2_cityhall")), (b, ("expl_3_civilrights", "expl_4_irish"))]


def return_file_years(path):
    """
    Loop through the files specified by the path and parse the top level
    comment, return a dictionary mapping file-name to file years.
    Summarize the result dictionary with a count of the distance between
    the two years.
    Also return a string containing the html of the given markdown file. 
    """
    name_year = {}
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        for entry in files:
            file_path = os.path.join(root, entry)
            name_year[entry] = parse_markdown_headers(file_path)
            name_year[entry]["md"] = return_html(
                                        file_path, name_year[entry]["mc"])

    return (summarize_years(name_year), name_year)

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

def summarize_years(name_year):
    """
    Return the number of years between the bottom and top entry in the
    input name to year dictionary. And the year of the bottom entry. 
    """
    temp = sorted([f for f in name_year.items() \
        if not f[1]["date"] == "none"], key=lambda x: int(x[1]["date"]))

    return (int(temp[-1][1]["date"]) - int(temp[0][1]["date"]),  \
            int(temp[0][1]["date"]))

def return_html(path, mc):
    """
    Given an input path, return an html string of the corresponding input
    markdown. Also use jinja macro to process figures in the text. If it is
    background text, return the html of the input markdown. If it is explore
    text, return a dictionary mapping "<key" to html rendered as markdown. 
    """
    f = codecs.open(path, mode="r", encoding="utf-8")

    if mc == "none":
        html = markdown.markdown(f.read(), output_format="html5",
                                    safe_mode=False)
     
        t = Template("""
          {% macro figure(caption, src) -%}
          <figure class="cap-top">
    	      <a href="{{ src }}">
                 <img src="{{ src }}" alt="{{ caption }}">
    		  </a>
          <figcaption>
              {{ caption }}
          </figcaption>
          </figure>
          {%- endmacro %}
    	  """ + html)
        return t.render()
    else:
        temp_dict = {}
        ind = False
        curr = ""
        #f.readline() #skip html comment at the beginning
        for line in f.readlines():
            if line[0] == "<" and line[1] != "!": #ignore html
                curr = line[1::].rstrip()
                temp_dict[curr] = ""
            elif curr != "":
                temp_dict[curr] += line
            else:
                continue

        #turn each entry into a markdown string for the entry, turn
        #it back into a dictionary at the end dict(tuple()) turns 
        # (key,value) into {key: value}
        a = dict(tuple(map(lambda x: (x[0], markdown.markdown(x[1], 
                                    output_format="html5",
                                    safe_mode=False,
                                    extensions=["footnotes(BACKLINK_TEXT=)"]) ), 
                                    temp_dict.items())))
        return a


