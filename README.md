## ACEestFitness and Gym

This is a simple Flask web application to track workouts.

### Running the application locally

1.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask app:**
    ```bash
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

### Testing

   ```
   pytest
   ```

3. **Build Docker image:**
   ```
   docker build -t flask-app:latest .
   ```

4. **Deploy on Minikube:**
   ```
   kubectl apply -f kubernetes/
   minikube service flask-app-service
   ```

5. **CI/CD:**
   - Configure Jenkins to pick up the `Jenkinsfile`.
   - Set up SonarQube on your local Windows machine and configure Jenkins accordingly.
