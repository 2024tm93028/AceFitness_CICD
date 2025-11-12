from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages and session

@app.before_request
def before_request():
    """Initialize session and global g object for the request."""
    g.workouts = session.get('workouts', {"Warm-up": [], "Workout": [], "Cool-down": []})

@app.route("/", methods=["GET", "POST"])
def index():
    workouts = session.get('workouts')

    if request.method == "POST":
        category = request.form.get("category")
        exercise = request.form.get("workout", "").strip()
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
            "exercise": exercise,
            "duration": duration,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        g.workouts[category].append(entry)
        session['workouts'] = workouts  # Save back to session

        flash(f"Success: '{workout}' added to {category}!", "success")
        return redirect(url_for('index'))

    # For a GET request, calculate summary
    total_time = sum(e['duration'] for sessions in g.workouts.values() for e in sessions)

    if total_time < 30:
        motivational_note = "Good start! Keep moving 💪"
    elif total_time < 60:
        motivational_note = "Nice effort! You're building consistency 🔥"
    else:
        motivational_note = "Excellent dedication! Keep up the great work 🏆"

    return render_template("index.html",
                           workouts=g.workouts,
                           total_time=total_time,
                           motivational_note=motivational_note)

@app.route("/workout-chart")
def workout_chart():
    """Displays a personalized workout chart."""
    chart_data = {
        "Warm-up": ["5 min Jog", "Jumping Jacks", "Arm Circles", "Leg Swings", "Dynamic Stretching"],
        "Workout": ["Push-ups", "Squats", "Plank", "Lunges", "Burpees", "Crunches"],
        "Cool-down": ["Slow Walking", "Static Stretching", "Deep Breathing", "Yoga Poses"]
    }
    return render_template("workout_chart.html", chart_data=chart_data)

@app.route("/diet-chart")
def diet_chart():
    """Displays a diet chart for different fitness goals."""
    diet_plans = {
        "Weight Loss": ["Oatmeal with Fruits", "Grilled Chicken Salad", "Vegetable Soup", "Brown Rice & Stir-fry Veggies"],
        "Muscle Gain": ["Egg Omelet", "Chicken Breast", "Quinoa & Beans", "Protein Shake", "Greek Yogurt with Nuts"],
        "Endurance": ["Banana & Peanut Butter", "Whole Grain Pasta", "Sweet Potatoes", "Salmon & Avocado", "Trail Mix"]
    }
    return render_template("diet_chart.html", diet_plans=diet_plans)

if __name__ == "__main__":
    # Host must be '0.0.0.0' to be accessible from outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)
