// Jenkinsfile
// This defines the full CI/CD pipeline in code (Pipeline-as-Code)

pipeline {
    agent any  // Run on any available Jenkins agent

    environment {
        DOCKERHUB_USER = 'YOUR_DOCKERHUB_USERNAME'   // ← change this
        IMAGE_NAME     = 'cicd-portfolio'
        IMAGE_TAG      = "${BUILD_NUMBER}"            // Auto-increments each build
    }

    stages {

        // ── 1. CHECKOUT ────────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '📥 Pulling latest code from GitHub...'
                checkout scm
            }
        }

        // ── 2. TEST ────────────────────────────────────────────────────────
        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    pip install flask --quiet
                    python -m py_compile app/app.py
                    echo "Syntax check passed!"
                '''
            }
        }

        // ── 3. BUILD DOCKER IMAGE ──────────────────────────────────────────
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        // ── 4. PUSH TO DOCKER HUB ─────────────────────────────────────────
        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing image to Docker Hub...'
                // 'dockerhub-credentials' is set up in Jenkins → Credentials
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

        // ── 5. DEPLOY TO KUBERNETES ────────────────────────────────────────
        stage('Deploy to Kubernetes') {
            steps {
                echo '☸️  Deploying to Kubernetes...'
                sh """
                    # Update image tag in deployment
                    sed -i 's|${DOCKERHUB_USER}/${IMAGE_NAME}:latest|${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|g' k8s/deployment.yaml

                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    # Wait for rollout to finish
                    kubectl rollout status deployment/cicd-app --timeout=60s
                """
            }
        }
    }

    // ── POST-BUILD ACTIONS ─────────────────────────────────────────────────
    post {
        success {
            echo '✅ Pipeline succeeded! App is live.'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs above.'
        }
        always {
            // Clean up local Docker images to save disk space
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} || true"
        }
    }
}
