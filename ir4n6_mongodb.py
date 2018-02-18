""" ir4n6 custom MongoDB initiation script

Call via:
   mDB = ir4n6_mongodb.MongoDB(auth=True, mongodb_creds=credsDict)
   myColl = mDB.collection(coll_name='myCollection')
"""

import pymongo

__author__ = 'Paul Kincaid <paul@ir4n6.io>'

class MongoDB(object):
    """ ir4n6 custom MongoDB initiation and worker function

    Parameters
    ----------
    auth          : boolean -- (required) True = MongoDB auth enabled
    mongodb_creds : dict    -- (required if auth set)
        server   : string  -- MongoDB server - defaults to localhost
        port     : integer --  MongoDB server - defaults to 27017
        username : string  --  MongoDB username
        password : string  --  MongoDB user password
        database : string  --  Database to authenticate against and subsequently use

        Call via mDB = ip4n6_mongodb.MongoDB(auth=True, mongodb_creds=credsDict)
                 myColl = mDB.collection(coll_name='myCollection')
    """
    def __init__(self, auth, mongodb_creds):
        server = mongodb_creds['server']
        port = mongodb_creds['port']
        username = mongodb_creds['username']
        password = mongodb_creds['password']
        database = mongodb_creds['database']

        self.client = pymongo.MongoClient(server, port=port, username=username, password=password, authSource=database)
        self.db = self.client['{}'.format(database)]

    def collection(self, coll_name):
        """ Create or attach to a collection

        Parameters
        ----------
        coll_name : string -- (Required) Name of the collection

        Returns
        -------
        The collection object => make sure you assign to a variable in your program
        """
        self.coll_name = self.db['{}'.format(coll_name)]
        return self.coll_name

    def insert_one(self, coll_name, data):
        coll_name.insert_one(data)
