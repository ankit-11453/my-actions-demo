pipeline {
    agent any
    stages {
        stage('Diagnose PATH') {
            steps {
                bat '''
                    echo ========================================
                    echo Current User:
                    whoami
                    echo ========================================
                    echo PATH expansion test:
                    echo %%PATH%%
                    echo ========================================
                    echo System32 test:
                    C:\\Windows\\System32\\where.exe cmd
                    echo ========================================
                    echo Python test:
                    python --version
                    pip --version
                    echo ========================================
                '''
            }
        }
    }
}