pipeline {
    agent any

    environment {
        // The image name and tag
        IMAGE_NAME = 'fitness-app:latest'
    }

    stages {

        stage('SonarQube Scan') {
            steps {
                script {
                    // This assumes you have the "SonarQube Scanner for Jenkins" plugin installed,
                    // a SonarQube server configured in Jenkins, and a sonar-project.properties file in your project root.
                    // Replace 'your-sonarqube-server-name' with the name of your SonarQube server configuration in Jenkins.
                    withSonarQubeEnv('your-sonarqube-server-name') {
                        bat 'sonar-scanner'
                    }
                }
            }
        }
        
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