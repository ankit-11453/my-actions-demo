pipeline {
    agent any

        options {
        timestamps()
            }

    environment {
        // Prefer the Windows Python Launcher if installed
        PY_CMD = 'py -3.13'
        VENV_DIR = 'venv'
        VENV_PY = 'venv\\Scripts\\python.exe'
        VENV_PIP = 'venv\\Scripts\\pip.exe'
        ROBOT = 'venv\\Scripts\\robot.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                bat '''
                echo === DEBUG: Workspace ===
                cd
                echo WORKSPACE=%CD%
                dir
                '''
            }
        }

        stage('Precheck Python') {
            steps {
                bat '''
                @echo on
                echo === DEBUG: PATH ===
                echo %PATH%

                echo === DEBUG: Who am I ===
                whoami

                echo === DEBUG: Check py launcher ===
                py -0p
                if errorlevel 1 (
                    echo ERROR: Python launcher 'py' is not available.
                    exit /b 1
                )

                echo === DEBUG: Python version ===
                %PY_CMD% --version
                if errorlevel 1 (
                    echo ERROR: Requested Python version is not available.
                    exit /b 1
                )
                '''
            }
        }

        stage('Create Venv') {
            steps {
                bat '''
                @echo on
                echo === Create virtual environment ===
                if exist %VENV_DIR% (
                    echo Existing venv found
                ) else (
                    %PY_CMD% -m venv %VENV_DIR%
                    if errorlevel 1 (
                        echo ERROR: Failed to create virtual environment.
                        exit /b 1
                    )
                )

                if not exist %VENV_PY% (
                    echo ERROR: venv python not found at %VENV_PY%
                    dir %VENV_DIR%
                    exit /b 1
                )

                %VENV_PY% --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                @echo on
                echo === Upgrade pip ===
                %VENV_PY% -m pip install --upgrade pip setuptools wheel
                if errorlevel 1 exit /b 1

                echo === Install requirements ===
                %VENV_PIP% install -r requirements.txt
                if errorlevel 1 exit /b 1

                echo === Installed packages ===
                %VENV_PIP% list
                '''
            }
        }

        stage('Test Robot') {
            steps {
                bat '''
                @echo on
                echo === Run Robot Tests ===
                if not exist tests (
                    echo ERROR: tests folder not found
                    dir
                    exit /b 1
                )

                %ROBOT% -d results tests
                if errorlevel 1 exit /b 1
                '''
            }
        }
    }

    post {
        always {
            bat '''
            echo === DEBUG: Final workspace listing ===
            dir
            if exist results dir results
            '''
            archiveArtifacts artifacts: 'results/**', allowEmptyArchive: true
        }
        failure {
            echo 'Build failed. Check Python availability, PATH, and venv creation logs.'
        }
    }        
}