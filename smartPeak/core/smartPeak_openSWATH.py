# -*- coding: utf-8 -*-
# modules
from smartPeak.io.smartPeak import smartPeak
from smartPeak.io.smartPeak_i import smartPeak_i
from smartPeak.io.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
from smartPeak.pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from smartPeak.pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
from smartPeak.algorithm.MRMFeatureSelector import MRMFeatureSelector
from smartPeak.algorithm.MRMFeatureValidator import MRMFeatureValidator
from smartPeak.ui.FeaturePlotter import FeaturePlotter
from smartPeak.data.ReferenceDataMethods import ReferenceDataMethods
# external
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class smartPeak_openSWATH():
    def __init__(self):
        self.featureMap = None
        self.chromatogram_map = None
        self.targeted = None
        self.trafo = None
        self.msExperiment = None
        self.validation_metrics = None
        self.swath = None
        self.reference_data = None
        self.meta_data = None

    def clear_data(self):
        """Remove all data"""        
        self.featureMap = None
        self.chromatogram_map = None
        self.targeted = None
        self.trafo = None
        self.msExperiment = None
        self.validation_metrics = None
        self.swath = None
        self.reference_data = None
        self.meta_data = None

    def load_TraML(self, filenames_I, verbose_I=False):
        """Load TraML file

        Args:
            filenames_I (list): list of filename strings

        Internals:
            targeted (TargetedExperiment)

        """
        if verbose_I:
            print("Loading TraML")

        traML_csv_i, traML_i = None, None
        if 'traML_csv_i'in filenames_I.keys():
            traML_csv_i = filenames_I['traML_csv_i']
        if 'traML_i'in filenames_I.keys():
            traML_i = filenames_I['traML_i']

        # load and make the transition file
        targeted = pyopenms.TargetedExperiment()  # must use "PeptideSequence"
        if traML_csv_i is not None:
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(
                traML_csv_i.encode('utf-8'), 21, targeted)
        elif traML_i is not None:
            targeted = pyopenms.TargetedExperiment()
            tramlfile = pyopenms.TraMLFile()
            tramlfile.load(traML_i.encode('utf-8'), targeted)
        self.targeted = targeted

    def load_Trafo(
        self,
        filenames_I,
        MRMFeatureFinderScoring_params_I={},
        verbose_I=False
    ):
        """Load Trafo file

        Args:
            filenames_I (list): list of filename strings
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags

        Internals:
            targeted (TargetedExperiment)
        
        """
        if verbose_I:
            print("Loading Trafo")

        trafo_csv_i = None
        if 'trafo_csv_i'in filenames_I.keys(): 
            trafo_csv_i = filenames_I['trafo_csv_i']
        MRMFeatureFinderScoring_params = MRMFeatureFinderScoring_params_I
        
        # set up MRMFeatureFinderScoring (featurefinder) and
        # parse the MRMFeatureFinderScoring params
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        smartpeak = smartPeak()
        parameters = smartpeak.updateParameters(
            parameters,
            MRMFeatureFinderScoring_params,
            )
        featurefinder.setParameters(parameters)     

        # # prepare the model parameters for RTNormalization (interpolation)
        # model_params_list = [
        #   {'name':'interpolation_type','value': 'linear','type': 'string'},
        #     {'name':' extrapolation_type','value': 'two-point-linear','type': 'string'},
        # ]
        # model_params = pyopenms.Param()
        # model_params = smartpeak.setParameters(model_params_list,model_params)

        trafo = pyopenms.TransformationDescription()
        if trafo_csv_i is not None:
            # load and make the transition file for RTNormalization 
            targeted_rt_norm = pyopenms.TargetedExperiment()
            tramlfile = pyopenms.TransitionTSVReader()
            tramlfile.convertTSVToTargetedExperiment(
                trafo_csv_i.encode('utf-8'), 21, targeted_rt_norm
                )
            # Normalize the RTs
            # NOTE: same MRMFeatureFinderScoring params will be used to pickPeaks
            RTNormalizer = OpenSwathRTNormalizer()
            trafo = RTNormalizer.main(
                self.chromatogram_map,
                targeted_rt_norm,
                model_params=None,
                # model_params=model_params,
                model_type="linear",
                # model_type="interpolated",
                min_rsq=0.95,
                min_coverage=0.6,
                estimateBestPeptides=True,
                MRMFeatureFinderScoring_params=parameters
                )
        self.trafo = trafo

    def load_MSExperiment(
        self,
        filenames_I,
        MRMMapping_params_I={},
        chromatogramExtractor_params_I={},
        verbose_I=False
    ):
        """Load MzML into an MSExperiment

        Args:
            filenames_I (list): list of filename strings
            MRMMapping_params_I (list): 
                list of key:value parameters for OpenMS::MRMMapping
            chromatogramExtractor_params_I (list): 
                list of key:value parameters for OpenMS::ChromatogramExtractor

        Internals:
            msExperiment (TargetedExperiment)
        
        """
        if verbose_I:
            print("Loading mzML")

        mzML_feature_i = None
        if 'mzML_feature_i'in filenames_I.keys():
            mzML_feature_i = filenames_I['mzML_feature_i']      

        # load chromatograms
        chromatograms = pyopenms.MSExperiment()
        if mzML_feature_i is not None:
            fh = pyopenms.FileHandler()
            fh.loadExperiment(mzML_feature_i.encode('utf-8'), chromatograms)

        if chromatogramExtractor_params_I and \
            chromatogramExtractor_params_I is not None and \
            self.targeted is not None:
            # convert parameters
            smartpeak = smartPeak()
            chromatogramExtractor_params = {d['name']: smartpeak.castString(
                d['value'], 
                d['type']) for d in chromatogramExtractor_params_I}
            # chromatogramExtractor_params = {d['name']:smartpeak.parseString(d['value']) 
            #   for d in chromatogramExtractor_params_I}
            # exctract chromatograms
            chromatograms_copy = copy.copy(chromatograms)
            chromatograms.clear(True)
            if chromatogramExtractor_params['extract_precursors']:
                tr = self.targeted.getTransitions()
                for t in tr:
                    t.setProductMZ(t.getPrecursorMZ())
                self.targeted.setTransitions(tr)
            chromatogramExtractor = pyopenms.ChromatogramExtractor()
            chromatogramExtractor.extractChromatograms(
                chromatograms_copy,
                chromatograms, 
                self.targeted,
                chromatogramExtractor_params['extract_window'],
                chromatogramExtractor_params['ppm'],
                pyopenms.TransformationDescription(),
                chromatogramExtractor_params['rt_extraction_window'],
                chromatogramExtractor_params['filter'],
                )

        self.msExperiment = chromatograms

        # map transitions to the chromatograms
        if MRMMapping_params_I and \
            MRMMapping_params_I is not None and \
            self.targeted is not None:        
            # set up MRMMapping and
            # parse the MRMMapping params
            mrmmapper = pyopenms.MRMMapping()
            smartpeak = smartPeak()
            parameters = mrmmapper.getParameters()
            parameters = smartpeak.updateParameters(
                parameters,
                MRMMapping_params_I,
                )
            mrmmapper.setParameters(parameters)  
            chromatogram_map = pyopenms.MSExperiment()

            # mrmmapper = MRMMapper()
            # chromatogram_map = mrmmapper.algorithm(
            #     chromatogram_map=chromatograms,
            #     targeted=self.targeted, 
            #     precursor_tolerance=0.0009, #hard-coded for now
            #     product_tolerance=0.0009, #hard-coded for now
            #     allow_unmapped=True,
            #     allow_double_mappings=True
            # )

            mrmmapper.mapExperiment(chromatograms, self.targeted, chromatogram_map)
        self.chromatogram_map = chromatogram_map

    def load_SWATHorDIA(
        self,
        filenames_I,
        verbose_I=False
    ):
        """Load SWATH or DIA into an MSExperiment
        Args:
            filenames_I (list): list of filename strings
        Internals:
            msExperiment (TargetedExperiment)
        
        """
        if verbose_I:
            print("Loading SWATH/DIA files")

        dia_csv_i = None
        if 'dia_csv_i'in filenames_I.keys(): 
            dia_csv_i = filenames_I['dia_csv_i']

        # load in the DIA data
        swath = pyopenms.MSExperiment()
        if dia_csv_i is not None:
            chromatogramExtractor = OpenSwathChromatogramExtractor()
            # read in the DIA data files:
            # dia_files_i = ...(dia_csv_i)
            swath = chromatogramExtractor.main(
                infiles=[],
                targeted=self.targeted,
                extraction_window=0.05,
                min_upper_edge_dist=0.0,
                ppm=False,
                is_swath=False,
                rt_extraction_window=-1,
                extraction_function="tophat"
            )
        self.swath = swath

    def openSWATH(
        self,
        MRMFeatureFinderScoring_params_I={},
        verbose_I=False
    ):
        """Run the openSWATH workflow for a single sample
        
        Args:
            filenames_I (list): list of filename strings
            MRMFeatureFinderScoring_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
                
        """
        if verbose_I:
            print("Picking peaks using OpenSWATH")

        # helper classes
        smartpeak = smartPeak()

        # make the decoys
        # MRMDecoy
        # How are the decoys added into the experiment?

        # Create empty output
        output = pyopenms.FeatureMap()
        
        # set up MRMFeatureFinderScoring (featurefinder) and
        # parse the MRMFeatureFinderScoring params
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        parameters = featurefinder.getParameters()
        parameters = smartpeak.updateParameters(
            parameters,
            MRMFeatureFinderScoring_params_I,
            )
        featurefinder.setParameters(parameters)    
        
        # set up MRMFeatureFinderScoring (featurefinder) and 
        # run
        featurefinder.pickExperiment(
            self.chromatogram_map, 
            output, 
            self.targeted, 
            self.trafo,
            self.swath)
        
        self.featureMap = output

    def filterAndSelect_py(
        self,
        filenames_I,
        MRMFeatureFilter_filter_params_I={},
        MRMFeatureSelector_select_params_I={},
        MRMFeatureSelector_schedule_params_I={},
        verbose_I=False
    ):
        """Run the openSWATH post processing filtering workflow for a single sample
        
        Args:
            filenames_I (list): list of filename strings
            MRMFeatureFilter_filter_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
            MRMFeatureSelector_select_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags
            MRMFeatureSelector_schedule_params_I (dict): dictionary of parameter
                names, values, descriptions, and tags

        Internals:
            features (FeatureMap): output from SWATH workflow
            msExperiment (MSExperiment): 
            targeted (TargetedExperiment): 

        Returns:
            output_selected (FeatureMap): filtered and/or selected features
                
        """
        # variables
        calibrators_csv_i = None
        mrmfeatureqcs_csv_i = None
        if 'calibrators_csv_i'in filenames_I.keys():
            calibrators_csv_i = filenames_I['calibrators_csv_i']
        if 'mrmfeatureqcs_csv_i'in filenames_I.keys():
            mrmfeatureqcs_csv_i = filenames_I['mrmfeatureqcs_csv_i']

        # filter features
        if verbose_I:
            print("Filtering picked features")
        if MRMFeatureFilter_filter_params_I:   
            # set up MRMFeatureFilter and parse the MRMFeatureFilter params
            featureFilter = pyopenms.MRMFeatureFilter()
            parameters = featureFilter.getParameters()
            smartpeak = smartPeak()
            parameters = smartpeak.updateParameters(
                parameters,
                MRMFeatureFilter_filter_params_I,
                )
            featureFilter.setParameters(parameters) 

            # read in the parameters for the MRMFeatureQC
            featureQC = pyopenms.MRMFeatureQC()
            featureQCFile = pyopenms.MRMFeatureQCFile()
            featureQCFile.load(mrmfeatureqcs_csv_i.encode('utf-8'), featureQC)  

            output_filtered = copy.copy(self.featureMap)
            featureFilter.FilterFeatureMap(
                output_filtered,
                featureQC,
                self.targeted)
        else:
            output_filtered = self.featureMap

        # select features
        if verbose_I:
            print("Selecting picked features")
        featureSelector = MRMFeatureSelector()
        if calibrators_csv_i is not None:
            smartpeak_i = smartPeak_i()
            smartpeak_i.read_csv(calibrators_csv_i, delimiter=',')
            calibrators = smartpeak_i.getData()
            smartpeak_i.clear_data()
        else: 
            calibrators = []
        if MRMFeatureSelector_schedule_params_I:
            output_selected = featureSelector.schedule_MRMFeatures_qmip(
                features=output_filtered,
                tr_expected=calibrators,    
                targeted=self.targeted,
                schedule_criteria=MRMFeatureSelector_schedule_params_I,                
                score_weights=MRMFeatureSelector_select_params_I
            )
        elif MRMFeatureSelector_select_params_I:
            output_selected = featureSelector.select_MRMFeatures_score(
                output_filtered,
                MRMFeatureSelector_select_params_I)
            # output_selected = featureSelector.select_MRMFeatures_qmip(
            #     features = output_filtered,
            #     tr_expected = calibrators,    
            #     select_criteria = MRMFeatureSelector_select_params_I,     
            # )
        else:
            output_selected = output_filtered

        self.featureMap = output_selected

    def load_featureMap(
        self,
        filenames_I={},
        verbose_I=False
    ):
        """Load a FeatureMap
        
        Args:
            filenames_I (list): list of filename strings
            
        """        
        if verbose_I:
            print("Loading FeatureMap")

        # Handle the filenames
        featureXML_i = None
        if 'featureXML_i'in filenames_I.keys():
            featureXML_i = filenames_I['featureXML_i']        

        # Store outfile as featureXML    
        featurexml = pyopenms.FeatureXMLFile()
        output = pyopenms.FeatureMap()
        if featureXML_i is not None:
            featurexml.load(featureXML_i.encode('utf-8'), output)

        self.featureMap = output

    def extract_metaData(self, verbose_I=False):
        """Extracts metadata from the chromatogram
        """
        if verbose_I:
            print("Extracting metadata")

        # initialize output variables
        filename = ''
        samplename = ''
        instrument = ''
        software = ''

        # filename
        loaded_file_path = self.chromatogram_map.getLoadedFilePath()
        if loaded_file_path is not None:
            filename = loaded_file_path.decode('utf-8').replace('file://', '')
        # filename = '''%s/%s''' %(
        #     chromatograms_mapped.getSourceFiles()[0].getPathToFile().decode('utf-8').replace('file://',''),
        #     chromatograms_mapped.getSourceFiles()[0].getNameOfFile().decode('utf-8'))

        # sample name
        mzml_id = self.chromatogram_map.getMetaValue(b'mzml_id')
        if mzml_id is not None:
            samplename_list = mzml_id.decode('utf-8').split('-')
            samplename = '-'.join(samplename_list[1:])   

        # instrument
        instrument_name = self.chromatogram_map.getInstrument().getName()
        if instrument_name is not None:
            instrument = instrument_name.decode('utf-8')
            # software
            software_name = self.chromatogram_map.getInstrument().getSoftware().getName()
            if software_name is not None:
                software = software_name.decode('utf-8')

        self.meta_data = {
            "filename": filename,
            "sample_name": samplename,
            "instrument": instrument,
            "software": software
        }

    def store_featureMap(
        self,
        filenames_I={},
        verbose_I=False
    ):
        """Store FeatureMap as .xml and .csv
        
        Args:
            filenames_I (list): list of filename strings
        """
        if verbose_I:
            print("Storing FeatureMap")

        # Handle the filenames
        featureXML_o, feature_csv_o = None, None
        if 'featureXML_o'in filenames_I.keys():
            featureXML_o = filenames_I['featureXML_o']
        if 'feature_csv_o'in filenames_I.keys():
            feature_csv_o = filenames_I['feature_csv_o']

        # Store outfile as featureXML    
        featurexml = pyopenms.FeatureXMLFile()
        if featureXML_o is not None:
            featurexml.store(featureXML_o.encode('utf-8'), self.featureMap)
        
        # Store the outfile as csv     
        featurescsv = OpenSwathFeatureXMLToTSV()  
        if feature_csv_o is not None:
            featurescsv.store(
                feature_csv_o, self.featureMap, self.targeted,
                run_id=self.meta_data['sample_name'],
                filename=self.meta_data['filename']
                )

    def load_validationData(
        self,
        filenames_I,
        ReferenceDataMethods_params_I={},
        verbose_I=False
    ):
        """Load the validation data from file or from a database
        
        Args:
            filenames_I (dict): dictionary of filenames
            ReferenceDataMethods_params_I (dict): dictionary of DB query parameters
        
        """
        if verbose_I:
            print("Loading validation data")

        smartpeak = smartPeak()

        # Handle the filenames
        referenceData_csv_i, db_ini_i = None, None
        if 'referenceData_csv_i'in filenames_I.keys(): 
            referenceData_csv_i = filenames_I['referenceData_csv_i']
        if 'db_ini_i'in filenames_I.keys(): 
            db_ini_i = filenames_I['db_ini_i']

        # Parse the input parameters
        ReferenceDataMethods_dict = {d['name']: smartpeak.parseString(
            d['value'], encode_str_I=False) for d in ReferenceDataMethods_params_I}
        experiment_ids_I = [],
        sample_names_I = [],
        sample_types_I = [],
        acquisition_methods_I = [],
        quantitation_method_ids_I = [],
        component_names_I = [],
        component_group_names_I = [],
        where_clause_I = '',
        used__I = True,
        experiment_limit_I = 10000,
        mqresultstable_limit_I = 1000000,
        # settings_filename_I = 'settings.ini',
        # data_filename_O = ''
        if "experiment_ids_I" in ReferenceDataMethods_dict.keys():
            experiment_ids_I = ReferenceDataMethods_dict["experiment_ids_I"]
        if "sample_names_I" in ReferenceDataMethods_dict.keys():
            sample_names_I = ReferenceDataMethods_dict["sample_names_I"]
        if "sample_types_I" in ReferenceDataMethods_dict.keys():
            sample_types_I = ReferenceDataMethods_dict["sample_types_I"]
        if "acquisition_methods_I" in ReferenceDataMethods_dict.keys():
            acquisition_methods_I = ReferenceDataMethods_dict["acquisition_methods_I"]
        if "quantitation_method_ids_I" in ReferenceDataMethods_dict.keys():
            quantitation_method_ids_I = ReferenceDataMethods_dict[
                "quantitation_method_ids_I"]  
        if "component_names_I" in ReferenceDataMethods_dict.keys():
            component_names_I = ReferenceDataMethods_dict["component_names_I"]   
        if "component_group_names_I" in ReferenceDataMethods_dict.keys():
            component_group_names_I = ReferenceDataMethods_dict["component_group_names_I"]
        if "where_clause_I" in ReferenceDataMethods_dict.keys():
            where_clause_I = ReferenceDataMethods_dict["where_clause_I"]
        if "used__I" in ReferenceDataMethods_dict.keys():
            used__I = ReferenceDataMethods_dict["used__I"]
        if "experiment_limit_I" in ReferenceDataMethods_dict.keys():
            experiment_limit_I = ReferenceDataMethods_dict["experiment_limit_I"]
        if "mqresultstable_limit_I" in ReferenceDataMethods_dict.keys():
            mqresultstable_limit_I = ReferenceDataMethods_dict["mqresultstable_limit_I"]
        # if "settings_filename_I" in ReferenceDataMethods_dict.keys():
        #     settings_filename_I = ReferenceDataMethods_dict["settings_filename_I"]
        # if "data_filename_O" in ReferenceDataMethods_dict.keys():
        #     data_filename_O = ReferenceDataMethods_dict["data_filename_O"]

        # read in the reference data
        reference_data = []
        if referenceData_csv_i is not None:            
            smartpeak_i = smartPeak_i()
            smartpeak_i.read_csv(referenceData_csv_i)
            reference_data = smartpeak_i.getData()
            smartpeak_i.clear_data()
        elif db_ini_i is not None:
            referenceDataMethods = ReferenceDataMethods()
            reference_data = referenceDataMethods.getAndProcess_referenceData_samples(
                experiment_ids_I=experiment_ids_I,
                sample_names_I=sample_names_I,
                sample_types_I=sample_types_I,
                acquisition_methods_I=acquisition_methods_I,
                quantitation_method_ids_I=quantitation_method_ids_I,
                component_names_I=component_names_I,
                component_group_names_I=component_group_names_I,
                where_clause_I=where_clause_I,
                used__I=used__I,
                experiment_limit_I=experiment_limit_I,
                mqresultstable_limit_I=mqresultstable_limit_I,
                settings_filename_I=db_ini_i,
                data_filename_O=''
            )
        self.reference_data = reference_data

    def validate(
        self,
        MRMRFeatureValidator_params_I={},
        verbose_I=False
    ):
        """Validate the selected peaks agains reference data
        """
        if verbose_I:
            print("Validating features")

        # map the reference data
        if MRMRFeatureValidator_params_I:
            featureValidator = MRMFeatureValidator()
            features_mapped, validation_metrics = featureValidator.validate_MRMFeatures(
                reference_data=self.reference_data,
                features=self.featureMap,
                Tr_window=float(MRMRFeatureValidator_params_I[0]['value'])
                )
            self.featureMap = features_mapped
            self.validation_metrics = validation_metrics

    def export_featurePlots(
        self,        
        filenames_I,
        FeaturePlotter_params_I={},
        verbose_I=False
    ):
        """Export plots of peaks with features annotated
        """
        if verbose_I:
            print("Plotting peaks with features")
        
        # Handle the filenames
        features_pdf_o = None
        if 'features_pdf_o'in filenames_I.keys():
            features_pdf_o = filenames_I['features_pdf_o']  

        # export diagnostic plots
        if FeaturePlotter_params_I:
            featurePlotter = FeaturePlotter()
            featurePlotter.setParameters(FeaturePlotter_params_I)
            featurePlotter.plot_peaks(
                filename_I=features_pdf_o,
                transitions=self.targeted,
                chromatograms=self.chromatogram_map,
                features=self.featureMap
            )