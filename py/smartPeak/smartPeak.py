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
    def convert_byte2String(byte_I, encoding_I='utf-8'):
        """Convert a byte to a string
        
        Args
            byte_I (byte): byte representation of a string
            encoding_I (str): byte encoding, default = 'utf-8'

        Returns
            string_O (str):            
        
        """
        string_O = None
        if type(byte_I)==type(''.encode(encoding_I)): 
            string_O = byte_I.decode(encoding_I)
        else:
            print("input is not of type byte.")
        return string_O

    @staticmethod
    def convert_string2Byte(string_I, encoding_I='utf-8'):
        """Convert a string to a byte
        
        Args
            string_I (str): 
            encoding_I (str): byte encoding, default = 'utf-8'

        Returns
            byte_O (byte): byte representation of a string            
        
        """
        byte_O = None
        if type(string_I)==type(''): 
            byte_O = string_I.encode(encoding_I)
        else:
            print("input is not of type str.")
        return byte_O

    def convert_MQQMethod2Feature(self,MQQMethod_I):
        """Convert MultiQuant QMethod.csv file to feature.csv file
        
        Args
            MQQMethod_I (list:dict): list of dictionaries of headers/values
            
        Returns
            FeatureXML_O (list:dict): list of dictionaries of headers/values
        
        """
        FeatureXML_O = []
        #create header map:
        header_map = {
            'ProteinName':'Group Name',
            'transition_group_id':'Group Name',
            'transition_name':'Name',
            'Tr_recalibrated':'Expected RT',
            'RetentionTime':'Expected RT',
            'PrecursorMz':'Q1 Mass - 1',
            'ProductMz':'Q3 Mass - 1'
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
                tmp[h1]=row[h2]
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
        quantifier_O = int(name_lst[1].split('_')[-1])
        label_type_O = name_lst[2]

        return component_group_name_O,quantifier_O,label_type_O

    def updateParameters(self,Param_IO,parameters_I):
        """Update a Param object
        Args
            Param_IO (pyopenms.Param()): Param object to update
            parameters_I (list): list of parameters to update
            
        Output
            Param_IO (pyopenms.Param()): updated Param object
        
        """
        for param in parameters_I:
            name = param['name'].encode('utf-8')
            # #test:
            # if name == 'rt_extraction_window'.encode('utf-8'):
            #     print('check')
            #check if the param exists
            if not Param_IO.exists(name):
                print("parameter not found: " + param['name'])
                continue
            #check supplied user parameters
            if 'value' in param.keys() and param['value']:
                if 'type' in param.keys() and param['type']:
                    value = self.castString(param['value'],param['type'])
                else:
                    value = self.parseString(param['value'])
                # if not self.checkParameterValue(value):
                #     continue;
            else:
                value = Param_IO.getValue(name)
            if 'description' in param.keys() and param['description']:
                description = param['description'].encode('utf-8')
            else:
                description = Param_IO.getDescription(name)
            if 'tags' in param.keys() and param['tags']:
                tags = param['tags'].encode('utf-8')
            else:
                tags = Param_IO.getTags(name)
            #update the params
            Param_IO.setValue(name,
                value,
                description,
                tags)
        return Param_IO

    def setParameters(self,parameters_I,Param_O):
        """set a Param object
        Args
            parameters_I (list): list of parameters to update
            
        Output
            Param_O (pyopenms.Param()): Param object
        
        """
        for param in parameters_I:
            name = param['name'].encode('utf-8')
            #check if the param exists
            if not Param_IO.exists(name):
                print("parameter not found: " + param['name'])
                continue
            #check supplied user parameters
            if 'value' in param.keys() and param['value']:
                if 'type' in param.keys() and param['type']:
                    value = self.castString(param['value'], param['type'])
                else:
                    value = self.parseString(param['value'])
            else:
                value = ''.encode('utf-8')
            if 'description' in param.keys() and param['description']:
                description = param['description'].encode('utf-8')
            else:
                description = ''.encode('utf-8')
            if 'tags' in param.keys() and param['tags']:
                tags = param['tags'].encode('utf-8')
            else:
                tags = ''.encode('utf-8')
            #update the params
            Param_O.setValue(name,
                value,
                description,
                tags)
        return Param_O

    @staticmethod
    def checkParameterValue(value_I):
        """Check for a valid openMS parameter
        
        Args
            value_I (): input value_I

        Returns
            valid_O (bool): true, if valid input
                            false, if invalid input
        """    
        valid_O = True;
        if value_I == -1:
            valid_O = False;
        return valid_O;

    @staticmethod
    def castString(str_I,type_I):
        """Cast a string to the desired type 
        and return the eval
        
        Args
            str_I (str): input string
            type_I (str): type

        Returns
            str_O (): evaluated string

        Tests: todo...
            assert(parseString('1')==1)
            assert(parseString('-1')==-1)
            assert(parseString('1.0')==1.0)
            assert(parseString('0.005')==0.005)
            assert(parseString('-1.0')==-1.0)
            assert(parseString('[1]')==[1])
            assert(parseString('(1)')==(1))
            assert(parseString('{1}')=={1})
            assert(parseString('a')==a.encode('utf-8'))
            
        """
        str_O = None;
        try:
            if type_I == 'int':
                str_O = int(str_I)
            elif type_I == 'float':
                str_O = float(str_I)
            elif type_I == 'string' and str_I == 'TRUE':
                str_O = 'true'.encode('utf-8')
            elif type_I == 'string' and str_I == 'FALSE':
                str_O = 'false'.encode('utf-8')
            elif type_I == 'string':
                str_O = str_I.encode('utf-8')
            else:
                print(type_I+ ' type not supported')
                str_O = str_I.encode('utf-8')
        except Exception as e:
            print(e);
        return str_O;

    @staticmethod
    def parseString(str_I):
        """Parse string and return the eval
        
        Args
            str_I (str): input string
            
        Returns
            str_O (): evaluated string

        Tests:
            assert(parseString('1')==1)
            assert(parseString('-1')==-1)
            assert(parseString('1.0')==1.0)
            assert(parseString('0.005')==0.005)
            assert(parseString('-1.0')==-1.0)
            assert(parseString('[1]')==[1])
            assert(parseString('(1)')==(1))
            assert(parseString('{1}')=={1})
            assert(parseString('a')==a.encode('utf-8'))
            
        """
        def isfloat(str_i):
            isfloat_o = True;
            try:
                float(str_i)
            except Exception:
            # except ValueError:
                isfloat_o = False;
            return isfloat_o;

        str_O = None;
        try:
            if str_I.isdigit():
                str_O = int(str_I)
            elif str_I[0]=='-' and str_I[1:].isdigit():
                str_O = int(str_I)
            elif isfloat(str_I):
                str_O = float(str_I)
            # elif str_I.isdecimal():
            #     str_O = float(str_I)
            # elif str_I[0]=='-' and str_I[1:].isdecimal():
            #     str_O = float(str_I)
            elif str_I[0]=='[' and str_I[-1]==']':
                str_O = list(str_I[1:-1])
            elif str_I[0]=='{' and str_I[-1]=='}':
                str_O = dict(str_I[1:-1])
            elif str_I[0]=='(' and str_I[-1]==')':
                str_O = tuple(str_I[1:-1])
            else:
                str_O = str_I.encode('utf-8');
        except Exception as e:
            print(e);
        return str_O;
