# -*- coding: utf-8 -*-
from __future__ import print_function, division

# Description: class NeuroML for loading NeuroML from single file into MOOSE
# Version 1.0 by Aditya Gilra, NCBS, Bangalore, India, 2011 for serial MOOSE
# Version 1.5 by Niraj Dudani, NCBS, Bangalore, India, 2012, ported to parallel MOOSE
# Version 1.6 by Aditya Gilra, NCBS, Bangalore, India, 2012, further changes for parallel MOOSE
# Maintainer: Dilawar Singh, dilawars@ncbs.res.in 
#  - python3 related fixes.

"""
NeuroML.py is the preferred interface to read NeuroML files.

Instantiate NeuroML class, and thence use method:

readNeuroMLFromFile(...) to load NeuroML from a file:

(a) the file could contain all required levels 1, 2 and 3 - Morph, Channel and Network;

OR

(b) the file could have only L3 (network) with L2 (channels/synapses) and L1
(cells) spread over multiple files;
 these multiple files should be in the same or lower-level directory
 named as <chan/syn_name>.xml or <cell_name>.xml or <cell_name>.morph.xml
 (essentially as generated by neuroConstruct's export).

OR

(c) the file could contain only L2 (MorphML) or only L1 (ChannelML),
 in which case the loader reads them into /library or at the path passed in.

OR

(d) your lower level L1 and L2 xml files could be scattered in non-hierarchical directories,
 then you can use this reader to load the ChannelML files individually into /library,
 then this reader to load MorphML files into /library.
 Store the cellDict returned for each cell, and combine them into a larger cellsDict as below,
 and finally call this reader on the NetworkML file passing the cellsDict.
 [OR you can use the separate Channel, Morph and NetworkML loaders in moose.neuroml.<...>
 to load each level files individually i.e. first load ChannelML files into /library,
 then cells from MorphML and, finally the NetworkML.]

For testing, you can also call this from the command line with a neuroML file as argument.
However, the new relative import .ChannelML breaks calling it from commandline,
 so have to do it on python / ipython terminal:
In [1]: import moose
In [2]: import moose.neuroml
In [3]: moose.neuroml.loadNeuroML_L123('Generated.net.xml')
"""

import moose
import moose.utils as mu
from xml.etree import cElementTree as ET
from moose.neuroml.ChannelML import ChannelML
from moose.neuroml.MorphML import MorphML
from moose.neuroml.NetworkML import NetworkML

from moose.neuroml.utils import *

import sys
from os import path

class NeuroML():

    def __init__(self):
        pass

    def readNeuroMLFromFile(self, filename, params={}, cellsDict={}):
        """
        For the format of params required to tweak what cells are loaded,
         refer to the doc string of NetworkML.readNetworkMLFromFile().
        Returns (populationDict,projectionDict),
         see doc string of NetworkML.readNetworkML() for details.
        """
        mu.info("Loading neuroml file %s " % filename)
        moose.Neutral('/library') # creates /library in MOOSE tree; elif present, wraps
        tree = ET.parse(filename)
        root_element = tree.getroot()

        # if model_path is given in params, use it else use the directory of NML
        # as model_dir.
        self.model_dir = params.get('model_dir', path.dirname(path.abspath(filename)))

        if 'lengthUnits' in list(root_element.attrib.keys()):
            self.lengthUnits = root_element.attrib['lengthUnits']
        else:
            self.lengthUnits = 'micrometer'

        ## lots of gymnastics to check if temperature meta tag is present
        self.temperature = CELSIUS_default # gets replaced below if tag for temperature is present
        self.temperature_default = True
        for meta_property in root_element.findall('.//{'+meta_ns+'}property'):
            ## tag can be an attrib or an element
            if 'tag' in list(meta_property.attrib.keys()): # tag is an attrib
                tagname = meta_property.attrib['tag']
                if 'temperature' in tagname:
                    self.temperature = float(meta_property.attrib['value'])
                    self.temperature_default = False
            else: # tag is a separate element
                tag = meta_property.find('.//{'+meta_ns+'}tag')
                tagname = tag.text
                if 'temperature' in tagname:
                    ## value can be a tag or an element
                    if 'value' in list(tag.attrib.keys()): # value is an attrib
                        self.temperature = float(tag.attrib['value'])
                        self.temperature_default = False
                    else: # value is a separate element
                        self.temperature = float(tag.find('.//{'+meta_ns+'}value').text)
                        self.temperature_default = False
        if self.temperature_default:
            mu.info("Using default temperature of %s degree Celsius" % self.temperature)
        self.nml_params = {
                'temperature':self.temperature,
                'model_dir':self.model_dir,
        }


        mu.debug("Loading channels and synapses into MOOSE /library ...")
        cmlR = ChannelML(self.nml_params)
        for channels in root_element.findall('.//{'+neuroml_ns+'}channels'):
            self.channelUnits = channels.attrib['units']
            for channel in channels.findall('.//{'+cml_ns+'}channel_type'):
                ## ideally I should read in extra params
                ## from within the channel_type element and put those in also.
                ## Global params should override local ones.
                cmlR.readChannelML(channel,params=params,units=self.channelUnits)
            for synapse in channels.findall('.//{'+cml_ns+'}synapse_type'):
                cmlR.readSynapseML(synapse,units=self.channelUnits)
            for ionConc in channels.findall('.//{'+cml_ns+'}ion_concentration'):
                cmlR.readIonConcML(ionConc,units=self.channelUnits)

        mu.debug("Loading cell definitions into MOOSE /library ...")
        mmlR = MorphML(self.nml_params)
        self.cellsDict = cellsDict
        for cells in root_element.findall('.//{'+neuroml_ns+'}cells'):
            for cell in cells.findall('.//{'+neuroml_ns+'}cell'):
                cellDict = mmlR.readMorphML(cell,params=params,lengthUnits=self.lengthUnits)
                self.cellsDict.update(cellDict)

        ## check if there are populations in this NML files,
        ## if not, it's a MorphML or ChannelML file, not NetworkML, so skip.
        if root_element.find('.//{'+neuroml_ns+'}populations') is None \
            and root_element.find('.//{'+nml_ns+'}populations') is None:
            return (self.cellsDict,'no populations (L3 NetworkML) found.')
        else:
            mu.debug("Loading individual cells into MOOSE root ... ")
            nmlR = NetworkML(self.nml_params)
            return nmlR.readNetworkML(root_element,self.cellsDict,\
                    params=params,lengthUnits=self.lengthUnits)
        ## cellsDict = { cellname: (segDict, cableDict), ... } # multiple cells
        ## where segDict = { segid1 : [ segname,(proximalx,proximaly,proximalz),
        ##     (distalx,distaly,distalz),diameter,length,[potential_syn1, ... ] ] , ... }
        ## segname is "<name>_<segid>" because 1) guarantees uniqueness,
        ##     & 2) later scripts obtain segid from the compartment's name!
        ## and cableDict = { cablegroupname : [campartment1name, compartment2name, ... ], ... }
        self.cellsDict = nmlR.cellSegmentDict

def loadNeuroML_L123(filename):
    neuromlR = NeuroML()
    return neuromlR.readNeuroMLFromFile(filename)

if __name__ == "__main__":
    if len(sys.argv)<2:
        mu.error("You need to specify the neuroml filename.")
        sys.exit(1)
    print(loadNeuroML_L123(sys.argv[1]))
