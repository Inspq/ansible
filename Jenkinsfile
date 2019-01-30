#!/usr/bin/env groovy
pipeline {
    agent any
    triggers { pollSCM('H/15 * * * *') }
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }

    stages {
        stage ('Configurer Ansible') {
            steps {
                sh "printf '[defaults]\nroles_path=roles\nhost_key_checking = False' > ansible.cfg"
            	sh "source hacking/env-setup; ansible-galaxy install -r requirements.yml"
            }
        }
        stage ('Validation des modules ansibles') {
            steps {
                sh "source hacking/env-setup; ansible-test sanity --test validate-modules"
           	}
        }
        stage ('Tests sécurités des modules ansible sx5') {
            steps {
                sh "docker run -u root --rm -v ${WORKSPACE}/lib/ansible/modules/identity/sx5:/app nexus3.inspq.qc.ca:5000/inspq/bandit:SNAPSHOT bandit -r ./"
           	}
        }
        stage ('Tests sécurités des modules ansible Keycloak') {
            steps {
                script {
                    try{
                        sh "docker run -u root --rm -v ${WORKSPACE}/lib/ansible/modules/identity/keycloak:/app nexus3.inspq.qc.ca:5000/inspq/bandit:SNAPSHOT bandit -r ./"
                    }
                    catch (exc){
                        currentStage.result = 'FAILURE'
                        currentBuild.result = 'UNSTABLE'
                    }
                }
           	}
        }
        stage ('Tests unitaires des modules ansible de Keycloak sur la dernière version de Keycloak') {
            steps {
                sh "source hacking/env-setup; ansible-playbook -i keycloak.hosts -e docker_image=nexus3.inspq.qc.ca:5000/inspq/keycloak -e docker_image_version=latest deploy-keycloak.yml"
                script {
                    try {
		                sh "source hacking/env-setup; nosetests --with-xunit --xunit-file=nosetests-keycloak.xml test/units/module_utils/test_keycloak_utils.py test/units/modules/identity/keycloak/test_keycloak_authentication.py test/units/modules/identity/keycloak/test_keycloak_client.py test/units/modules/identity/keycloak/test_keycloak_group.py test/units/modules/identity/keycloak/test_keycloak_identity_provider.py test/units/modules/identity/keycloak/test_keycloak_realm.py test/units/modules/identity/keycloak/test_keycloak_role.py test/units/modules/identity/keycloak/test_keycloak_user.py test/units/modules/identity/keycloak/test_keycloak_component.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                sh "source hacking/env-setup; ansible-playbook -i keycloak.hosts cleanup-keycloak.yml"
            }
            post {
                success {
                    junit '**/nosetests-keycloak.xml'
                }
                unstable{
                    junit '**/nosetests-keycloak.xml'
                }
            }
        }
        stage ('Tests unitaires des modules ansible de Keycloak sur la dernière version de RHSSO') {
            steps {
                sh "source hacking/env-setup; ansible-playbook -i keycloak.hosts -e docker_image=nexus3.inspq.qc.ca:5000/inspq/rhsso -e docker_image_version=latest deploy-keycloak.yml"
                script {
                    try {
		                sh "source hacking/env-setup; nosetests --with-xunit --xunit-file=nosetests-rhsso.xml test/units/module_utils/test_keycloak_utils.py test/units/modules/identity/keycloak/test_keycloak_authentication.py test/units/modules/identity/keycloak/test_keycloak_client.py test/units/modules/identity/keycloak/test_keycloak_group.py test/units/modules/identity/keycloak/test_keycloak_identity_provider.py test/units/modules/identity/keycloak/test_keycloak_realm.py test/units/modules/identity/keycloak/test_keycloak_role.py test/units/modules/identity/keycloak/test_keycloak_user.py test/units/modules/identity/keycloak/test_keycloak_component.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                sh "source hacking/env-setup; ansible-playbook -i keycloak.hosts cleanup-keycloak.yml"
            }
            post {
                success {
                    junit '**/nosetests-rhsso.xml'
                }
                unstable{
                    junit '**/nosetests-rhsso.xml'
                }
            }
        }
      stage ('Tests unitaires des modules ansible de sx5-sp-config') {
            steps {
                sh "source hacking/env-setup; ansible-playbook -i keycloak.hosts -e docker_image=nexus3.inspq.qc.ca:5000/inspq/keycloak -e docker_image_version=latest deploy-keycloak.yml"
                sh "source hacking/env-setup; ansible-playbook -i sx5-sp-config.hosts -e sx5spconfig_image_version=0.0.1-SNAPSHOT deploy-sx5-sp-config.yml"
                script {
                    try {
		                sh "source hacking/env-setup; nosetests --with-xunit --xunit-file=nosetests-sx5-sp-config.xml test/units/module_utils/test_sx5_sp_config_system_utils.py test/units/modules/identity/sx5/test_sx5_sp_config_system.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                sh "source hacking/env-setup; ansible-playbook -i sx5-sp-config.hosts cleanup-sx5-sp-config.yml"
                sh "source hacking/env-setup; ansible-playbook -i keycloak.hosts cleanup-keycloak.yml"
            }
            post {
                success {
                    junit '**/nosetests-sx5-sp-config.xml'
                }
                unstable{
                    junit '**/nosetests-sx5-sp-config.xml'
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
                if (currentBuild.getPreviousBuild() != null && currentBuild.getPreviousBuild().getResult().toString() != "SUCCESS") {
                    mail(to: "${equipe}", 
                        subject: "Tests unitaires des modules Ansible pour Keycloak réalisée avec succès: ${env.JOB_NAME} #${env.BUILD_NUMBER}", 
                        body: "${env.BUILD_URL}")
                }
            }
        }
        failure {
            mail(to: "${equipe}",
                subject: "Échec des tests unitaires des modules Ansible pour Keycloak : ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "${env.BUILD_URL}")
        }
        unstable {
            mail(to : "${equipe}",
                subject: "Tests unitaires des modules Ansible pour Keycloak instable : ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "${env.BUILD_URL}")
        }
    }
}