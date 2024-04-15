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
                            // Remove if something exists on remote host
                            sh "ssh -i /tmp/remote-key btomka@172.18.0.2 'rm -rf /home/btomka/*'"
                            // Copy the code to the remote host using SSH
                            sh 'scp -i /tmp/remote-key -r ./ btomka@172.18.0.2:/home/btomka'
                            // Run the command on the remote server using the private key file
                            echo repo.name
                            if (repo.name == 'linux') {
                                sh "ssh -i /tmp/remote-key btomka@172.18.0.2 'cd /home/btomka/linux && ls -larth'"
                            } else if (repo.name == 'jenkins') {
                                sh "ssh -i /tmp/remote-key btomka@172.18.0.2 'cd /home/btomka/jenkins && ls -larth'"
                            }
                            
                        } else {
                            echo "Remote repository ${repo.name} has no changes. Skipping the build."
                        }
                    }
                }
            }
        }
    }
}
