
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh './run.sh'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
