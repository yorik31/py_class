# -*- coding: utf-8 -*-
# Source Generated with Decompyle++
# File: product_import_module.pyc (Python 2.7)

import os
import sys
from xml.dom import minidom
from os import listdir
import glob
import numpy as np
import glob
import imp
import shutil
import time
import re

class product_import_module:
    
    def __init__(self, product_path):
        self.product_path = os.path.abspath(product_path)
        self.home_dir = str(os.getcwd())

    
    def extract_metadata(self):
        rootDir = self.home_dir
        product = self.product_path
        print ' '
        print os.path.join(rootDir, 'wflow.xml')
        print ' '
        queryPath = '/'.join([
            os.environ['ppScript'],
            'productImport',
            'xq'])
        utilPath = '/'.join([
            os.environ['ppScript'],
            'productImport'])
        print ' In processing : ' + product
        print ' '
        print ' - Recherche du WorkFlow'
        print ' '
        xql_file_name = os.path.join(queryPath, 'selectQuerynameForAccess.xql')
        cmd = ' '.join([
            'sh queryLight.sh -f',
            xql_file_name,
            '-variable file',
            product,
            '>',
            os.path.join(rootDir, 'wflow.xml')])
        print cmd
        os.system(cmd)
        xml_file = os.path.join(rootDir, 'wflow.xml')
        xmldoc = minidom.parse(xml_file)
        queryName = xmldoc.getElementsByTagName('browseQueryName')[0].firstChild.data
        xql_file_name = '/'.join([
            queryPath,
            queryName])
        product_name = os.path.basename(product)
        out_file = os.path.join(rootDir, 'md.xml')
        print ' '
        print ' --- Execute Query : --- '
        print ' '
        element = xmldoc.getElementsByTagName('addhocScript')
        if element:
            addhocScriptName = xmldoc.getElementsByTagName('addhocScript')[0].firstChild.data
            print 'Execute addhoc Script in First - cas Landsat'
            #computeOrientationAngle = computeOrientationAngle
            from estimate_orientation_angle_LandsatScene import  computeOrientationAngle
            angle = computeOrientationAngle(product)
            cmd = ' '.join([
                'sh queryLight.sh -f',
                xql_file_name,
                '-variable file',
                product,
                '-variable angle',
                str(angle),
                '>',
                out_file])
            print cmd
            os.system(cmd)
            print '-- End of query Light'
            print ' '
        else:
            cmd = ' '.join([
                'sh queryLight.sh -f',
                xql_file_name,
                '-variable file',
                product,
                '>',
                out_file])
            print cmd
            os.system(cmd)
        print '-- Move md File'
        input_file = out_file
        product_name = product_name.replace('.TIFF', '')
        out_file = os.path.join(product, 'm_metadata.xml')
        print '-- Destination File : ' + out_file
        cmd = ' '.join([
            'mv',
            input_file,
            out_file])
        os.system(cmd)
        print '-- Remove Work Flow File : ' + xml_file
        cmd = ' '.join([
            'rm -f',
            xml_file])
        os.system(cmd)
        print ' '
        print '-- End '


