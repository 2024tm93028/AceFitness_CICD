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
                sh 'python -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'source venv/bin/activate && pytest'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                sh "sonar-scanner -Dsonar.projectKey=flask-app -Dsonar.sources=. -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_LOGIN}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-app:latest .'
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh 'kubectl apply -f kubernetes/'
            }
        }
    }
}