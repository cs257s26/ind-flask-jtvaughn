from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, redirect, url_for, request
from flask import jsonify
from urllib.parse import unquote

from ProductionCode.top_species_command_line import forward_geocode, filter_by_radius, top_species_by_taxon
from ProductionCode.top_species_command_line import load_data as load_species_data
from ProductionCode.leaderboard_command_line import load_data as load_leaderboard_data
from ProductionCode.leaderboard_command_line import create_leaderboard, check_for_improper_request, print_leaders

app = Flask(__name__)

@app.route('/top_species/<location>/<radius>/<top_n>')
def top_species(location, radius=10, top_n=3):
    """Finds most observed species near a location in Minnesota.
    
    Args:
        location: City name to search near, e.g. 'Northfield, Minnesota'
        radius: Search radius in miles (default: 10)
        top_n: Number of top species per taxon (default: 3)
        
    Returns:
        JSON dict mapping iconic_taxon string to list of (taxon_name, common_name, count) tuples sorted by count descending, or an error message if the location is invalid or no observations are found."""
    data=load_species_data()

    location = request.args.get('location', default=location, type=str)
    if "minnesota" not in location.lower():
        location = f"{location}, Minnesota"
    radius = request.args.get('radius', default=10, type=int)
    top_n = request.args.get('top_n', default=3, type=int)  

    coords= forward_geocode(location)
    if coords is None:
        return jsonify({"error": f"Could not geocode '{location}'"})
    lat, lon = coords

    observations = filter_by_radius(data, lat, lon, radius)
    if len(observations) == 0:
        return jsonify({"error": f"No observations found near '{location}'. Make sure your location is in Minnesota."})
    result = top_species_by_taxon(observations, top_n)

    return jsonify(result)

@app.route('/leaderboard/<animal>')
def leaderboard(animal):
    """Displays the top 100 species-specific contributors to INaturalist in Minnesota for a given animal.
    
    Args:
        animal: Common name of the animal to search for, e.g. 'Common Loon'
    
    Returns:
        JSON list of top contributors with their contribution counts, or an error message if the animal is not found."""
    data = load_leaderboard_data()
    animal = request.args.get('animal', default=animal, type=str)
    check_result = check_for_improper_request(animal, data)
    
    if not check_result:
        return jsonify({"error": "Sorry, this is not an animal. Please try again."})
    
    leaderboard = create_leaderboard(animal,data)
    result= print_leaders(*leaderboard)  

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)