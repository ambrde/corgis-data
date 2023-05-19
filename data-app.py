from flask import Flask, url_for, render_template, request, Markup

import json

app = Flask(__name__)

@app.route("/")
def render_about():
    return render_template("datahome.html")
    
@app.route("/databystate")
def render_databystate():
    with open("wind_turbines.json") as turbine_data:
        data = json.load(turbine_data)
    with open("state_abbrs.json") as state_abbrs:
        stnames = json.load(state_abbrs)
    if "state" in request.args:
        state = request.args["state"]
        totals = get_state_totals(data, state)
        fullname = get_state_names(stnames, state)
        return render_template('databystate-response.html', options=get_state_options(data), fullname=get_state_names(stnames, state), 
               state=state, turbs=totals[0], cap=totals[1], homes=totals[2])
    return render_template("databystate.html", options=get_state_options(data))
    
@app.route("/databyyear")
def render_databyyear():
    with open("wind_turbines.json") as turbine_data:
        data = json.load(turbine_data)
    if "year" in request.args:
        year = request.args["year"]
        ytotal = get_year_total(data, year)
        return render_template('databyyear-response.html', yoptions=get_year_options(data), year=year, totalnum=ytotal[0])
    return render_template("databyyear.html", yoptions=get_year_options(data))
    
def get_state_names(stnames, state):
    for e in stnames:
        abbr = e["abbreviation"]
        if abbr == request.args["state"]:
            fullname = e["name"]
    return fullname
     
def get_state_options(data):
    """Returns the html code for a drop down menu.  Each option is a state for which there is data"""
    states = []
    options = ""
    for s in data:
        state = s["Site"]["State"]
        if (state not in states):
            states.append(state)
    states.sort()
    for e in states:
        options += Markup("<option value=\"" + e + "\">" + e + "</option>")
    return options
    
def get_year_options(data):
    """Returns the html code for a drop down menu.  Each option is a year for which there is data"""
    years = []
    yoptions = ""
    for s in data:
        year = s["Year"]
        if (year not in years):
            years.append(year)
    years.sort()
    for o in years:
        yoptions += Markup("<option value=\"" + str(o) + "\">" + str(o) + "</option>")
    return yoptions
    
def get_state_totals(data, state):
    turbs = 0
    cap = 0
    for s in data:
        if s["Site"]["State"] == state:
            turbs = turbs + 1
            cap = cap + s["Turbine"]["Capacity"]
    cap = cap/1000 #divide by 1000 to convert kW to MW
    return [format(turbs, ','), format(cap, ',g'), format(round(cap*136), ',')] #multiply by 187 to get approx. number of homes powered
    
def get_year_total(data, year):
    totalnum = 0
    for s in data:
        if str(s["Year"]) == year:
            totalnum = totalnum + 1
    return [format(totalnum, ',')]

if __name__=="__main__":
    app.run(debug=False)