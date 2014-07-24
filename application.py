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
    
    if util.template_render == None:
         util.generate_file_years("./text/background")
         util.template_render = calculate_timeline_placement(
                                    util.name_year, 10)
         return render_template('background.html', items=util.template_render)

    else:
        return render_template('background.html', items=util.template_render)
        #calculate_timeline_placement( 
        #                return_file_years("./text/background"), 10)
        
    #return render_template('background.html', items=name_year)

@app.route('/explore/')
def explore():
    if util.template_render == None:
     util.generate_file_years("./text/background")
     util.template_render = calculate_timeline_placement(
                                util.name_year, 10)
     return render_template('explore.html', items=util.template_render)

    else:
        return render_template('explore.html', items=util.template_render)


## Helper Functions ##
def calculate_timeline_placement(name_year, buf):
    """
    Calculate the individual placement of each of the timeline circles using
    the input name_year information. The buffer is the percent that needs to 
    be left open on either side for the timeline. Sorted by year. 
    (doc_name, distance_percent, info_tuple) 
    """     
    #unpack the values in name_year
    year_span, docs = name_year
    min_year = year_span[1]
    background_temp = []
    print year_span

    for doc, info in docs.items():
        if info["date"] != "none":
            distance = (int(info["date"])*1.0 - min_year)/year_span[0] * \
                (100 - buf*2) + buf
            background_temp.append( (doc, distance, info) )

    return sorted(background_temp, key=lambda x: x[1])


if __name__ == '__main__':
    app.run(debug=True)
