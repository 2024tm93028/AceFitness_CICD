from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

workouts = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        workout = request.form['workout']
        duration = request.form['duration']
        if workout and duration:
            try:
                duration = int(duration)
                workouts.append({'workout': workout, 'duration': duration})
            except ValueError:
                return render_template('index.html', error='Duration must be a number', workouts=workouts)
            return redirect(url_for('view_workouts'))
        else:
            return render_template('index.html', error='Please enter both workout and duration.', workouts=workouts)
    return render_template('index.html', workouts=workouts)

@app.route('/workouts')
def view_workouts():
    return render_template('workouts.html', workouts=workouts)

if __name__ == '__main__':
    app.run(debug=True)
