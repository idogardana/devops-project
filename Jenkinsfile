pipeline {
    agent any
    environment {
        IMAGE_NAME = "idogardana/myapp"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                sh '''
                    pip install pytest flask --break-system-packages
                    pytest app/test_app.py -v
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }
        stage('Update K8s Manifest') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-credentials',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                        git config user.email "ci@jenkins"
                        git config user.name "Jenkins"
                        sed -i "s|image: idogardana/myapp:.*|image: idogardana/myapp:${IMAGE_TAG}|g" k8s/deployment.yaml
                        git add k8s/deployment.yaml
                        git commit -m "ci: update image tag to ${IMAGE_TAG}"
                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/idogardana/devops-project.git main
                    '''
                }
            }
        }
    }
    post {
        failure {
            echo "Pipeline failed at build ${BUILD_NUMBER}"
        }
        success {
            echo "Successfully deployed version ${BUILD_NUMBER}"
        }
    }
}
