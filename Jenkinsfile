pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ${VENV} || true
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    npm install -g newman
                '''
            }
        }

        stage('Start FastAPI App') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    nohup uvicorn app.user_api:app --host 127.0.0.1 --port 8000 > app.log 2>&1 &
                    sleep 5
                '''
            }
        }

        stage('Run Newman API Tests') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    mkdir -p results
                    newman run tests/postman/UserAPI.postman_collection.json \
                      -e tests/postman/env.json \
                      --reporters cli,json \
                      --reporter-json-export results/newman-report.json
                '''
            }
        }

        stage('Run Robot Tests') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    robot -d results/robot tests/robot/suites
                '''
            }
        }
    }

    post {
        always {
            robot(
                outputPath: 'results/robot',
                outputFileName: 'output.xml',
                reportFileName: 'report.html',
                logFileName: 'log.html'
            )
            archiveArtifacts artifacts: 'results/**/*', fingerprint: true
        }
    }
}