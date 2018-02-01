#!/usr/bin/env groovy
pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }
    tools {
        jdk 'JDK1.8.0_65'
        maven 'M3'
    }
    stages {
        stage('Checkout de Keycloak') {
            steps {
                script {
                    BRANCH_NAME = 'trunk'
                    tagDocker = 'SNAPSHOT'
                }
                echo 'Obtention de... ' + BRANCH_NAME
                checkout scm
            }
        }
        stage ('Tests unitaires') {
            parallel {
                stage ('Tests unitaires du module ansible de Keycloak') {
                    steps {
                        sh "if [ ! -d ansible ]; then git clone https://github.com/Inspq/ansible.git && cd ansible; else cd ansible && git pull; fi; git checkout inspq"
                        sh "source ansible/hacking/env-setup; cd ansible && ansible-test sanity --test validate-modules"
                        sh "touch ansible.cfg"
                        sh "printf '[defaults]\nroles_path=${WORKSPACE}/rolesansible/roles\nlibrary=${WORKSPACE}/ansible/lib/ansible/modules:library\nmodule_utils=${WORKSPACE}/ansible/lib/ansible/module_utils:module_utils\n' >> ansible.cfg"
                        sh "source ansible/hacking/env-setup; ansible-playbook createUnitEnv.yml -i UNIT/UNIT.hosts"
                        sh "source ansible/hacking/env-setup; nosetests --with-xunit ansible/test/units/module_utils/test_keycloak_utils.py ansible/test/units/modules/identity/keycloak/test_keycloak*.py"
                        sh "source ansible/hacking/env-setup; ansible-playbook cleanupUnitEnv.yml -i UNIT/UNIT.hosts"
                    }
                    post {
                        success {
                            junit '**/nosetests.xml'
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script {equipe = 'eric.parent@inspq.qc.ca'
            }
        }
        success {
            script {
                if (currentBuild.getPreviousBuild().getResult().toString() != "SUCCESS") {
                    mail(to: "${equipe}", 
                        subject: "Construction de ${BRANCH_NAME} réalisée avec succès: ${env.JOB_NAME} #${env.BUILD_NUMBER}", 
                        body: "${env.BUILD_URL}")
                }
            }
        }
        failure {
            mail(to: "${equipe}",
                subject: "Échec de la construction de ${BRANCH_NAME} : ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "${env.BUILD_URL}")
        }
        unstable {
            mail(to : "${equipe}",
                subject: "Constructionde ${BRANCH_NAME} instable : ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "${env.BUILD_URL}")
        }
    }
}