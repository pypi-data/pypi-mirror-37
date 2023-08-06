import pronto
import json
import tarfile
import tempfile
from requests import get
import shutil
import os, sys
import pkgutil


def update_ontology():
    """
    Download latest ontology from CARD and extract aro.obo file to ~/.card-trick/
    """
    url = 'https://card.mcmaster.ca/latest/ontology'
    _, file_name = tempfile.mkstemp('.tar.bz2')
    dest_dir = tempfile.mkdtemp()
    
    # get latest database file and write to temp file
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)
    
    # extract tar.bz2 file to temp dir
    with tarfile.open(file_name, "r:bz2") as tar_file:
        tar_file.extractall(dest_dir)
    
    # check if ~/.card_shark dir exists and make it if not
    home = os.path.expanduser("~")
    if not os.path.exists('{0}/.card-trick'.format(home)):
        os.makedirs('{0}/.card-trick'.format(home))
    
    # copy aro.obo ontology file to directory
    shutil.copyfile('{0}/aro.obo'.format(dest_dir), '{0}/.card-trick/aro.obo'.format(home))
    

def parse_ontology(obo_file):
    """
    Parse aro.obo ontology from CARD
    Params:
        obo_file: File path to the aro.obo file
    Returns:
        antibiotics, genes: tuple of dictionaries.
                            antibiotics contains antibiotic names as keys, values are the genes that confer resistance to the antibiotic
                            genes: gene names as keys, values are the antibiotics linked to the genes
    """

    antibiotics = {}
    genes = {}

    o = pronto.Ontology(obo_file)
    # loop through all terms in the ontology
    for term_name in o.terms:
        term = o.terms[term_name]
        # get relationships for the term
        relations = term.relations
        for rel in relations:
            # if the relationship is 'confers_resistance_to_drug' populate genes dict
            if rel.obo_name == 'confers_resistance_to_drug':
                # make an entry in genes for the ontology term
                genes[term.name] = {}
                # find all parent terms for the term and add as a list
                genes[term.name]['parents'] = [t.name for t in term.rparents()] 
                # populate the ARO id into the dict
                genes[term.name]['id'] = term.id
                genes[term.name]['antibiotics'] = []
                for relationship_entity in relations[rel]:
                    # add each antibiotic to the gene
                    antibiotic = relationship_entity.name
                    genes[term.name]['antibiotics'].append(antibiotic)
                    # either make a new entry in the antibiotics dict or add the gene to the current list
                    if antibiotic in antibiotics:
                        antibiotics[antibiotic]['genes'].append(term.name)
                    else:
                        antibiotics[antibiotic] = {}
                        antibiotics[antibiotic]['genes'] = [term.name]

    return antibiotics, genes

def write_ontology(antibiotics, genes, directory = '{0}/.card-trick'.format(os.path.expanduser("~"))):
    """
    write the antibiotics and genes dicts to json fikes in the ~/.card-trick directory
    """
    with open('{0}/antibiotics.json'.format(directory), 'w') as antibiotics_json:
        antibiotics_json.write(json.dumps(antibiotics))
    with open('{0}/genes.json'.format(directory), 'w') as genes_json:
        genes_json.write(json.dumps(genes))

def get_json_data(prefix):
    home = os.path.expanduser("~")
    if os.path.exists('{0}/.card-trick/{1}.json'.format(home, prefix)):
        data = open('{0}/.card-trick/{1}.json'.format(home, prefix)).read()
    else:
        data = pkgutil.get_data('card_trick', 'data/{0}.json'.format(prefix))
    return data

def search_dict(dict, search_term):
    """
    search dictionary for a term in the keys
    """
    found = {k:v for (k,v) in dict.items() if search_term.lower() in k.lower()}
    return found

def get_json_and_search(json_prefix, search_term):
    if len(search_term) < 3:
        sys.exit('Error: The search term must be at least 3 characters')
    data = get_json_data(json_prefix)
    dict = json.loads(data)
    return search_dict(dict, search_term)

def search_antibiotics(search_term):
    """
    search antibiotics dict for an antibiotic and report genes responsible for resistance to the antibiotic
    """
    return get_json_and_search('antibiotics', search_term)


def search_genes(search_term):
    """
    search genes dict for a gene and report antibiotics it confers resistance to
    """
    return get_json_and_search('genes', search_term)
