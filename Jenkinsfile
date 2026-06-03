pipeline {
    agent any
    environment {
        IMAGE_NAME = "idogardana/myapp"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }
    stages {
        // שלב ה-Checkout האוטומטי קורה כאן לבד, אין צורך לכתוב אותו ידנית
        
        stage('Test') {
            steps {
                sh 'docker run --rm -v $(pwd)/app:/app -v $(pwd)/run_tests.sh:/run_tests.sh -w /app python:3.11-slim sh /run_tests.sh'
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
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                    sh "docker push ${IMAGE_NAME}:latest"
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
                    sh """
                        # הגדרת משתמש גיט
                        git config user.email "ci@jenkins"
                        git config user.name "Jenkins"
                        
                        # מעבר לבראנץ' ומשיכת השינויים הכי עדכניים מהשרת
                        git checkout main
                        git pull origin main
                        
                        # עדכון תגית הדוקר במניפסט
                        sed -i "s|image: idogardana/myapp:.*|image: idogardana/myapp:${IMAGE_TAG}|g" k8s/deployment.yaml
                        
                        # בדיקה: האם הקובץ באמת השתנה? רק אם כן - נבצע קומיט ופוש
                        if ! git diff --quiet k8s/deployment.yaml; then
                            git add k8s/deployment.yaml
                            git commit -m "ci: update image tag to ${IMAGE_TAG}"
                            git push https://\${GIT_USER}:\${GIT_TOKEN}@github.com/idogardana/devops-project.git main
                        else
                            echo "No changes detected in deployment.yaml. Skipping push."
                        fi
                    """
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