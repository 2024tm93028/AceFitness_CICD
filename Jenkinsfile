pipeline {
    agent any

    environment {
        // The image name and tag
        IMAGE_NAME = 'fitness-app:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                // Get the code from your Git repository
                git 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Use Minikube's Docker daemon
                    sh 'eval $(minikube -p minikube docker-env)'
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                // Apply the Kubernetes configurations
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl rollout status deployment/fitness-app-deployment'
            }
        }
    }
}