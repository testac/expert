'''learn.py

Collect a bunch of facts about Plants from dbpedia.
'''

import os
import os.path
import rdflib

DEFAULT_DATA_DIR = 'data'

def main():
    # DBPedia's definition of a Plant.
    DBPEDIA_PLANT_URI = 'http://dbpedia.org/resource/Plant'
    # Setting up the global SPARQL namespace.
    NS = {
        'dbpedia-owl': rdflib.Namespace('http://dbpedia.org/ontology/'),
    }

    # A few magic incantations to turn on SPARQL in rdflib.
    rdflib.plugin.register('sparql', rdflib.query.Processor,
                           'rdfextras.sparql.processor', 'Processor')
    rdflib.plugin.register('sparql', rdflib.query.Result,
                           'rdfextras.sparql.query', 'SPARQLQueryResult')

    # Our graph of plant information.
    g = rdflib.Graph()

    # Start by crawling the Plant fact file.
    print 'Learning about %s ...' % DBPEDIA_PLANT_URI
    g.parse(DBPEDIA_PLANT_URI)

    # For each entity that is in the kingom of plants, learn facts about that
    # plant.
    for plant_uri in g.query('SELECT ?s WHERE { ?s dbpedia-owl:kingdom ?o }',
            initNs=NS):
        print 'Learning about %s ...' % plant_uri
        g.parse(plant_uri)

    print 'Learned %d facts.' % len(g)

    # Write down what we've learned so that way we don't have to recrawl it!
    filename = os.path.join(os.environ.get('DATA_DIR', DEFAULT_DATA_DIR),
                'plants_from_dbpedia.rdf')
    print 'Writing facts down in %s ...' % filename
    g.serialize(filename)
    print 'Done.'

if __name__ == '__main__':
    main()
