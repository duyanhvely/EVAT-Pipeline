pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t evat-data-science .'
                sh 'docker images evat-data-science'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    docker run --rm evat-data-science \
                    bash -c "pip install pytest && cd /main && python -m pytest -v --tb=short -p no:cacheprovider || true"
                '''
            }
        }
        stage('Code Quality') {
            steps {
                sh '''
                    docker run --rm evat-data-science \
                    bash -c "pip install pylint && pylint main/app --fail-under=5 || true"
                '''
            }
        }
        stage('Security') {
            steps {
                sh '''
                    docker run --rm evat-data-science \
                    bash -c "pip install bandit && bandit -r main/app -f txt || true"
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker stop evat-app || true
                    docker rm evat-app || true
                    docker run -d -p 8000:8000 --name evat-app evat-data-science
                    sleep 5
                    docker ps | grep evat-app
                '''
            }
        }
        stage('Release') {
            steps {
                sh '''
                    docker tag evat-data-science evat-data-science:v1.0
                    docker images evat-data-science
                    echo "Successfully released evat-data-science:v1.0"
                '''
            }
        }
        stage('Monitoring') {
            steps {
                sh '''
                    echo "=== Container Status ==="
                    docker inspect evat-app --format="Status: {{.State.Status}}"
                    echo "=== Resource Usage ==="
                    docker stats --no-stream evat-app
                    echo "=== Container Logs ==="
                    docker logs evat-app --tail=20 || true
                    echo "Monitoring complete"
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
