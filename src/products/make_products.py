# -*- coding: utf-8 -*-
import os
#import click
#from dotenv import find_dotenv, load_dotenv
import networkx as nx

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from src.products.daily_logs import DailyLogs
from src.products.weekly_activity_totals import WeeklyActivityTotals

PRODUCTS = {"weekly_activity_totals": WeeklyActivityTotals, "daily_logs": DailyLogs}

"""
    Playing around with NetworkX.  A bit overkill here, but want to see
    how lightweight it is. 
"""

def construct_graph():
    # a directed graph
    g = nx.DiGraph()
    for k, v in PRODUCTS.iteritems():
        # add a node for each data product
        
        # and an edge between any dependencies between products
        g.add_node(k)
        for requirement in v.requires:
            g.add_edge(requirement, k)
        
    return g
        
def plot_graph(g):
    nx.draw_networkx(g)


#@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
def main(project_dir):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Making data products from raw data')
    
    g = construct_graph()

    try:
        nodes = nx.topological_sort(g)
    except nx.NetworkXUnfeasible:
        logger.error("Could not establish build order for data products. Check product dependencies")
        
    for name in nodes:
        klass_inst = PRODUCTS[name]()
        for r in PRODUCTS[name].requires:
            logger.info("Setting value {} on {}".format(r, klass_inst))
            setattr(klass_inst, r, PRODUCTS[r]().read())
        klass_inst.read() 
        

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    #load_dotenv(find_dotenv())

    #plot_graph(construct_graph())
    main(project_dir)
