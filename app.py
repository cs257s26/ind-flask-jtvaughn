import datasource
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '123456789'

ds = datasource.DataSource()

@app.route('/')
def index():
    return render_template('404.html')

@app.route('/top_species')
def top_species():
    """Finds most observed species near a location in Minnesota."""
    location = request.args.get('location', 'Northfield, Minnesota')
    radius   = float(request.args.get('radius', 10))
    top_n    = int(request.args.get('top_n', 3))

    city_name, results = ds.getTopSpeciesByCity(location, radius, top_n)
    if results is None:
        return render_template('404.html', error=f"Could not geocode '{location}'."), 404
    if len(results) == 0:
        return render_template('404.html', error=f"No observations found near '{location}'."), 404
    return render_template('top_species.html', location=city_name, radius=radius, top_n=top_n, results=results)

@app.route('/leaderboard')
def leaderboard():
    """Displays the top 100 contributors for a given animal."""
    animal  = request.args.get('animal', 'American Toad')
    results = ds.getLeaderboard(animal)
    if len(results) == 0:
        return render_template('404.html', error=f"No observations found for '{animal}'."), 404
    return render_template('leaderboard.html', animal=animal, leaderboard=results)

if __name__ == '__main__':
    app.run(debug=True)