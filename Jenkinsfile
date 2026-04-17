pipeline {
    agent any

    environment {
        VENV = 'venv'
        RESULTS_DIR = 'results'
        APP_HOST = '127.0.0.1'
        APP_PORT = '8000'
        PATH = 'C:\\Users\\Akisou\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\Akisou\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\
        LocalCache\\local-packages\\Python313;%PATH%'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo PATH=%%PATH%%
                    python --version
                    if not exist %VENV% python -m venv %VENV%
                    call %VENV%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Install Newman') {
            steps {
                bat '''
                    npm --version
                    npm install -g newman
                    newman --version
                '''
            }
        }

        stage('Start FastAPI App') {
            steps {
                bat '''
                    if not exist %RESULTS_DIR% mkdir %RESULTS_DIR%
                    call %VENV%\\Scripts\\activate
                    start /B cmd /c "uvicorn app.user_api:app --host %APP_HOST% --port %APP_PORT% > %RESULTS_DIR%\\app.log 2>&1"
                    timeout /t 8 /nobreak
                    curl http://%APP_HOST%:%APP_PORT%/health
                '''
            }
        }

        stage('Run Newman API Tests') {
            steps {
                bat '''
                    if not exist %RESULTS_DIR%\\newman mkdir %RESULTS_DIR%\\newman
                    newman run tests\\postman\\UserAPI.postman_collection.json ^
                      -e tests\\postman\\local_env.json ^
                      -r cli,junit,json ^
                      --reporter-junit-export %RESULTS_DIR%\\newman\\newman-report.xml ^
                      --reporter-json-export %RESULTS_DIR%\\newman\\newman-report.json
                '''
            }
        }

        stage('Run Robot Tests') {
            steps {
                bat '''
                    if not exist %RESULTS_DIR%\\robot mkdir %RESULTS_DIR%\\robot
                    call %VENV%\\Scripts\\activate
                    robot --outputdir %RESULTS_DIR%\\robot tests\\robot\\suites
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'results/newman/*.xml'
            robot(
                outputPath: 'results/robot',
                outputFileName: 'output.xml',
                reportFileName: 'report.html',
                logFileName: 'log.html',
                disableArchiveOutput: false
            )
            archiveArtifacts artifacts: 'results/**/*', fingerprint: true, allowEmptyArchive: true
        }
    }
}