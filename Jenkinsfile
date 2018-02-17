#!/usr/bin/env groovy
pipeline {
    agent any
    triggers { pollSCM('H/15 * * * *') }
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Environnement pour les tests') {
            steps {
                script {
                    BRANCH_NAME = 'trunk'
                }
            }
        }
        stage ('Checkout de keycloak') {
            steps {
                checkout([$class: 'SubversionSCM',
                        additionalCredentials: [],
                        excludedCommitMessages: '',
                        excludedRegions: '',
                        excludedRevprop: '',
                        excludedUsers: '',
                        filterChangelog: false,
                        ignoreDirPropChanges: false,
                        includedRegions: '',
                        locations: [[credentialsId: '30020735-8a8a-4209-bcb1-35b991e3b7ba',
                                    depthOption: 'infinity',
                                    ignoreExternalsOption: true,
                                    local: 'keycloak',
                                    remote: "http://svn.inspq.qc.ca/svn/inspq/dev/Inspq.SX5/trunk/keycloak"]],
                        workspaceUpdater: [$class: 'UpdateUpdater']])
            }
        }
        stage ('Configurer Ansible') {
            steps {
                checkout([$class: 'SubversionSCM',
                        additionalCredentials: [],
                        excludedCommitMessages: '',
                        excludedRegions: '',
                        excludedRevprop: '',
                        excludedUsers: '',
                        filterChangelog: false,
                        ignoreDirPropChanges: false,
                        includedRegions: '',
                        locations: [[credentialsId: '30020735-8a8a-4209-bcb1-35b991e3b7ba',
                                    depthOption: 'infinity',
                                    ignoreExternalsOption: true,
                                    local: 'roles',
                                    remote: "http://svn.inspq.qc.ca/svn/inspq/infrastructure/ansible/trunk/roles"]],
                        workspaceUpdater: [$class: 'UpdateUpdater']])
                sh "touch ansible.cfg"
                sh "printf '[defaults]\nroles_path=roles\nhost_key_checking = False' > ansible.cfg"
            }
        }
        stage ('Tests unitaires du module ansible de Keycloak') {
            steps {
                // sh "source hacking/env-setup; ansible-test sanity --test validate-modules"
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
            script {
                equipe = 'mathieu.couture@inspq.qc.ca,etienne.sadio@inspq.qc.ca,soleman.merchan@inspq.qc.ca,philippe.gauthier@inspq.qc.ca,pierre-olivier.chiasson@inspq.qc.ca,eric.parent@inspq.qc.ca'
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