pipeline {
    agent any

    environment {
        // The image name and tag
        IMAGE_NAME = 'fitness-app:latest'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Set up Minikube Docker environment for Windows
                    bat 'minikube -p minikube docker-env --shell=cmd > minikubeEnv.cmd'
                    bat 'call minikubeEnv.cmd'
                    bat "docker build -t %IMAGE_NAME% ."
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl rollout status deployment/fitness-app-deployment'
            }
        }
    }
}