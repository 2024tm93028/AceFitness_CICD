pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t flask-app:latest .'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('LocalSonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh 'kubectl apply -f kubernetes\\deployment.yaml'
                sh 'kubectl apply -f kubernetes\\service.yaml'
            }
        }
    }
}