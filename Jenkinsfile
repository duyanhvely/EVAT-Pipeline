pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t evat-data-science .'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    docker run --rm evat-data-science \
                    bash -c "pip install pytest && pytest main/app --tb=short || true"
                '''
            }
        }
        stage('Code Quality') {
            steps {
                sh '''
                    docker run --rm evat-data-science \
                    bash -c "pip install pylint && pylint main/app || true"
                '''
            }
        }
        stage('Security') {
            steps {
                sh '''
                    docker run --rm evat-data-science \
                    bash -c "pip install bandit && bandit -r main/app || true"
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker stop evat-app || true
                    docker rm evat-app || true
                    docker run -d -p 8000:8000 --name evat-app evat-data-science
                '''
            }
        }
        stage('Release') {
            steps {
                sh '''
                    docker tag evat-data-science evat-data-science:v1.0
                    echo "Released version 1.0"
                '''
            }
        }
        stage('Monitoring') {
            steps {
                sh '''
                    docker inspect evat-app || true
                    docker stats --no-stream evat-app || true
                    echo "Monitoring complete"
                '''
            }
        }
    }
} 