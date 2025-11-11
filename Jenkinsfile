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
                    // Use Minikube's Docker daemon on Windows
                    bat '@FOR /f "tokens=*" %%i IN (\'minikube -p minikube docker-env --shell cmd\') DO @%%i'
                    bat "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                // Apply the Kubernetes configurations
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl rollout status deployment/fitness-app-deployment'
            }
        }
    }
}
