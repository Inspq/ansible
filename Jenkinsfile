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

                sh "rm -rf ansible"
                sh "rm -rf ansible-core-sitemap.xml"
                sh "rm -rf bin"
                sh "rm -rf CHANGELOG.md"
                sh "rm -rf CODING_GUIDELINES.md"
                sh "rm -rf contrib"
                sh "rm -rf CONTRIBUTING.md"
                sh "rm -rf COPYING"
                sh "rm -rf .coveragerc"
                sh "rm -rf docs"
                sh "rm -rf docsite_requirements.txt"
                sh "rm -rf examples"
                sh "rm -rf .git"
                sh "rm -rf .gitattributes"
                sh "rm -rf .github"
                sh "rm -rf .gitignore"
                sh "rm -rf .gitmodules"
                sh "rm -rf hacking"
                sh "rm -rf lib"
                sh "rm -rf .mailmap"
                sh "rm -rf Makefile"
                sh "rm -rf MANIFEST.in"
                sh "rm -rf MODULE_GUIDELINES.md"
                sh "rm -rf packaging"
                sh "rm -rf README.md"
                sh "rm -rf RELEASES.txt"
                sh "rm -rf requirements.txt"
                sh "rm -rf ROADMAP.rst"
                sh "rm -rf .settings"
                sh "rm -rf setup.py"
                sh "rm -rf shippable.yml"
                sh "rm -rf test"
                sh "rm -rf ticket_stubs"
                sh "rm -rf tox.ini"
                sh "rm -rf VERSION"
                sh "rm -rf .yamllint"

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