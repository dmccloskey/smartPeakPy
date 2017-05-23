# coding: utf-8
#modules
from .smartPeak import smartPeak
from .pyTOPP.MRMMapper import MRMMapper
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_openSWATH_py():
    def __init__(self):
        pass

    def calculateConcentrations(self):
        """Calculate the concentrations 

        Args

        Returns

        """
        pass

    def openSWATH_py(self,
        filenames_I,
        MRMFeatureFinderScoring_params_I={},
        ):
        """Run the openSWATH workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        # variables
        mzML_feature_i = filenames_I['mzML_feature_i']
        traML_csv_i = filenames_I['traML_csv_i']
        traML_i = filenames_I['traML_i']
        featureXML_o = filenames_I['featureXML_o']
        feature_csv_o = filenames_I['feature_csv_o']
        MRMFeatureFinderScoring_params = MRMFeatureFinderScoring_params_I

        # load chromatograms
        chromatograms = pyopenms.MSExperiment()
        fh = pyopenms.FileHandler()
        fh.loadExperiment(mzML_feature_i.encode('utf-8'), chromatograms)

        # # apply a filter
        # filter = pyopenms.SavitzkyGolayFilter()
        # filter.filterExperiment(chromatograms)
        # file = pyopenms.MzMLFile()
        # file.store('/home/user/openMS_MRMworkflow/QC1_p.mzML',chromatograms)

        # load and make the transition file
        targeted = pyopenms.TargetedExperiment()
        tramlfile = pyopenms.TransitionTSVReader()
        tramlfile.convertTSVToTargetedExperiment(traML_csv_i.encode('utf-8'),21,targeted)
        # #load transitions file
        # targeted = pyopenms.TargetedExperiment()
        # tramlfile = pyopenms.TraMLFile()
        # tramlfile.load(traML_i.encode('utf-8'), targeted)

        # map transitions to the chromatograms
        mrmmapper = MRMMapper()
        chromatograms_mapped = mrmmapper.algorithm(
            chromatogram_map=chromatograms,
            targeted=targeted, 
            precursor_tolerance=0.0005,
            product_tolerance=0.0005, 
            allow_unmapped=True,
            allow_double_mappings=True
        )

        #make the decoys
        #MRMDecoy
        #How are the decoys added into the experiment?

        # load in the DIA data
        empty_swath = pyopenms.MSExperiment()
        # extractor = pyopenms.ChromatogramExtractor()
        # extractor.extractChromatograms(MSExperiment[Peak1D, ChromatogramPeak] & input,
        #     MSExperiment[Peak1D, ChromatogramPeak] & output,
        #     TargetedExperiment & transition_exp,
        #     double extract_window,
        #     bool ppm,
        #     TransformationDescription trafo,
        #     double rt_extraction_window,
        #     String filter)
        #Does this work for any ms2 data?

        # normalize the RTs
        trafo = pyopenms.TransformationDescription()
        # model = trafo.getModelType()
        # parameters = trafo.getModelParameters()
        # #...
        # trafo.setParameters(parameters)
        # trafo.fitModel(String model_type, Param params)

        #MRMRTNormalizer
        #What is required to generate this?

        # Create empty output
        output = pyopenms.FeatureMap()
        
        # set up MRMFeatureFinderScoring (featurefinder) and
        # parse the MRMFeatureFinderScoring params
        # featurefinder = pyopenms.PeakPickerMRM()
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        parameters = self.updateParameters(
            parameters,
            MRMFeatureFinderScoring_params,
            )
        featurefinder.setParameters(parameters)

        
        # set up MRMFeatureFinderScoring (featurefinder) and 
        # run
        #TODO: need to break into individual functions to create the GUI
        #mapExperimentToTransitionList
        #MRMTransitionGroupPicker
        #OpenSwathScoring #scores added to features generated MRMTransitionGroupPicker
        #OpenSwath_Scores #Holds the scores computed by OpenSwathScoring
        # featurefinder.pickChromatograms(chromatograms, output)
        featurefinder.pickExperiment(chromatograms, output, targeted,
                                        trafo, empty_swath)

        # Store outfile as featureXML
        featurexml = pyopenms.FeatureXMLFile()
        featurexml.store(featureXML_o.encode('utf-8'), output)

        # Store the outfile as csv


        # write out for mProphet

    def updateParameters(self,Param_IO,parameters_I):
        """Update a Param object
        Args
            Param_IO (pyopenms.Param()): Param object to update
            parameters_I (list): list of parameters to update
            
        Output
            Param_IO (pyopenms.Param()): updated Param object
        
        """
        for param in parameters_I:
            name = param['name'].encode('utf-8');
            # #test:
            # if name == 'rt_extraction_window'.encode('utf-8'):
            #     print('check')
            #check if the param exists
            if not Param_IO.exists(name):
                print("parameter not found: " + name)
                continue;
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

    def isotopeLabeledQuantitation_py(self,
        filenames_I,):
        """Isotope labeled quantification workflow for a single sample
        
        Args
            filenames_I (list): list of filename strings
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
        
        Notes
            requires both heavy and light features in the same featureMap
        
        """

        # variables
        featureXML_i = filenames_I['featureXML_i']
        consensusXML_o = filenames_I['consensusXML_o']

        # load featureMap
        maps = pyopenms.FeatureMap();
        featurexml = pyopenms.FeatureXMLFile()
        featurexml.load(featureXML_i.encode('utf-8'), maps)

        # group the features
        output = pyopenms.ConsensusMap()
        # #some sort of configuration needs to be done?
        # ConsensusMap out;
        # out.getFileDescriptions()[0].filename = "data/Tutorial Labeled.featureXML";
        # out.getFileDescriptions()[0].size = maps[0].size();
        # out.getFileDescriptions()[0].label = "light";
        # out.getFileDescriptions()[1].filename = "data/Tutorial Labeled.featureXML";
        # out.getFileDescriptions()[1].size = maps[0].size();
        # out.getFileDescriptions()[1].label = "heavy";
        algorithm = pyopenms.FeatureGroupingAlgorithmLabeled()
        # set the parameters
        #params = pyopenms.Param()
        algorithm.group(maps,output)

        # store outfile
        consensus = pyopenms.ConsensusXMLFile();
        consensus_file.store(consensusXML_o.encode('utf-8'), output)