# Flask App Boilerplate

## Features

- Python Flask webserver
- Dockerized for container deployment
- Minikube + Kubernetes manifests for local clusters
- Pytest for unit testing
- Jenkins pipeline for CI/CD
- SonarQube integration for code quality (locally)

## Quickstart

1. **Build and run locally:**
   ```
   pip install -r requirements.txt
   python -m app.app
   ```

2. **Run tests:**
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
