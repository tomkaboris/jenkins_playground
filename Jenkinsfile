pipeline {
    agent any

    parameters {
        string(name: 'API_URL', defaultValue: 'https://10.80.0.100/rest', description: 'API URL')
        string(name: 'API_USERNAME', defaultValue: 'admin', description: 'API Username')
        password(name: 'API_PASSWORD', defaultValue: 'admin', description: 'API Password')
        string(name: 'API_INTERVAL', defaultValue: '5', description: 'Interval in seconds')
        string(name: 'API_DURATION', defaultValue: '600', description: 'Duration in seconds')
        string(name: 'API_OUTPUT_FILE', defaultValue: 'api_data.json', description: 'Output JSON file name')
    }

    environment {
        API_URL = "${params.API_URL}"
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
        stage('Run Script') {
            steps {
                sh 'python pull_data.py'
            }
        }
    }
}
