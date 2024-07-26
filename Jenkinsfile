pipeline {
    agent any

    parameters {
        string(name: 'API_IP', defaultValue: '10.80.0.100', description: 'API IP')
        string(name: 'API_USERNAME', defaultValue: 'admin', description: 'API Username')
        password(name: 'API_PASSWORD', defaultValue: 'admin', description: 'API Password')
        string(name: 'API_INTERVAL', defaultValue: '5', description: 'Interval in seconds')
        string(name: 'API_DURATION', defaultValue: '30', description: 'Duration in seconds')
        string(name: 'API_IDS', defaultValue: '["SYSTEM_NAME", "MEM_STATS"]', description: 'Data for metrics')
    }

    environment {
        API_IP = "${params.API_IP}"
        USERNAME = "${params.API_USERNAME}"
        PASSWORD = "${params.API_PASSWORD}"
        INTERVAL = "${params.API_INTERVAL}"
        DURATION = "${params.API_DURATION}"
        OUTPUT_FILE = "${params.API_OUTPUT_FILE}"
    }

    stages {
        stage('Python version') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('Run Script') {
            steps {
                sh 'python3 pull_data.py'
            }
        }
    }
}
