from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# In-memory storage for workouts, similar to the original desktop app
workouts = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        workout_name = request.form.get("workout")
        duration_str = request.form.get("duration")

        if not workout_name or not duration_str:
            flash("Error: Please enter both workout and duration.", "error")
            return redirect(url_for('index'))

        try:
            duration = int(duration_str)
            if duration <= 0:
                flash("Error: Duration must be a positive number.", "error")
                return redirect(url_for('index'))
                
            workouts.append({"workout": workout_name, "duration": duration})
            flash(f"Success: '{workout_name}' added successfully!", "success")
        except ValueError:
            flash("Error: Duration must be a valid number.", "error")
        
        return redirect(url_for('index'))

    # For a GET request, render the page with the list of workouts
    return render_template("index.html", workouts=workouts)

if __name__ == "__main__":
    # The host must be '0.0.0.0' to be accessible from outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)