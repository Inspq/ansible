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

def login(url, username, password):
    '''
Fonction : login
Description :
    Cette fonction permet de s'authentifier sur le serveur Keycloak.
Arguments :
    url :
        type : str
        description :
            url de base du serveur Keycloak        
    username :
        type : str
        description :
            identifiant � utiliser pour s'authentifier au serveur Keycloak        
    password :
        type : str
        description :
            Mot de passe pour s'authentifier au serveur Keycloak        
    '''
    # Login to Keycloak
    accessToken = ""
    body = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': 'admin-cli'
    }
    try:
        loginResponse = requests.post(url + '/auth/realms/master/protocol/openid-connect/token',data=body)
    
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

def loginAndSetHeaders(url, username, password):
    headers = {}
    try:
        accessToken = login(url, username, password)
        headers = setHeaders(accessToken)
    except Exception, e:
        raise e
    return headers

def sx5RestClientget(url,clientName,realm):
    dataResponse=None
    body = {
            'clientId': clientName,
            'realmId': realm
    }
    try:
        dataResponse = requests.get(url + '/search/findByRealmIdAndClientId',params=body)
    
    except requests.exceptions.RequestException, e:
        raise e
    except ValueError, e:
        raise e
    
    return dataResponse

def sx5RestClientAdd(url,clientName,realm,clientUrl,username,password):
    result = False
    body = {
            "clientId": clientName,
            "realmId": realm,
            "url": clientUrl,
            "username": username,
            "password": password
    }
    try:
        getResponse = requests.post(url,json=body)
        dataResponse = getResponse.json()
        if dataResponse['clientId'] is clientName:
            result = true
        
    except requests.exceptions.RequestException, e:
        raise e
    except ValueError, e:
        raise e
    
    return result

def sx5RestClientUpdate(url,id,clientName,realm,clientUrl,username,password):
    result = False
    body = {
            "clientId": clientName,
            "realmId": realm,
            "url": clientUrl,
            "username": username,
            "password": password
    }
    try:
        getResponse = requests.put(url+'/'+str(id),json=body)
        dataResponse = getResponse.json()
        if dataResponse['clientId'] is clientName and dataResponse['realmId'] is realm and dataResponse['url'] is clientUrl:
            result = true
        
    except requests.exceptions.RequestException, e:
        raise e
    except ValueError, e:
        raise e
    
    return result

def sx5RestClientCreat(url,clientName,realm,clientUrl,username,password):
    dataResponse=""
    try:
        getResponse = sx5RestClientget(url,clientName,realm)
        if getResponse.status_code == 200:
            dataResponse = getResponse.json()
            sx5RestClientUpdate(url,dataResponse['id'],clientName,realm,clientUrl,username,password)
        else:
            addTest = sx5RestClientAdd(url,clientName,realm,clientUrl,username,password)
            if addTest:
                dataResponse = sx5RestClientget(url,clientName,realm)
    except requests.exceptions.RequestException, e:
        raise e
    except ValueError, e:
        raise e
    
    return dataResponse