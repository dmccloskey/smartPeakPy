# -*- coding: utf-8 -*-
import pytest
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from smartPeak.core.smartPeak_o import smartPeak_o
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class testSmartPeak():
    """tests for fastPeak"""

    #tests for smartPeak_openSWATH_cmd
    def test_make_osCmd(self, verbose_I=False):
        """Test make_osCmd function

        """

        params = [
            {
                'param': 'param1',
                'delim': ' ',
                'value': 'value1'
            },
            {
                'param': 'param2',
                'delim': ' ',
                'value': 'value2'
            },
        ]
        function = 'test'
        ans = 'test param1 value1 param2 value2'
        test = smartPeak.make_osCmd(params, function)
        if verbose_I: print(test)
        assert (test == ans)

    def test_convert_byte2String(self, verbose_I=False):
        """Test convert_byte2String function
        """
        str_test = 'a'.encode('utf-8')
        assert(smartPeak.convert_byte2String(str_test, encoding_I='utf-8')=='a')


    def test_convert_string2Byte(self, verbose_I=False):
        """Test convert_string2Byte function
        """
        str_test = 'a'.encode('utf-8')
        assert(smartPeak.convert_string2Byte('a', encoding_I='utf-8')==str_test)

    def test_convert_MQQMethod2Feature(self,verbose_I=False):
        """Test convert_MQQMethod2Feature function
        """
        
        filename_I='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_qmethod.csv'
        filename_O='/home/user/openMS_MRMworkflow/BloodProject01/BloodProject01_SWATH_feature.csv'       
        self.convert_MQQMethod2Feature(filename_I,filename_O) 

        #TODO: re-read in resulting file and compare to test file

    def convert_MQQMethod2Feature(self,filename_I,filename_O):
        """Convert MultiQuant QMethod file to feature.csv file
        
        """
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_csv(filename_I,delimiter=',')
        MQQMethod = smartpeak_i.getData()
        smartpeak_i.clear_data()

        smartpeak = smartPeak()
        features = smartpeak.convert_MQQMethod2Feature(MQQMethod)
        headers = ['ProteinName',
            'FullPeptideName',
            'transition_group_id',
            'transition_name',
            'Tr_recalibrated',
            'Annotation',
            'RetentionTime',
            'PrecursorMz',
            'MS1 Res',
            'ProductMz',
            'MS2 Res',
            'Dwell',
            'Fragmentor',
            'Collision Energy',
            'Cell Accelerator Voltage',
            'LibraryIntensity',
            'decoy',
            'PeptideSequence',
            'LabelType',
            'PrecursorCharge',
            'FragmentCharge',
            'FragmentType',
            'FragmentSeriesNumber'
        ]
        smartpeak_o = smartPeak_o(features)
        smartpeak_o.write_dict2csv(filename_O,headers=headers)

    def test_parse_MQTransitionName(self,verbose_I=False):
        """Test parse_MQTransitionName function
        """
        heavy = 'atp.atp_1.Heavy'
        light = 'atp.atp_2.Light'
        component_group_name,quantifier,label_type = smartPeak.parse_MQTransitionName(heavy)
        assert(component_group_name=='atp')
        assert(quantifier==1)
        assert(label_type=='Heavy')
        component_group_name,quantifier,label_type = smartPeak.parse_MQTransitionName(light)
        assert(component_group_name=='atp')
        assert(quantifier==2)
        assert(label_type=='Light')    

    def test_parseString(self, verbose_I=False):
        """Test parseString function
        
        """
        assert(smartPeak.parseString('1')==1)
        assert(smartPeak.parseString('-1')==-1)
        assert(smartPeak.parseString('1.0')==1.0)
        assert(smartPeak.parseString('0.005')==0.005)
        assert(smartPeak.parseString('-1.0')==-1.0)
        assert(smartPeak.parseString('[1]')==list('1'))
        assert(smartPeak.parseString('(1)')==tuple('1'))
        assert(smartPeak.parseString('{1}')==dict('1'))
        assert(smartPeak.parseString('a')=='a'.encode('utf-8'))
        assert(smartPeak.parseString('a',encode_str_I = False)=='a')
        assert(smartPeak.parseString("'a'")=='a'.encode('utf-8'))
        assert(smartPeak.parseString("['a','b','c']",encode_str_I = False)==['a','b','c'])
        assert(smartPeak.parseString("[1.0,2.0,3.0]")==[1.0,2.0,3.0])

    def test_castString(self, verbose_I=False):
        """Test castString function
        """
        assert(smartPeak.castString('1','int')==1)
        assert(smartPeak.castString('1.0','float')==1.0)
        assert(smartPeak.castString('TRUE','string')==True)
        assert(smartPeak.castString('FALSE','string')==True)
        assert(smartPeak.castString('a','string')=='a'.encode('utf-8'))
   
    def test_updateParameters(self, verbose_I=False):
        """Test updateParameters function

        TODO: 
        1. make a test "update_parameters.csv"
        2. read in "update_parameters"
        """
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        ff_parameters = featurefinder.getParameters()
        update_parameters = [] #read from file...
        ff_parameters = smartpeak.updateParameters(
            ff_parameters,
            test_parameters,
            )
        featurefinder.setParameters(ff_parameters)
        test_parameters = featurefinder.getParameters()
        assert(test_parameters==ff_parameters)

    def test_setParameters(self, verbose_I=False):
        """Test setParameters function

        TODO: 
        1. make a test "update_parameters.csv"
        2. read in "update_parameters"
        """
        pass

    def compareValues(self, verbose_I=False):
        """Test castString function
        """
        assert(smartPeak.compareValues(1,2,'<')==True)
        assert(smartPeak.compareValues(1,2,'>')==False)
        assert(smartPeak.compareValues(-1,2,'<abs')==True)
        assert(smartPeak.compareValues(-3,2,'>abs')==True)