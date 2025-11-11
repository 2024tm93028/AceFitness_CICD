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
                    // Use Minikube's Docker daemon
                    bat 'eval $(minikube -p minikube docker-env)'
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
