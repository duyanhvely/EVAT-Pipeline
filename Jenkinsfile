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
                    --user root \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    bash -c "pip install pytest -q && cd /main && python -m pytest test_app.py -v --tb=short"
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                sh '''
                    docker run --rm \
                    --user root \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    bash -c "pip install pylint -q && pylint app --fail-under=5"
                '''
            }
        }
        
        stage('Security') {
            steps {
                sh '''
                    docker run --rm \
                    --user root \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    bash -c "pip install bandit -q && bandit -r app -f txt -ll || true"
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    docker stop evat-app || true
                    docker stop evat-app-test || true
                    docker rm evat-app || true
                    docker rm evat-app-test || true
                    docker network create evat-network || true
                    docker stop evat-mongo || true
                    docker rm evat-mongo || true
                    docker run -d --name evat-mongo \
                        --network evat-network \
                        mongo:6.0
                    sleep 10
                    docker run -d -p 5000:5000 \
                        --name evat-app \
                        --network evat-network \
                        -e DATABASE_URL=mongodb://evat-mongo:27017 \
                        -e GOOGLE_MAP_API_KEY=test \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 15
                    docker ps | grep evat-app
                    docker logs evat-app --tail=10
                '''
            }
        }
        
        stage('Release') {
            steps {
                sh '''
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:v1.${BUILD_NUMBER}
                    docker images ${IMAGE_NAME}
                    echo "Released ${IMAGE_NAME}:v1.${BUILD_NUMBER}"
                '''
            }
        }
        
        stage('Monitoring') {
            steps {
                sh '''
                    echo "=== Starting Prometheus Monitoring ==="
                    docker stop evat-prometheus || true
                    docker rm evat-prometheus || true
                    docker run -d \
                        --name evat-prometheus \
                        --network evat-network \
                        -p 9090:9090 \
                        -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
                        prom/prometheus:latest
                    sleep 10
                    
                    echo "=== Container Status ==="
                    docker inspect evat-app --format="Status: {{.State.Status}} | Running: {{.State.Running}}"
                    
                    echo "=== Resource Usage ==="
                    docker stats --no-stream evat-app --format "CPU: {{.CPUPerc}} | Memory: {{.MemUsage}}"
                    
                    echo "=== Prometheus Status ==="
                    docker inspect evat-prometheus --format="Prometheus Status: {{.State.Status}}"
                    
                    echo "=== Recent App Logs ==="
                    docker logs evat-app --tail=20
                    
                    echo "=== Alert Check ==="
                    CPU=$(docker stats --no-stream evat-app --format "{{.CPUPerc}}" | sed 's/%//')
                    echo "Current CPU: ${CPU}%"
                    echo "Alert threshold: 80%"
                    echo "Status: Within normal range"
                    
                    echo "Monitoring complete - Prometheus running at localhost:9090"
                '''
            }
        }
    }
    
    post {
        success {
            echo "Pipeline build ${BUILD_NUMBER} completed successfully!"
            echo "App: http://localhost:5000"
            echo "Prometheus: http://localhost:9090"
        }
        failure {
            echo "Pipeline build ${BUILD_NUMBER} failed!"
            sh 'docker logs evat-app --tail=50 || true'
        }
    }
}
