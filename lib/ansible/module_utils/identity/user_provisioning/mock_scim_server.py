import json

def mocked_scim_requests(*args, **kwargs):
    USERS = [
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test01",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test01",
                "version":None
            },
            "userName":"test01",
            "name":{
                "formatted":None,
                "familyName":"Test1",
                "givenName":"Test1",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test1@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test02",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test02",
                "version":None
            },
            "userName":"test02",
            "name":{
                "formatted":None,
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test2@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test03",
            "externalId":"5e771101-e3cd-4a77-851b-54f3f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test03",
                "version":None
            },
            "userName":"test03",
            "name":{
                "formatted":None,
                "familyName":"Test3",
                "givenName":"Test3",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test.test3@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },        
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test02",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test02",
                "version":None
            },
            "userName":"test02",
            "name":{
                "formatted":None,
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":"Test 02",
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test2@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
           "userName":"testes01",
           "displayName":None,
           "name":{
              "middleName":None,
              "givenName":"Test",
              "familyName":"Test"
           },
           "roles":[
              {
                 "display":"FA-SAISIE",
                 "primary":False
              }
           ],
           "id":"testes01",
           "schemas":[
              "urn:ietf:params:scim:schemas:core:2.0:User"
           ]
        }        
    ]        
    class MockResponse:
        def __init__(self, json_data, status_code):
            #self.json_data = json_data
            self.code = status_code
            if json_data is not None:                                                                                                  
                self.fp = json.dumps(json_data)                               
                self.json_data = json_data
            self.headers = {
                "dict": {
                    "connection":"close",
                    "content-type":"application/json;charset=UTF-8",
                    "date": "Wed, 30 Oct 2019 12:46:02 GMT",
                    "transfer-encoding": "chunked"
                },
                "headers":['Content-Type: application/json;charset=UTF-8\r\n', 'Transfer-Encoding: chunked\r\n', 'Date: Wed, 30 Oct 2019 12:46:02 GMT\r\n', 'Connection: close\r\n']
            }
                        
        def read(self):
            return self.fp

    if args[0] == 'http://scim.server.url/scim/v2/Users/.search' and kwargs["method"] == 'POST':
        if "data" in kwargs and USERS[1]["userName"] in kwargs["data"]:
            response = {
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
                "id": None,
                "externalId": None,
                "meta": None,
                "totalResults": 1,
                "Resources": [ USERS[1] ],
                "startIndex": 1,
                "itemsPerPage": 10
            }
        elif "data" in kwargs and USERS[0]["userName"] in kwargs["data"]:
            response = {
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
                "id": None,
                "externalId": None,
                "meta": None,
                "totalResults": 1,
                "Resources": [ USERS[0] ],
                "startIndex": 1,
                "itemsPerPage": 10
            }
        else:
            response = {
                "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
                "id": None,
                "externalId": None,
                "meta": None,
                "totalResults": 0,
                "Resources": [],
                "startIndex": 1,
                "itemsPerPage": 10
            }
            
        return MockResponse(
            response
            ,200)
        
    elif args[0] == 'http://scim.server.url/scim/v2/Users/' + USERS[1]["userName"] and kwargs["method"] == 'GET':
        return MockResponse(USERS[1], 200)

    elif args[0] == 'http://scim.server.url/scim/v2/Users' and kwargs["method"] == 'POST':
        if "data" in kwargs and "externalId" not in kwargs["data"]:
            response = {
                "schemas":["urn:ietf:params:scim:api:messages:2.0:Error"],
                "id":None,
                "externalId":None,
                "status":400,
                "meta":None,
                "scimType":None,
                "detail":"External Id must be specified"
            }
            return(MockResponse(response, 400))
        if "data" in kwargs:
            for user in USERS:
                if user["userName"] in kwargs["data"]:
                    if "externalId" not in user:
                        user["externalId"] =  json.loads(kwargs["data"])["externalId"]
                    return MockResponse(user, 201)
            
        return MockResponse(None, 400)

    elif args[0] == 'http://scim.server.url/scim/v2/Users/' + USERS[0]["userName"] and kwargs["method"] == 'DELETE':
        return MockResponse(None, 204)

    elif args[0] == 'http://scim.server.url/scim/v2/Users/' + USERS[1]["userName"] and kwargs["method"] == 'PUT':
        if "data" in kwargs and "externalId" not in kwargs["data"]:
            response = {
                "schemas":["urn:ietf:params:scim:api:messages:2.0:Error"],
                "id":None,
                "externalId":None,
                "status":400,
                "meta":None,
                "scimType":None,
                "detail":"External Id must be specified"
            }
            return(MockResponse(response, 400))
        if "data" in kwargs:
            return MockResponse(json.loads(kwargs["data"]), 204)
            #for user in USERS:
            #    if user["userName"] in kwargs["data"]:
            #        user["externalId"] =  json.loads(kwargs["data"])["externalId"]
            #        return MockResponse(user, 204)
    
    return MockResponse(None, 404)
