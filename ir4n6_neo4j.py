# Simple function to create two nodes and a relationship between them
#      session.write_transaction(n4j_use, <Node1 Type>, <Node1 Value>, <RELATIONSHIP>, <Node2 Type>, <Node2 Value>)
#
# n4j = Neo4j()
# with n4j.driver.session() as session:
#   session.write_transaction(n4j.n4j_use, "Instance", "{name: 'test', myID: '123'}", 'SOMETHING', "test", "{name: 'test'}")

import sys

class Neo4j(object):
    """ Neo4j Populating Script

    Parameters
    ----------
    server_ip : string           -- Neo4j Server IP Address - defaults to localhost
    auth      : (user, password) -- Neo4j Username and Password - defaults to 'Neo4j' and 'password'
    flush     : <bool>           --  Flush Neo4j graph database prior to use

    Returns
    -------
    Neo4j object that can be used to populate the graph database

    Raises
    ------
    ImportError: missing neo4j-driver library

    Examples
    --------
    In [1]: from ir4n6_neo4j import *
       ...: n4j = Neo4j()
       ...: with n4j.driver.session() as session:
       ...:     session.write_transaction(n4j.n4j_use, "Instance", "{name: 'test', myID: '123'}", 'SOMETHING', "test", "{name: 'test'}")
       ...:     session.write_transaction(n4j.n4j_use, "Instance", "{{name: '{}', myID: '123'}}".format(some_var), 'SOMETHING', "test", "{name: 'test'}")
    """

    def __init__(self, server_ip='localhost', auth=("neo4j", "password"), flush=0):
        try:
            from neo4j.v1 import GraphDatabase
            try:
                self.driver = GraphDatabase.driver("bolt://{}:7687".format(server_ip), auth=auth)
                print("Connected to Neo4j on bolt://localhost:7687")
                #print("Using Neo4j - Populating Neo4j Graph DB")
                if flush:
                    # We'll flush collections to clear out the DB so we can preserve authentication
                    print
                    print("******************************************************************************")
                    print("* You selected 'flush_neo4j' - this will flush all entries in the Neo4j DB!!!!")
                    print("******************************************************************************")
                    choice = input("Are you sure (Y/N)???? ").upper()
                    if choice == 'Y':
                        sure = input("ARE YOU SURE(Y/N) YOU WANT TO DELETE THE NEO4J DATABASE??????? ").upper()
                        if sure == 'Y':
                            pass
                            with self.driver.session() as session:
                                session.write_transaction(self.n4j_flush)
                        else:
                            print("Then please remove '--flush_neo4j' from the command line arguments :)")
                            print("Exiting")
                            sys.exit()
            except:
                print
                print("****** ERROR ******")
                print("Cannot connect to Neo4j - http://localhost:7687")
                sys.exit()

        except ImportError:
            print("Missing Neo4j Python Module")
            print(" 'pip install neo4j-driver'")
            sys.exit()

    def n4j_flush(self, tx):
        """ Flush the Neo4j Graph Database prior to using it.

        Utilized via the 'flush' keyword in the instantiation call

        Example
        -------
        In [1]: from ir4n6_neo4j import *
           ...: n4j = Neo4j(flush=1)
        """
        tx.run('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r')

    def n4j_use(self, tx, type1, properties1, relationship, type2, properties2):
        """
        Add nodes and the relationship between

        Parameters
        ----------
        # session.write_transaction(n4j_use, <Node1 Type>, <Node1 Value>, <RELATIONSHIP>, <Node2 Type>, <Node2 Value>)
        node1_type   : string
        node1_value  : key/value pair -- "{name: node_name}"
        relationship : string documenting the relationship between Node1 and Node2
        node2_type   : string
        node2_value  : key/value pair -- "{name: node_name}" or "{{name: '{}'}".format(some_var)

        It is possible that the key/value pair is enclosed in another set of brackets, depending on the version of python
         and the formatting string functions that are used (e.g., "{{name: '{}'}}".format(some_var))

        Returns
        -------
        No return value

        Example
        -------
        In [5]: with n4j.driver.session() as session:
           ...:     session.write_transaction(n4j.n4j_use, "Instance", "{name: 'test', myID: '123'}", 'SOMETHING', "test", "{name: 'test'}")
        """
        tx.run("""MERGE (a:{} {})
                    MERGE (b:{} {})
                    MERGE (a)-[:{}]->(b)""".format(type1, properties1, type2, properties2, relationship))

#from neo4j.v1 import GraphDatabase
#def n4j_use(tx, type1, properties1, relationship, type2, properties2):
#    tx.run("""MERGE (a:{} {})
#                MERGE (b:{} {})
#                MERGE (a)-[:{}]->(b)""".format(type1, properties1, type2, properties2, relationship))

#def n4j_use_old(tx, type1, name1, relationship, type2, name2):
#    tx.run("MERGE (a:" + type1 + " {name: $name1}) "
#            "MERGE (b:" + type2 + " {name: $name2})"
#            "MERGE (a)-[:" + relationship + "]->(b) ",
#            name1=name1, name2=name2)

#def graphdb(server_ip, auth):
#    return GraphDatabase.driver("bolt://{}:7687".format(server_ip), auth=auth)

#MERGE (a:AAAAA {name:'asdf', blah:'dfgs'})
