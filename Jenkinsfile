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
                    fa_svn_url = 'http://svn.inspq.qc.ca/svn/inspq/dev/FA/branches/Keycloak'
                }
                echo 'Obtention de... ' + BRANCH_NAME
//                sh "svn checkout ${fa_svn_url} ${WORKSPACE}/FA"
                sh "ls -al"
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