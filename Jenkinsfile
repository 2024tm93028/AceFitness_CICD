pipeline {
    agent any

    tools {
        // Make sure 'python3' is configured in Jenkins Global Tool Configuration
        python 'python3'
    }

    environment {
        // Configure SonarQube server and scanner in Jenkins settings
        SONAR_SCANNER_HOME = tool 'SonarScanner'
        PATH = "${SONAR_SCANNER_HOME}/bin:${env.PATH}"
        // Assuming SonarQube is running on localhost
        SONAR_HOST_URL = "http://localhost:9000" 
        // Generate a token in SonarQube and add it to Jenkins credentials
        SONAR_LOGIN = credentials('sonarqube-token') 
    }

    stages {
        stage('Install Dependencies') {
            steps {
                bat'python -m venv venv'
                bat'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat'source venv/bin/activate && pytest'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                bat"sonar-scanner -Dsonar.projectKey=flask-app -Dsonar.sources=. -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_LOGIN}"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat'docker build -t flask-app:latest .'
            }
        }

        stage('Deploy to Minikube') {
            steps {
                bat'kubectl apply -f kubernetes/'
            }
        }
    }
}