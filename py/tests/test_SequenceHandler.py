# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from . import data_dir
from smartPeak.pyTOPP.SequenceHandler import SequenceHandler
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestSequenceHandler():
    
    def load_data(self,
        featureXML_i = "features/150601_0_BloodProject01_PLT_QC_Broth-1_1.featureXML",
        traML_csv_i = "BloodProject01_SWATH.csv",
        filename_params = "BloodProject01_MRMFeatureFinderScoring_params.csv"):
        """load the test data"""                   

        # load targeted experiment
        traML_csv_i = data_dir + "/" + traML_csv_i
        self.targeted = pyopenms.TargetedExperiment() #must use "PeptideSequence"
        if not traML_csv_i is None:
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,self.targeted)

        # load the featureMap
        featureXML_i = data_dir + "/" + featureXML_i     
        featurexml = pyopenms.FeatureXMLFile()
        self.featureMap = pyopenms.FeatureMap()
        if not featureXML_i is None:
            featurexml.load(featureXML_i.encode('utf-8'), self.featureMap)
        
        # load the parameters
        filename_params = data_dir + "/" + filename_params
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_openMSParams(filename_params,",")
        self.params = smartpeak_i.getData()
        smartpeak_i.clear_data()

    def test_addSampleToSequence(self):
        seqhandler = SequenceHandler()

        # test data
        meta_data1 = {'filename':'file1','sample_name':'sample1'}
        featuremap1 = None
        
        meta_data2 = {'filename':'file2','sample_name':'sample2'}
        featuremap2 = None
        
        meta_data3 = {'filename':'file3','sample_name':'sample3'}
        featuremap3 = None

        # add the injections to the sequence
        seqhandler.addSampleToSequence(meta_data1, featuremap1)
        seqhandler.addSampleToSequence(meta_data2, featuremap2)
        seqhandler.addSampleToSequence(meta_data3, featuremap3)

        assert(len(seqhandler.sequence) == 3)
        assert(seqhandler.sequence_index[1] == 'sample2')

    def test_getMetaValue(self):
        self.load_data()    
        seqhandler = SequenceHandler()

        feature, subordinate = None, None
        result = seqhandler.getMetaValue(feature, subordinate, "RT")
        assert(result == 10.0) #TODO
        result = seqhandler.getMetaValue(feature, subordinate, "calculated_concentration")
        assert(result == 10.0) #TODO

    def test_makeDataMatrixFromMetaValue(self):  
        seqhandler = SequenceHandler()

        # load the data
        filename_filenames = data_dir + "/" + '/home/user/openMS_MRMworkflow/Unknowns/filenames.csv',
        filename_params = data_dir + "/" + '/home/user/openMS_MRMworkflow/Unknowns/MRMFeatureFinderScoring_params.csv',
        delimiter = ','
        from smartPeak.core.smartPeak_openSWATH_py import smartPeak_openSWATH_py
        from smartPeak.core.smartPeak_AbsoluteQuantitation_py import smartPeak_AbsoluteQuantitation_py
        AbsoluteQuantitation_py = smartPeak_AbsoluteQuantitation_py()
        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for sample,v in filenames.items():
            print("processing sample "+ sample)
            try:
                ## pick peaks with OpenSWATH
                # dynamically make the filenames
                data_dir = v['data_dir']
                mzML_i = '''%s/mzML/%s.mzML'''%(data_dir,sample)
                traML_csv_i = '''%s/traML.csv'''%(data_dir)
                trafo_csv_i = '''%s/trafo.csv'''%(data_dir)
                # load in the files
                openSWATH_py.load_TraML({'traML_csv_i':traML_csv_i})
                openSWATH_py.load_SWATHorDIA({})
                openSWATH_py.load_MSExperiment({'mzML_feature_i':mzML_i})
                openSWATH_py.extract_metaData()
                openSWATH_py.meta_data['sample_type'] = 'Unknown'
                openSWATH_py.load_Trafo( #skip transformation of RT
                    {},#{'trafo_csv_i':trafo_csv_i},
                    params['MRMFeatureFinderScoring'])
                # dynamically make the filenames
                featureXML_o = '''%s/quantitation/%s.featureXML'''%(data_dir,sample) 
                feature_csv_o = '''%s/quantitation/%s.csv'''%(data_dir,sample)
                openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})

                # record features
                seqhandler.addSampleToSequence(openSWATH_py.meta_data,openSWATH_py.featureMap)
            except Exception as e:
                print(e)
                skipped_samples.append({'sample_name':sample,
                    'error_message':e})
            # manual clear data for the next iteration
            openSWATH_py.clear_data()

        # Test:
        columns, rows, data = seqhandler.makeDataMatrixFromMetaValue(
            meta_values = ["calculated_concentration"], sample_types = ["Unknown"])
        
        assert(len(columns) == 6)
        assert(columns[0] == '170808_Jonathan_yeast_Sacc1_1x')
        assert(rows[0] == ('accoa', 'accoa.accoa_1.Light'))
        assert(rows[0,0] == 1.2483242974681299)
        assert(data[len(rows)-1,len(columns)-1] == 1.57260671576702)
        