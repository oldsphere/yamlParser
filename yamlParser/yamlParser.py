#!/usr/bin/env python3
# Date: 28/11/2018 12:03:39
# Description:
#   Functions to parse YAML configuration files of Solstice

from ruamel import yaml

class DeepDict(dict):
    # - Constructor -
    def __init__(self, v):
        ''' Constructor (must be created from another dict '''
        dict.__init__(self, v)
        self._parent = v

    # - Public Method -
    def deepget(self, value, alt=None, parent=False):
        ''' Search on the content dictionaries for a given key
            Continue the search on the level below
        '''
        for k,v in self.items():
            if k == value:
                if parent:     return self._parent
                else:          return v

            if type(v) == dict:
                res = DeepDict(v).deepget(value, alt, parent)
                if res != alt:
                    return res

            if type(v) == list:
                res = DeepList(v).deepget(value, alt, parent)
                if res != alt:
                    return res

        return alt


class DeepList(list):
    # - Public Method -
    def deepget(self, value, alt=None, parent=False):
        ''' Search in the content dictionaries for a given key
            Continue the search on the level below
        '''
        for k in self:
            if type(k) == list:
                res = DeepList(k).deepget(value, alt, parent)
                if res != alt:
                    return res

            if type(k) == dict:
                res = DeepDict(k).deepget(value, alt, parent)
                if res != alt:
                    return res

        return alt


class YAMLNode:
    # - Constructor -
    def __init__(self, refObj={'null' : {}}):
        ''' Constructor '''
        assert(isNode(refObj))
        label = list(refObj.keys())[0]
        self._ref = refObj[label]
        self._isoDictParent = {}
        self._parent = refObj
        self._label = label
        self._parse()

    # - Public Methods -
    def get(self, value, alt=None):
        ''' Get subfunction '''

        if type(self._ref) == dict:
            return self._ref.get(value, alt or {})

        if type(self._ref) == list:

            if type(value) == str:
                if value in self.__dict__.keys():
                    return self.__dict__[value]
                return alt

            if value < len(self._ref):
                return self._ref[value]
            return alt or []

    def deepget(self, value, alt=None, parent=False):
        ''' Search for any dictionary with the key "value" '''

        if type(self._ref) == dict:
            return DeepDict(self._ref).deepget(value, alt, parent)

        if type(self._ref) == list:
            return DeepList(self._ref).deepget(value, alt, parent)

        else:
            print('Non structure reference')
            return alt

    def deepget_any(self, value_list, alt=None):
        ''' Search for any of the value of the list contained '''

        for value in value_list:
            res = self.deepget(value, alt)
            if res != alt:
                return res
        return alt

    def has(self, value):
        ''' Check if the value is contained in the element '''
        return self.get(value, 1) != 1

    def deephas(self, value):
        ''' Check if the value if contained by any of the structure elements '''
        return self.deepget(value, 1) != 1

    def has_any(self, valueList):
        ''' Check if any of the value is contained in the element '''
        return any([self.has(v) for v in valueList])

    def deephas_any(self, valueList):
        ''' Check if any of the value is contained by any of the structure elements'''
        return any([self.deephas(v) for v in valueList])

    def which_has(self, valueList):
        ''' Check which of the valueList element is contained if any '''
        for value in valueList:
            if self.deephas(value):
                return value

        return None

    def set(self, key, value):
        ''' Set a value to the referenced key '''
        self._ref[key] = value

    def deepset(self, **kwargs):
        ''' Set a value to a deep yreferenced key '''
        for k,v in kwargs.items():
            p = self.deepget(k, alt={}, parent=True)
            p[k] = v

    def dump(self):
        return yaml.dump(self._ref)

    # - Private Methdos -
    def _parse(self):
        ''' Auto parse '''

        if isNode(self._ref):
            node = YAMLNode(self._ref)
            self.__dict__[node._label] = node

        elif type(self._ref) == list:
            self._parse_list(self._ref)

        elif type(self._ref) == dict:
            self._parse_dict(self._ref)

        elif isSimpleData(self._ref):
            print('Warning: Missing simple data')

    def _parse_list(self, listObj):
        ''' Parse a list object '''

        nodes = [YAMLNode(obj) for obj in listObj
                if isNode(obj)]
        labels = [node._label for node in nodes]
        for label in set(labels):
            multi_nodes = [n for n in nodes if n._label == label]
            self.__dict__[label] = YAMLNodeCollection.create(multi_nodes)

    def _parse_dict(self, dictObj):
        ''' Parse a dictionary object '''

        for k, v in self._ref.items():

            self._isoDictParent[k] = dictObj
            if isSimpleData(v):
                self.__dict__[k] = self._ref[k]

            else:
                node = YAMLNode({k: v})
                self.__dict__[k] = node

    # - Operators -
    def __repr__(self):
        ''' Representation operation '''
        return self._ref.__repr__()

    def __getitem__(self, index):
        ''' Return the item if the object is a list '''

        return self._ref.__getitem__(index)


class YAMLNodeCollection(list):
    # - Operators -
    def __call__(self, multiple=False, **kwargs):
        ''' Allow callable reference

            Return the node matching the criteria.
            If multilple option is disabled returns the first occurence is any.
            Else it always return another YAMLNodeCollection.
        '''

        matches = self.copy()
        for k,v in kwargs.items():
            newMatches = [n for n in matches if n.get(k) == v]
            matches = newMatches.copy()

        if not matches:
            return

        if multiple:
            return YAMLNodeCollection.create(matches)
        else:
            return matches[0]

    # - Static Methods -
    def create(struct):
        ''' Determine which type of object create
            Avoid the 1 element list
        '''

        assert(type(struct) == list)
        #if len(struct) == 1:
        #    if isNode(struct[0]._ref):
        #        return YAMLNode(struct[0]._ref)
        return YAMLNodeCollection(struct)


###################################
#        Helper functions         #
###################################

def isNode(obj):
    ''' check if the object is a valid node

        valid nodes are dictionaries with a single entry
    '''

    if type(obj) == YAMLNode:
        return True

    if type(obj) == dict:
        if len(obj.keys()) == 1 and \
           not isSimpleData(list(obj.values())[0]):
            return True
    return False

def isNodeCollection(obj):
    ''' Check if the object is a Node collection '''

    if type(obj) == YAMLNodeCollection:
        return Ture

    if type(obj) == list:
        if all([isNode(s) for s in obj]):
            return True
    return False

def isSimpleData(obj):
    ''' Check if an object has no internal dictionaries '''

    if type(obj) == dict:
        return False

    if type(obj) == list:
        if not all([isSimpleData(v) for v in obj]):
            return False
    return True

def get_struct(casefile):
    ''' Return the YAML struct '''

    return yaml.load(open(casefile, 'r').read())

def createYAMLTree(casedata):
    ''' Return a YAML tree '''
    data = get_struct(casedata)
    return YAMLNode({'root' : data})

if __name__ == '__main__':

    CASEFILE = 'testCase/geometry.yaml'
    data = get_struct(CASEFILE)

    root = createYAMLTree(CASEFILE)

