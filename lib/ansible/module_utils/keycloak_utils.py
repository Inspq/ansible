#!/usr/bin/python
# -*- coding: utf-8 -*-
def isDictEquals(dict1, dict2, exclude = []):
    '''
Fonction: isDictEquals
Description:    Cette fonction compare deux structures. Elle utilise tous les étéments de la structure 
                dict1 et valide que ses éléments se trouvent dans la structure dict2.
                Ca ne veut pas dire que les deux structures sont identiques, Il peut y avoir des 
                éléments dans dict2 qui ne sont pas dans dict1.
                Cette fonction est récursive et elle peut s'appeler avec des arguments qui ne sont pas
                de type dict
Arguments:
    dict1 : 
        type : 
            dict pour l'appel de base, peut être de type dict, list, bool, int ou str pour les appels récursifs
        description :
            structure de référence.
    dict2 : 
        type : 
            dict pour l'appel de base, peut être de type dict, list, bool, int ou str pour les appels récursifs
        description :
            structure avec laquelle comparer la structure dict1.
    exclude :
        type:
            list
        description :
            liste des clés à ne pas comparer
        valeur par défaut : liste vide
Retour:
    type:
        bool
    description:
        Retourne vrai (True) si tous les éléments de dict1 se retrouvent dans dict2
        Retourne faux (False), sinon
    '''
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
