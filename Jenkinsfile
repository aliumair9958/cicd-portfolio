pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'aliumair9958'
        IMAGE_NAME     = 'cicd-portfolio'
        IMAGE_TAG      = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    python3 -m py_compile app/app.py
                    echo "✅ Syntax check passed!"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying container...'
                sh '''
                    docker stop cicd-app || true
                    docker rm cicd-app || true
                    docker run -d \
                        --name cicd-app \
                        --restart always \
                        -p 5000:5000 \
                        -e APP_ENV=production \
                        -e APP_VERSION=${IMAGE_TAG} \
                        aliumair9958/cicd-portfolio:latest
                    echo "✅ App deployed at http://16.171.200.81:5000"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded! App is live at http://16.171.200.81:5000'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs above.'
        }
        always {
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} || true"
        }
    }
}
