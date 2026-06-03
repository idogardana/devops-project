pipeline {
    agent any
    environment {
        IMAGE_NAME = "idogardana/myapp"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') { ... }

        stage('Test') {
            // מריץ pytest
        }

        stage('Build Docker Image') {
            // docker build -t $IMAGE_NAME:$IMAGE_TAG
        }

        stage('Push to DockerHub') {
            // withCredentials — לעולם לא hardcode passwords!
            // docker push
        }

        stage('Update K8s Manifest') {
            // sed -i מחליף את ה-image tag ב-deployment.yaml
            // git commit & push — זה מה שמפעיל את ArgoCD
        }
    }
    post {
        failure { echo "Pipeline failed!" }
        success { echo "Deployed version ${BUILD_NUMBER}" }
    }
}
