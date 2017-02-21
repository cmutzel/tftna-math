# -*- coding: utf-8 -*-
import networkx as nx

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from src.products.daily_logs import DailyLogs
from src.products.base_training_goals import BaseTrainingGoals
from src.products.weekly_activity_totals import WeeklyActivityTotals


PRODUCTS = {
        "weekly_activity_totals": WeeklyActivityTotals,
        "base_training_goals": BaseTrainingGoals,
        "daily_logs": DailyLogs
}

"""
    Playing around with NetworkX.  A bit overkill here, but want to see
    how lightweight it is. 
""" 
        

class DataProductFactory(object):
    def __init__(self):
        # discovery the classes/methods responsible for each data product
        self.products = PRODUCTS
    
    def get_product(self, name="", force_build=False):
        """
        Params:
            string name - Should match one of the keys in PRODUCTS
        
        Returns:
            value of the data product (usually a Pandas DataFrame)
        
        Post-condition:
            Data product @name exists in ./data/processed
            
        """
        logger.info("Making '{}'".format(name))
        
        try:
            # instantiate the class responsible for the data product we want
            klass = self.products[name]
        except KeyError:
            raise Exception("Failed while building data products. No class found to produce '{}'".format(name))    
        
        product = klass()
        for r in self.products[name].requires:
            # here we ensure the data dependencies are available to the class
            # instance being used to build *this* product (node)
            logger.debug("Setting value {} on {}".format(r, product))
            setattr(product, r, self.get_product(r, force_build))
        value = product.read(force_build)
        
                
        return value
    
    def make_all(self):
        """Post-condition: all data products exist within ./data/processed"""
        logger.info("Making all products")
        for name in self.products.iterkeys():
            self.get_product(name)
        
    def plot_make_dependencies(self):
        # a directed graph
        g = nx.DiGraph()
        for name, klass in self.products.iteritems():
            # add a node for each data product
            g.add_node(name)
            
            # and an edge between any dependencies between products
            #  might be able to do this will add_edge exclusively (remove calls
            #  to add_node) above...requires further testing...
            for requirement in klass.requires:
                g.add_edge(requirement, name)
        nx.draw_networkx(g)   
        
if __name__ == '__main__':
    factory = DataProductFactory()
    factory.make_all()
        