import os, sys
import card_trick
import json
import pkgutil

def update():
    """
    execute the update command that updates the CARD database
    """
    card_trick.ontology_functions.update_ontology()
    home = os.path.expanduser("~")
    antibiotics, genes = card_trick.ontology_functions.parse_ontology('{0}/.card-trick/aro.obo'.format(home))
    card_trick.ontology_functions.write_ontology(antibiotics, genes)

def search(options):
    """
    execute the search command, to search the ontology
    """
    if options.gene_name:
        # search for antibiotic resistances conferred by the specified gene
        matching_genes = card_trick.ontology_functions.search_genes(options.gene_name)
        if options.output_format == 'tsv':
            print('gene\tantibiotics')
            for gene in matching_genes:
                print('{0}\t{1}'.format(gene, ','.join(sorted(matching_genes[gene]['antibiotics']))))
        elif options.output_format == 'json':
            print(json.dumps(matching_genes, indent=2, sort_keys=True))

    elif options.antibiotic_name:
        # search for genes that confer resistance to the specified antibiotic
        matching_antibiotics = card_trick.ontology_functions.search_antibiotics(options.antibiotic_name)
        if options.output_format == 'tsv':
            print('antibiotic\tgenes')
            for antibiotic in matching_antibiotics:
                print('{0}\t{1}'.format(antibiotic, ','.join(sorted(matching_antibiotics[antibiotic]['genes']))))
        elif options.output_format == 'json':
            print(json.dumps(matching_antibiotics, indent=2, sort_keys=True))