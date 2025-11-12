pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'docker build -t flask-app:latest .'
            }
        }
        stage('Test') {
            steps {
                bat 'pytest --maxfail=1 --disable-warnings -q'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('LocalSonarQube') {
                    bat 'sonar-scanner'
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                bat 'kubectl apply -f kubernetes\\deployment.yaml'
                bat 'kubectl apply -f kubernetes\\service.yaml'
            }
        }
    }
}