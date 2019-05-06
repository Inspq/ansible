# -*- coding: utf-8 -*-

def isDictEquals(dict1, dict2, exclude = []):
    try:
        if type(dict1) is list and type(dict2) is list:
            if len(dict1) == 0 and len(dict2) == 0:
                return True
            found = False
            for item1 in dict1:
                if type(item1) is list:
                    found1 = False
                    for item2 in dict2:
                        if isDictEquals(item1, item2, exclude):
                            found1 = True
                    if found1:
                        found = True
                elif type(item1) is dict:
                    found1 = False
                    for item2 in dict2:
                        if isDictEquals(item1, item2, exclude):
                            found1 = True
                    if found1:
                        found = True
                else:
                    found1 = False
                    for item2 in dict2:
                        if item1 == item2:
                            found1 = True
                    if found1:
                        found = True
            return found
        elif type(dict1) is dict and type(dict2) is dict:
            if len(dict1) == 0 and len(dict2) == 0:
                return True
            for key in dict1:
                if not (exclude and key in exclude):
                    if not isDictEquals(dict1[key], dict2[key], exclude) :
                        return False
            return True
        else:
            return dict1 == dict2
    except KeyError:
        return False
    except Exception, e:
        raise e

import requests
def login(url, realm, username, password, clientid, clientSecret):
    '''
Fonction : login
Description :
    Cette fonction permet de s'authentifier sur le serveur Keycloak.
Arguments :
    url :
        type : str
        description :
            url de base du serveur Keycloak        
    realm :
        type : str
        description :
            realm du serveur Keycloak        
    username :
        type : str
        description :
            identifiant utiliser pour s'authentifier au serveur Keycloak        
    password :
        type : str
        description :
            Mot de passe pour s'authentifier au serveur Keycloak        
    '''
    # Login to Keycloak
    accessToken = ""
    if clientSecret == '':
        body = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': clientid
        }
    else:
        body = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': clientid,
            'client_secret': clientSecret
        }
    try:
        loginResponse = requests.post(url + '/auth/realms/' + realm + '/protocol/openid-connect/token',data=body)
    
        loginData = loginResponse.json()
        accessToken = loginData['access_token']
    except requests.exceptions.RequestException, e:
        raise e
    except ValueError, e:
        raise e

    return accessToken

def setHeaders(accessToken):
    bearerHeader = "bearer " + accessToken
    headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'}
    return headers

def loginAndSetHeaders(url, realm, username, password, clientid, clientSecret):
    headers = {}
    try:
        accessToken = login(url, realm, username, password, clientid, clientSecret)
        headers = setHeaders(accessToken)
    except Exception, e:
        raise e
    return headers