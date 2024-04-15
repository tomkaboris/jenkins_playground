pipeline {
    agent any

    stages {
        stage('Check Remote Changes') {
            steps {
                script {
                    def repositories = [
                        [name: 'jenkins', url: 'https://github.com/tomkaboris/jenkins_playground.git'],
                        [name: 'linux', url: 'https://github.com/tomkaboris/linux_playground.git']
                    ]

                    repositories.each { repo ->
                        // Clone the repository if it doesn't exist locally
                        if (!fileExists(repo.name)) {
                            sh "git clone ${repo.url} ${repo.name}"
                        }

                        // Fetch the latest changes from the remote repository
                        sh "cd ${repo.name} && git fetch"

                        // Get the number of commits behind/ahead of the remote branch
                        def commitsBehind = sh(script: "cd ${repo.name} && git rev-list --count HEAD..origin/main", returnStdout: true).trim().toInteger()
                        def commitsAhead = sh(script: "cd ${repo.name} && git rev-list --count origin/main..HEAD", returnStdout: true).trim().toInteger()

                        if (commitsBehind > 0 || commitsAhead > 0) {
                            echo "Remote repository ${repo.name} has changes. Proceeding with the build."
                            // Your build steps here
                        } else {
                            echo "Remote repository ${repo.name} has no changes. Skipping the build."
                        }
                    }
                }
            }
        }
    }
}
