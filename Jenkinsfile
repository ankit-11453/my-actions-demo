pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                bat '''
                    echo %PATH%
                    C:\\Windows\\System32\\where.exe cmd
                    C:\\Program Files\\Python312\\python.exe --version
                '''
            }
        }
    }
}