from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from datetime import datetime
import io
import io
import base64
from matplotlib.figure import Figure



app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages and session


@app.before_request
def before_request():
    """Initialize session and global g object for the request."""
    g.workouts = session.get('workouts', {"Warm-up": [], "Workout": [], "Cool-down": []})

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        category = request.form.get("category")
        exercise = request.form.get("workout", "").strip()
        duration_str = request.form.get("duration", "").strip()

        if not exercise or not duration_str or not category:
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
        g.workouts[category].append(entry) # Append to the global workouts

        session['workouts'] = g.workouts  # Save the updated workouts back to session


        flash(f"Success: '{exercise}' added to {category}!", "success")
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
                           workouts=g.workouts, # Pass g.workouts to the template
                           total_time=total_time,

                           motivational_note=motivational_note)


@app.route("/workout-chart")
def workout_chart():
    """Displays a personalized workout chart."""
    chart_data = {
        "Warm-up (5-10 min)": ["5 min light cardio (Jog/Cycle)", "Jumping Jacks (30 reps)", "Arm Circles (15 Fwd/Bwd)"],
        "Strength Workout (45-60 min)": ["Push-ups (3 sets of 10-15)", "Squats (3 sets of 15-20)", "Plank (3 sets of 60 seconds)", "Lunges (3 sets of 10/leg)"],
        "Cool-down (5 min)": ["Slow Walking", "Static Stretching (Hold 30s each)", "Deep Breathing Exercises"]
    }
    return render_template("workout_chart.html", chart_data=chart_data)



@app.route("/diet-chart")
def diet_chart():
    """Displays a diet chart for different fitness goals."""
    diet_plans = {
        "🎯 Weight Loss": ["Breakfast: Oatmeal with Berries", "Lunch: Grilled Chicken/Tofu Salad", "Dinner: Vegetable Soup with Lentils"],
        "💪 Muscle Gain": ["Breakfast: 3 Egg Omelet, Spinach, Whole-wheat Toast", "Lunch: Chicken Breast, Quinoa, and Steamed Veggies", "Post-Workout: Protein Shake, Greek Yogurt"],
        "🏃 Endurance Focus": ["Pre-Workout: Banana & Peanut Butter", "Lunch: Whole Grain Pasta with Light Sauce", "Dinner: Salmon & Avocado Salad"]
    }
    return render_template("diet_chart.html", diet_plans=diet_plans)



@app.route("/progress-tracker")
def progress_tracker():
    """Displays a summary of workout progress, similar to the Tkinter app's progress tab."""
    # g.workouts is already populated by before_request
    totals = {cat: sum(entry['duration'] for entry in sessions) for cat, sessions in g.workouts.items()}

    # Determine motivational note based on total time
    total_overall_time = sum(totals.values())

    

    chart_image = None
    if total_overall_time > 0:
        # --- Generate Chart ---
        fig = Figure(figsize=(7.5, 4), dpi=100)
        colors = ["#007bff", "#28a745", "#ffc107"]

        # Bar Chart
        ax1 = fig.add_subplot(121)


        ax1.bar(totals.keys(), totals.values(), color=colors)
        ax1.set_title("Time per Category (Min)", fontsize=10)
        ax1.set_ylabel("Total Minutes", fontsize=8)
        ax1.tick_params(axis='x', labelsize=8)
        ax1.tick_params(axis='y', labelsize=8)

        # Pie Chart
        ax2 = fig.add_subplot(122)


        pie_labels = [k for k, v in totals.items() if v > 0]
        pie_values = [v for v in totals.values() if v > 0]
        pie_colors = [colors[i] for i, v in enumerate(totals.values()) if v > 0]
        ax2.pie(pie_values, labels=pie_labels, autopct="%1.1f%%", startangle=90, colors=pie_colors, textprops={'fontsize': 8})
        ax2.set_title("Workout Distribution", fontsize=10)
        ax2.axis('equal')

        fig.tight_layout(pad=2.0)

        # Save chart to a bytes buffer and encode to base64
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        chart_image = base64.b64encode(buf.getbuffer()).decode("ascii")



    # Motivational Note Logic
    if total_overall_time == 0:
        motivational_note = "Log a session to see your progress!"
    elif total_overall_time < 30:
        motivational_note = "Good start! Keep moving 💪"
    elif total_overall_time < 60:
        motivational_note = "Nice effort! You're building consistency 🔥"
    else:
        motivational_note = "Excellent dedication! Keep up the great work 🏆"


    return render_template("progress_tracker.html",
                           totals=totals,
                           motivational_note=motivational_note,
                           total_overall_time=total_overall_time,
                           chart_image=chart_image)


if __name__ == "__main__":
    # Host must be '0.0.0.0' to be accessible from outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)
