#!/usr/bin/env groovy
pipeline {
    agent any
    triggers { pollSCM('H/15 * * * *') }
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }
	environment{
	    KEYCLOAK_IMAGE='jboss/keycloak'
	    KEYCLOAK_VERSION='10.0.2'
	    RHSSO_IMAGE='nexus3.inspq.qc.ca:5000/inspq/rhsso'
	    RHSSO_VERSION='latest'
	    THREEEIGHTYNINEDS_IMAGE='minkwe/389ds'
	    THREEEIGHTYNINEDS_VERSION='latest'
	    SX5SPCONFIG_IMAGE='nexus3.inspq.qc.ca:5000/inspq/sx5-sp-config'
	    SX5SPCONFIG_VERSION='latest'
	    EMAIL_TO = 'mathieu.couture@inspq.qc.ca,etienne.sadio@inspq.qc.ca,soleman.merchan@inspq.qc.ca,philippe.gauthier@inspq.qc.ca,pierre-olivier.chiasson@inspq.qc.ca,eric.parent@inspq.qc.ca'
	}

    stages {
        stage ('Configurer Ansible') {
            steps {
                sh "printf '[defaults]\nroles_path=roles\nhost_key_checking = False' > ansible.cfg"
            	sh "ansible-galaxy install -r requirements.yml"
            }
        }
        stage ('Validation des modules ansibles') {
            steps {
                sh "python3 bin/ansible-test sanity --test pep8 lib/ansible/module_utils/keycloak.py lib/ansible/modules/identity/keycloak/keycloak_user.py lib/ansible/modules/identity/keycloak/keycloak_authentication.py lib/ansible/modules/identity/keycloak/keycloak_client.py lib/ansible/modules/identity/keycloak/keycloak_clienttemplate.py lib/ansible/modules/identity/keycloak/keycloak_component.py lib/ansible/modules/identity/keycloak/keycloak_group.py lib/ansible/modules/identity/keycloak/keycloak_identity_provider.py lib/ansible/modules/identity/keycloak/keycloak_realm.py lib/ansible/modules/identity/keycloak/keycloak_role.py lib/ansible/modules/identity/sx5/sx5_habilitation.py lib/ansible/modules/identity/sx5/sx5_sp_config_system.py lib/ansible/modules/identity/user_provisioning/scim_user.py"            
                // sh "python3 bin/ansible-test sanity --test validate-modules lib/ansible/module_utils/keycloak.py lib/ansible/modules/identity/keycloak/keycloak_user.py lib/ansible/modules/identity/keycloak/keycloak_authentication.py lib/ansible/modules/identity/keycloak/keycloak_client.py lib/ansible/modules/identity/keycloak/keycloak_clienttemplate.py lib/ansible/modules/identity/keycloak/keycloak_component.py lib/ansible/modules/identity/keycloak/keycloak_group.py lib/ansible/modules/identity/keycloak/keycloak_identity_provider.py lib/ansible/modules/identity/keycloak/keycloak_realm.py lib/ansible/modules/identity/keycloak/keycloak_role.py lib/ansible/modules/identity/sx5/sx5_habilitation.py lib/ansible/modules/identity/sx5/sx5_sp_config_system.py lib/ansible/modules/identity/user_provisioning/scim_user.py"
                sh "python3 bin/ansible-test sanity --test validate-modules lib/ansible/module_utils/keycloak.py lib/ansible/modules/identity/keycloak/keycloak_user.py lib/ansible/modules/identity/keycloak/keycloak_authentication.py lib/ansible/modules/identity/keycloak/keycloak_client.py lib/ansible/modules/identity/keycloak/keycloak_clienttemplate.py lib/ansible/modules/identity/keycloak/keycloak_component.py lib/ansible/modules/identity/keycloak/keycloak_group.py lib/ansible/modules/identity/keycloak/keycloak_identity_provider.py lib/ansible/modules/identity/keycloak/keycloak_realm.py lib/ansible/modules/identity/keycloak/keycloak_role.py lib/ansible/modules/identity/sx5/sx5_habilitation.py lib/ansible/modules/identity/user_provisioning/scim_user.py"
           	}
        }
        stage ('Tests sécurités des modules ansible sx5') {
            steps {
                script {
                    try{
                        sh "docker run -u root --rm -v ${WORKSPACE}/lib/ansible/modules/identity/sx5:/app nexus3.inspq.qc.ca:5000/inspq/bandit:SNAPSHOT bandit -r -s B608 ./"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
           	}
        }
        stage ('Tests sécurités des modules ansible Keycloak') {
            steps {
                script {
                    try{
                        sh "docker run -u root --rm -v ${WORKSPACE}/lib/ansible/modules/identity/keycloak:/app nexus3.inspq.qc.ca:5000/inspq/bandit:SNAPSHOT bandit -r -s B501,B105 ./"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
           	}
        }
        stage ('Tests sécurités des modules ansible SCIM') {
            steps {
                script {
                    try{
                        sh "docker run -u root --rm -v ${WORKSPACE}/lib/ansible/modules/identity/user_provisioning:/app nexus3.inspq.qc.ca:5000/inspq/bandit:SNAPSHOT bandit -r -s B501,B105 ./"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
           	}
        }
        stage ('Tests unitaires des modules ansible de Keycloak sur la dernière version de Keycloak') {
            steps {
                sh "docker run -d --rm --name testldap -p 10389:389 ${THREEEIGHTYNINEDS_IMAGE}:${THREEEIGHTYNINEDS_VERSION}"
                sh "docker run -d --rm --name testkc -p 18081:8080 --link testldap:testldap -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -e KEYCLOAK_CONFIG=standalone-test.xml ${KEYCLOAK_IMAGE}:${KEYCLOAK_VERSION}"
                sh '''
                until $(curl --output /dev/null --silent --head --fail http://localhost:18081/auth)
                do 
                	printf '.'
                	sleep 5
                done
                '''
                script {
                    try {
		                sh "nosetests --with-xunit --xunit-file=nosetests-keycloak.xml test/units/module_utils/test_keycloak_utils.py test/units/modules/identity/keycloak/test_keycloak_authentication.py test/units/modules/identity/keycloak/test_keycloak_client.py test/units/modules/identity/keycloak/test_keycloak_group.py test/units/modules/identity/keycloak/test_keycloak_identity_provider.py test/units/modules/identity/keycloak/test_keycloak_realm.py test/units/modules/identity/keycloak/test_keycloak_role.py test/units/modules/identity/keycloak/test_keycloak_user.py test/units/modules/identity/keycloak/test_keycloak_component.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                sh "docker stop testkc"
                sh "docker stop testldap"
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
                sh "docker run -d --rm --name testldap -p 10389:389 ${THREEEIGHTYNINEDS_IMAGE}:${THREEEIGHTYNINEDS_VERSION}"
                sh "docker run -d --rm --name testrhsso -p 18081:8080 --link testldap:testldap -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -e KEYCLOAK_CONFIG=standalone-test.xml ${RHSSO_IMAGE}:${RHSSO_VERSION}"
                sh '''
                until $(curl --output /dev/null --silent --head --fail http://localhost:18081/auth)
                do 
                	printf '.'
                	sleep 5
                done
                '''
                script {
                    try {
		                sh "nosetests --with-xunit --xunit-file=nosetests-rhsso.xml test/units/module_utils/test_keycloak_utils.py test/units/modules/identity/keycloak/test_keycloak_authentication.py test/units/modules/identity/keycloak/test_keycloak_client.py test/units/modules/identity/keycloak/test_keycloak_group.py test/units/modules/identity/keycloak/test_keycloak_identity_provider.py test/units/modules/identity/keycloak/test_keycloak_realm.py test/units/modules/identity/keycloak/test_keycloak_role.py test/units/modules/identity/keycloak/test_keycloak_user.py test/units/modules/identity/keycloak/test_keycloak_component.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                sh "docker stop testrhsso"
                sh "docker stop testldap"
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
                sh "docker run -d --rm --name testkc -p 18081:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -e KEYCLOAK_CONFIG=standalone-test.xml ${KEYCLOAK_IMAGE}:${KEYCLOAK_VERSION}"
                sh '''
                until $(curl --output /dev/null --silent --head --fail http://localhost:18081/auth)
                do 
                	printf '.'
                	sleep 5
                done
                '''
                sh "ansible-playbook -i sx5-sp-config.hosts -e sx5spconfig_image_version=${SX5SPCONFIG_VERSION} deploy-sx5-sp-config.yml"
                script {
                    try {
		                sh "source hacking/env-setup; nosetests --with-xunit --xunit-file=nosetests-sx5-sp-config.xml test/units/module_utils/test_sx5_sp_config_system_utils.py test/units/modules/identity/sx5/test_sx5_sp_config_system.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                sh "ansible-playbook -i sx5-sp-config.hosts cleanup-sx5-sp-config.yml"
                sh "docker stop testkc"
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
        stage ('Tests unitaires des modules ansible de sx5-habilitation') {
            steps {
                sh "docker run -d --rm --name testkc -p 18081:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -e KEYCLOAK_CONFIG=standalone-test.xml ${KEYCLOAK_IMAGE}:${KEYCLOAK_VERSION}"
                sh '''
                until $(curl --output /dev/null --silent --head --fail http://localhost:18081/auth)
                do 
                	printf '.'
                	sleep 5
                done
                '''
                sh "ansible-playbook -i sx5-sp-config.hosts -e sx5spconfig_image_version=${SX5SPCONFIG_VERSION} deploy-sx5-sp-config.yml"
                script {
                    try {
		                sh "source hacking/env-setup; cd test; nosetests --with-xunit --xunit-file=nosetests-sx5-sp-config.xml units/modules/identity/sx5/test_sx5_habilitation.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
                sh "ansible-playbook -i sx5-sp-config.hosts cleanup-sx5-sp-config.yml"
                sh "docker stop testkc"
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
        stage ('Tests unitaires des modules ansible SCIM') {
            steps {
                script {
                    try {
		                sh "source hacking/env-setup; cd test; nosetests --with-xunit --xunit-file=nosetests-scim.xml units/module_utils/identity/user_provisioning/test_scim.py units/modules/identity/user_provisioning/test_scim_user.py"
                    }
                    catch (exc){
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                success {
                    junit '**/nosetests-scim.xml'
                }
                unstable{
                    junit '**/nosetests-scim.xml'
                }
            }
        }
        
    }
    post {
        success {
            script {
                if (currentBuild.getPreviousBuild() != null && currentBuild.getPreviousBuild().getResult().toString() != "SUCCESS") {
                    mail(to: "${EMAIL_TO}", 
                        subject: "Tests unitaires des modules Ansible pour Keycloak réalisée avec succès: ${env.JOB_NAME} #${env.BUILD_NUMBER}", 
                        body: "${env.BUILD_URL}")
                }
            }
        }
        failure {
            mail(to: "${EMAIL_TO}",
                subject: "Échec des tests unitaires des modules Ansible pour Keycloak : ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "${env.BUILD_URL}")
        }
        unstable {
            mail(to : "${EMAIL_TO}",
                subject: "Tests unitaires des modules Ansible pour Keycloak instable : ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "${env.BUILD_URL}")
        }
    }
}