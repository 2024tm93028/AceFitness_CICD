from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages and session

@app.before_request
def initialize_session():
    """Initialize workouts in session if not already present."""
    if 'workouts' not in session:
        session['workouts'] = {"Warm-up": [], "Workout": [], "Cool-down": []}

@app.route("/", methods=["GET", "POST"])
def index():
    workouts = session.get('workouts')

    if request.method == "POST":
        category = request.form.get("category")
        workout = request.form.get("workout", "").strip()
        duration_str = request.form.get("duration", "").strip()

        if not workout or not duration_str or not category:
            flash("Error: Please fill all fields.", "error")
            return redirect(url_for('index'))

        try:
            duration = int(duration_str)
            if duration <= 0:
                flash("Error: Duration must be a positive number.", "error")
                return redirect(url_for('index'))
        except ValueError:
            flash("Error: Duration must be a valid number.", "error")
            return redirect(url_for('index'))

        entry = {
            "exercise": workout,
            "duration": duration,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        workouts[category].append(entry)
        session['workouts'] = workouts  # Save back to session

        flash(f"Success: '{workout}' added to {category}!", "success")
        return redirect(url_for('index'))

    # For a GET request, calculate summary
    total_time = sum(e['duration'] for sessions in workouts.values() for e in sessions)

    if total_time < 30:
        motivational_note = "Good start! Keep moving 💪"
    elif total_time < 60:
        motivational_note = "Nice effort! You're building consistency 🔥"
    else:
        motivational_note = "Excellent dedication! Keep up the great work 🏆"

    return render_template("index.html",
                           workouts=workouts,
                           total_time=total_time,
                           motivational_note=motivational_note)

if __name__ == "__main__":
    # Host must be '0.0.0.0' to be accessible from outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)
