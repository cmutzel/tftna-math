# -*- coding: utf-8 -*-

# A Base class for data products

import os
from pickle import dump, load

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataProduct(object):
    def __init__(self, product_name):
        self.value = None
        self.product_name = product_name
    
    def store(self):
        """For now, we just pickle all our data products"""

        dir = os.path.dirname(__file__) 
        path = os.path.join(dir, '../../data/processed',
                self.product_name +  ".pickle")
        logger.info("Storing value for {} to {} ".format(
                self.product_name, path))
        fh = open(path, mode="w")
        dump(self.value, fh)

    def read(self, force_build=False):
        """Reads the data product if it exists, otherwise builds it"""

        if not force_build:
            try:
                logger.debug("Checking for stored value for {}".format(
                        self.product_name))
                dir = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(dir,
                        '../../data/processed',
                        self.product_name + ".pickle")
                fh = open(path, mode="r")
                self.value = load(fh)
                logger.debug("Found {}, using.".format(self.product_name))
                return self.value
            
            except IOError:
                logger.warning("Failed opening {}, will build {} from dependencies.".format(
                        path, self.product_name))

        self.value = self.build()                
        self.store()
    
        return self.value
    
    def build(self):
        raise NotImplemented()