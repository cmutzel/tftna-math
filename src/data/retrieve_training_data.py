#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
retrieve_training_logs.py

Created on Tue Feb  7 18:56:58 2017

@author: chrismutzel
"""
from os import listdir
from shutil import copy

def retrieve_logs():
    #copy to dir
    copy_logs()
    
def copy_logs():
    """Right now, all we do to get a hold of the training logs is copy 
    them from another local directory"""
    src_dir = "/Users/chrismutzel/Dropbox/climbing/training logs"
    target_dir = "/Users/chrismutzel/projects/tftna-math/data/raw"
    
    for f in listdir(src_dir):
        if "Chris - Training" in f or "Chris - Climb" in f:
            copy("{}/{}".format(src_dir, f), target_dir)
    
if __name__ == "__main__":
    copy_logs()
