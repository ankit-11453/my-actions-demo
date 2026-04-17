pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo "=== Direct Python Test ==="
                    "C:\\Users\\Akisou\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python313\\python.exe" --version
                    
                    echo "=== Create VENV ==="
                    if not exist venv (
                        "C:\\Users\\Akisou\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python313\\python.exe" -m venv venv
                    )
                    
                    echo "=== Activate VENV ==="
                    call venv\\Scripts\\activate.bat
                    
                    echo "=== Install requirements ==="
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\pip.exe install -r requirements.txt
                    
                    echo "=== Verify ==="
                    venv\\Scripts\\pip.exe list
                '''
            }
        }

        stage('Test Robot') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    robot --version
                '''
            }
        }
    }
}