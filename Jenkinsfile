#!/usr/bin/env groovy
pipeline {
    agent any
    triggers { pollSCM('H/15 * * * *') }
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }
/*
    tools {
        jdk 'JDK1.8.0_65'
        maven 'M3'
    }
*/
    stages {
        stage('Environnement pour les tests') {
            steps {
                script {
                    BRANCH_NAME = 'trunk'
                    keycloak_svn_url = "http://svn.inspq.qc.ca/svn/inspq/dev/Inspq.SX5/trunk/keycloak"
                }
            }
        }
        stage ('Checkout de keycloak') {
            echo 'Checkout de keycloak ' + BRANCH_NAME
            steps {
                sh "if [ ! -d keycloak ]; then svn checkout ${keycloak_svn_url} keycloak; fi;"
                sh "ls -al"
            }
        }
        stage ('Tests unitaires du module ansible de Keycloak') {
            steps {
                sh "source hacking/env-setup; ansible-test sanity --test validate-modules"
                sh "touch ansible.cfg"
                sh "printf '[defaults]\nroles_path=${WORKSPACE}/rolesansible/roles\nlibrary=${WORKSPACE}/lib/ansible/modules:library\nmodule_utils=${WORKSPACE}/lib/ansible/module_utils:module_utils\n' >> ansible.cfg"
                sh "source hacking/env-setup; ansible-playbook keycloak/createUnitEnv.yml -i keycloak/UNIT/UNIT.hosts"
                sh "source hacking/env-setup; nosetests --with-xunit test/units/module_utils/test_keycloak_utils.py test/units/modules/identity/keycloak/test_keycloak*.py"
                sh "source hacking/env-setup; ansible-playbook keycloak/cleanupUnitEnv.yml -i keycloak/UNIT/UNIT.hosts"
            }
            post {
                success {
                    junit '**/nosetests.xml'
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