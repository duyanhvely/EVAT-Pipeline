pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "evat-data-science"
        IMAGE_TAG = "build-${BUILD_NUMBER}"
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
                sh 'docker images ${IMAGE_NAME}'
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    bash -c "pip install pytest && cd /main && python -m pytest test_app.py -v --tb=short"
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                sh '''
                    docker run --rm \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    bash -c "pip install pylint && pylint app --fail-under=5"
                '''
            }
        }
        
        stage('Security') {
            steps {
                sh '''
                    docker run --rm \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    bash -c "pip install bandit && bandit -r app -f txt -ll"
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    docker stop evat-app || true
                    docker rm evat-app || true
                    docker run -d -p 5000:5000 --name evat-app ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 10
                    docker ps | grep evat-app
                    docker exec evat-app python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" || echo "App starting up"
                '''
            }
        }
        
        stage('Release') {
            steps {
                sh '''
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:v1.${BUILD_NUMBER}
                    docker images ${IMAGE_NAME}
                    git tag -a v1.${BUILD_NUMBER} -m "Release build ${BUILD_NUMBER}" || true
                    echo "Released ${IMAGE_NAME}:v1.${BUILD_NUMBER}"
                '''
            }
        }
        
        stage('Monitoring') {
            steps {
                sh '''
                    echo "=== Container Status ==="
                    docker inspect evat-app --format="Status: {{.State.Status}} | Running: {{.State.Running}}"
                    echo "=== Resource Usage ==="
                    docker stats --no-stream evat-app --format "CPU: {{.CPUPerc}} | Memory: {{.MemUsage}}"
                    echo "=== Recent Logs ==="
                    docker logs evat-app --tail=30
                    echo "=== Health Check ==="
                    docker inspect evat-app --format="Health: {{.State.Health}}" || echo "No healthcheck data yet"
                    echo "Monitoring complete"
                '''
            }
        }
    }
    
    post {
        success {
            echo "Pipeline build ${BUILD_NUMBER} completed successfully!"
            echo "Image: evat-data-science:build-${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline build ${BUILD_NUMBER} failed!"
            sh 'docker logs evat-app --tail=50 || true'
        }
    }
}
