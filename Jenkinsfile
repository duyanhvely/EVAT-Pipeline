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
                sh 'pip3 install pytest'
                sh 'pytest main/app --tb=short || true'
            }
        }
        stage('Code Quality') {
            steps {
                sh 'pip3 install pylint'
                sh 'pylint main/app || true'
            }
        }
        stage('Security') {
            steps {
                sh 'pip3 install bandit'
                sh 'bandit -r main/app || true'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 8000:8000 evat-data-science'
            }
        }
    }
}
