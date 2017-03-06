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
