import os
import utility
from flask import Flask
from flask import render_template

app = Flask(__name__)
util = utility.UtilityFunc()

@app.route('/')
def index():
    return "<a href='/background/'>Index to Background</a>"

@app.route('/background/')
def background():
    build_background_timeline()
    return render_template('background.html', 
                            items=util.backg_render)

@app.route('/explore/')
def explore():
    build_background_timeline()
    build_explore_timeline()
    #if explore hasn't been generated yet
    return render_template('explore.html',
                        items=(util.expl_render, util.backg_render))

## Helper Functions ##
def build_background_timeline():
    """
    Generate the object to render for the background template. 
    """
    if util.backg_render == None:
        util.generate_file_years("./text/background", "backg")
        util.backg_render = calculate_timeline_placement(
                                util.backg_struct, 10)

def build_explore_timeline():
    if util.expl_render == None:
        util.generate_file_years("./text/explore", "expl")
        util.expl_render = calculate_timeline_placement(
                            util.expl_struct, 10, True)


def calculate_timeline_placement(name_year, buf, exp=False):
    """
    Calculate the individual placement of each of the timeline circles using
    the input name_year information. The buffer is the percent that needs to 
    be left open on either side for the timeline. Sorted by year. 
    (doc_name, distance_percent, info_tuple) 
    """     
    #take the year_span from the backg_struct
    #take the docs from the expl_struct
    if exp:
        year_span = util.backg_struct[0]
        docs = name_year[1]
    else:
        year_span, docs = name_year

    min_year = year_span[1]
    background_temp = []

    for doc, info in docs.items():
        if info["date"] != "none":
            distance = (int(info["date"])*1.0 - min_year)/year_span[0] * \
                (100 - buf*2) + buf
            background_temp.append( (doc, distance, info) )

    return sorted(background_temp, key=lambda x: x[1])


if __name__ == '__main__':
    app.run()
