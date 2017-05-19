# # Imports
import os

class smartPeak():
    """Class for smartPeak python methods"""
    # # Definitions
    @staticmethod
    def make_osCmd(paramDict_I, functionName_I):
        """Make a general command line call string
        
        Args
            paramDict_I (list:dict): list of dictionaries of parameter names and values
            functionName_I (str): name of the command line function
            
        Returns
            cmd_O (str): os command string
        
        """
        cmd_O = functionName_I
        for d in paramDict_I:
            cmd_O += ''' %s%s%s''' % (d['param'], d['delim'], d['value'])

    #         for p,v in d.items():
    #             cmd_O += ''' %s %s'''%(p,v)
        return cmd_O

    @staticmethod
    def run_osCmd(cmd_I, verbose_I=False):
        """Run a general command line call string
        
        Args
            cmd_I (str): os command string
            
        
        """
        if verbose_I: print(cmd_I)
        os.system("%s" % (cmd_I))

    @staticmethod
    def convert_MQQMethod2Feature(MQQMethod_I):
        """Convert MultiQuant QMethod.csv file to feature.csv file
        
        Args
            MQQMethod_I (list:dict): list of dictionaries of headers/values
            
        Returns
            FeatureXML_O (list:dict): list of dictionaries of headers/values
        
        """
        FeatureXML_O = []
        #create header map:
        header_map = {
            'Group Name':'ProteinName',
            'Group Name':'transition_group_id',
            'Name':'transition_name',
            'Expected RT':'Tr_recalibrated',
            'Expected RT':'RetentionTime',
            'Q1 Mass - 1':'PrecursorMz',
            'Q3 Mass - 1':'ProductMz'
        }
        #create defaults:
        feature_defaults = {
            'FullPeptideName':'',
            'Annotation':'',
            'MS1 Res':'Unit',
            'MS2 Res':'Unit',
            'Dwell':'',
            'Fragmentor':'',
            'Collision Energy':'',
            'Cell Accelerator Voltage':'',
            'LibraryIntensity':'1',
            'decoy':'0',
            'PeptideSequence':'',
            'PrecursorCharge':'1',
            'FragmentCharge':'1',
            'FragmentType':''
        }
        for row in MQQMethod_I:
            tmp = {}
            for h1,h2 in header_map.items():
                tmp[h2]=row[h1]
            component_group_name,quantifier,label_type = self.parse_MQTransitionName(row['Name'])
            tmp['FragmentSeriesNumber']=quantifier
            tmp['LabelType']=label_type
            tmp.update(feature_defaults)
            FeatureXML_O.append(tmp)
        return FeatureXML_O

    @staticmethod
    def parse_MQTransitionName(name_I):
        """Parse MultiQuant transition name
        
        Args
            name_I (str): transition name
            
        Returns
            component_group_name_O (str): component_group_name
            quantifier_O (int): quantifier = 1, qualifier = 2
            label_type_O (str): Heavy or Light

        """
        name_lst = name_I.split('.')
        component_group_name_O = name_lst[0]
        quantifier_O = int(name_lst[1].split('_')[1])
        label_type_O = name_lst[2]

        return component_group_name_O,quantifier_O,label_type_O
