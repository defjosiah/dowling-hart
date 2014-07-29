import os
import utility
import codecs
import markdown
from flask import Flask
from flask import render_template

app = Flask(__name__)
util = utility.UtilityFunc()

@app.route('/')
#def index():
 #   return "<a href='/background/'>Index to Background</a>"

@app.route('/')
@app.route('/background/')
def background():
    build_background_timeline()
    intro = utility.return_html('./text/backg_intro.md', 'none')
    return render_template('background.html', 
                            items=util.backg_render, 
                            tot_points=len(util.backg_render),
                            intro=intro)

@app.route('/explore/')
def explore():
    build_background_timeline()
    build_explore_timeline()
    f = codecs.open("./text/directions/expl_directions.txt", mode="r", encoding="utf-8")
    g = codecs.open("./text/directions/expl_game_directions.txt", mode="r", encoding="utf-8")
    f = markdown.markdown(f.read(), output_format="html5",
                                    safe_mode=False)
    g = markdown.markdown(g.read(), output_format="html5",
                                    safe_mode=False)

    return render_template('explore.html',
                        items=(util.expl_render, util.backg_render),
                        solution=util.expl_answer, 
                        directions=(f,g),
                        tot_points=len(util.backg_render))

@app.route('/process/')
def process():
    return render_template('process.html')

#helper functions
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
        util.generate_explore_answer(2)


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
