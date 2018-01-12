# -*- coding: utf-8 -*-
from smartPeak.core.Utilities import Utilities
from smartPeak.io.FileReader import FileReader
from smartPeak.pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from smartPeak.pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
from smartPeak.data.ReferenceDataMethods import ReferenceDataMethods
# external
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class FileReaderOpenMS():

    def load_quantitationMethods(
        self,
        sample_IO,
        filenames_I,
        verbose_I=False
    ):
        """Load AbsoluteQuantitationMethods

        Args:
            sample_IO (SampleHandler)
            filenames_I (dict): dictionary of filename strings

        Internals:
            quantitationMethods (list): list of AbsoluteQuantitationMethod objects

        """
        if verbose_I:
            print("loading quantitation methods")

        quantitationMethods_csv_i = None
        if 'quantitationMethods_csv_i'in filenames_I.keys():
            quantitationMethods_csv_i = filenames_I['quantitationMethods_csv_i']

        quantitationMethods = []
        aqmf = pyopenms.AbsoluteQuantitationMethodFile()
        aqmf.load(quantitationMethods_csv_i, quantitationMethods)
        sample_IO.quantitationMethods = quantitationMethods

    def load_TraML(self, sample_IO, filenames_I, verbose_I=False):
        """Load TraML file

        Args:
            sample_IO (SampleHandler): sample object; updated in place
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
        sample_IO.targeted = targeted

    def load_Trafo(
        self,
        sample_IO,
        filenames_I,
        MRMFeatureFinderScoring_params_I={},
        verbose_I=False
    ):
        """Load Trafo file

        Args:
            sample_IO (SampleHandler): sample object; updated in place
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
        utilities = Utilities()
        parameters = utilities.updateParameters(
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
        # model_params = utilities.setParameters(model_params_list,model_params)

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
                sample_IO.chromatogram_map,
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
        sample_IO.trafo = trafo

    def load_MSExperiment(
        self,
        sample_IO,
        filenames_I,
        MRMMapping_params_I={},
        chromatogramExtractor_params_I={},
        verbose_I=False
    ):
        """Load MzML into an MSExperiment

        Args:
            sample_IO (SampleHandler): sample object; updated in place
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
            sample_IO.targeted is not None:
            # convert parameters
            utilities = Utilities()
            chromatogramExtractor_params = {d['name']: utilities.castString(
                d['value'], 
                d['type']) for d in chromatogramExtractor_params_I}
            # chromatogramExtractor_params = {d['name']:utilities.parseString(d['value']) 
            #   for d in chromatogramExtractor_params_I}
            # exctract chromatograms
            chromatograms_copy = copy.copy(chromatograms)
            chromatograms.clear(True)
            if chromatogramExtractor_params['extract_precursors']:
                tr = sample_IO.targeted.getTransitions()
                for t in tr:
                    t.setProductMZ(t.getPrecursorMZ())
                sample_IO.targeted.setTransitions(tr)
            chromatogramExtractor = pyopenms.ChromatogramExtractor()
            chromatogramExtractor.extractChromatograms(
                chromatograms_copy,
                chromatograms, 
                sample_IO.targeted,
                chromatogramExtractor_params['extract_window'],
                chromatogramExtractor_params['ppm'],
                pyopenms.TransformationDescription(),
                chromatogramExtractor_params['rt_extraction_window'],
                chromatogramExtractor_params['filter'],
                )

        sample_IO.msExperiment = chromatograms

        # map transitions to the chromatograms
        if MRMMapping_params_I and \
            MRMMapping_params_I is not None and \
            sample_IO.targeted is not None:        
            # set up MRMMapping and
            # parse the MRMMapping params
            mrmmapper = pyopenms.MRMMapping()
            utilities = Utilities()
            parameters = mrmmapper.getParameters()
            parameters = utilities.updateParameters(
                parameters,
                MRMMapping_params_I,
                )
            mrmmapper.setParameters(parameters)  
            chromatogram_map = pyopenms.MSExperiment()

            # mrmmapper = MRMMapper()
            # chromatogram_map = mrmmapper.algorithm(
            #     chromatogram_map=chromatograms,
            #     targeted=sample_IO.targeted, 
            #     precursor_tolerance=0.0009, #hard-coded for now
            #     product_tolerance=0.0009, #hard-coded for now
            #     allow_unmapped=True,
            #     allow_double_mappings=True
            # )

            mrmmapper.mapExperiment(chromatograms, sample_IO.targeted, chromatogram_map)
        sample_IO.chromatogram_map = chromatogram_map

    def load_SWATHorDIA(
        self,
        sample_IO,
        filenames_I,
        verbose_I=False
    ):
        """Load SWATH or DIA into an MSExperiment

        Args:
            sample_IO (SampleHandler): sample object; updated in place
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
                targeted=sample_IO.targeted,
                extraction_window=0.05,
                min_upper_edge_dist=0.0,
                ppm=False,
                is_swath=False,
                rt_extraction_window=-1,
                extraction_function="tophat"
            )
        sample_IO.swath = swath

    def load_featureMap(
        self,
        sample_IO,
        filenames_I={},
        verbose_I=False
    ):
        """Load a FeatureMap
        
        Args:
            sample_IO (SampleHandler): sample object; updated in place
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

        sample_IO.featureMap = output

    def load_validationData(
        self,
        sample_IO,
        filenames_I,
        ReferenceDataMethods_params_I={},
        verbose_I=False
    ):
        """Load the validation data from file or from a database
        
        Args:
            sample_IO (SampleHandler): sample object; updated in place
            filenames_I (dict): dictionary of filenames
            ReferenceDataMethods_params_I (dict): dictionary of DB query parameters
        
        """
        if verbose_I:
            print("Loading validation data")

        utilities = Utilities()

        # Handle the filenames
        referenceData_csv_i, db_ini_i = None, None
        if 'referenceData_csv_i'in filenames_I.keys(): 
            referenceData_csv_i = filenames_I['referenceData_csv_i']
        if 'db_ini_i'in filenames_I.keys(): 
            db_ini_i = filenames_I['db_ini_i']

        # Parse the input parameters
        ReferenceDataMethods_dict = {d['name']: utilities.parseString(
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
            smartpeak_i = FileReader()
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
        sample_IO.reference_data = reference_data