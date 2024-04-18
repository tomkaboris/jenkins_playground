pipeline {
    agent any

    stages {
        stage('Check Remote Changes') {
            steps {
                script {
                    
                    changes = ''
                    
                    def repositories = [
                        [name: 'terraform', url: 'https://github.com/tomkaboris/terraform_playground.git'],
                        [name: 'ansible', url: 'https://github.com/tomkaboris/ansible_playground.git']
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
                            echo "Remote repository ${repo.name} has changes. Proceeding with the build VM."
                            // Remove if something exists on remote host
                            sh "ssh -i /home/remote-key btomka@172.30.67.102 'rm -rf /home/btomka/jenkins/*'"
                            // Copy code to the remote host using SSH
                            sh 'scp -i /home/remote-key -r ./terraform ./ansible btomka@172.30.67.102:/home/btomka/jenkins'
                            // Add value to the changes
                            if (repo.name == 'linux') {
                                changes = 'linux'
                            } else if (repo.name == 'terraform') {
                                changes = 'terraform'
                            }
                        } else {
                            echo "Remote repository ${repo.name} has no changes."
                        }
                    }
                }
            }
        }
        stage('Build VM') {
            steps {
                script {
                    if (changes != '') {
                        sh "ssh -i /home/remote-key btomka@172.30.67.102 'cd /home/btomka/jenkins/terraform/KVM/Ubuntu && terraform init && terraform apply -auto-approve'"
                    }
                }
            }
        }
    }
}
