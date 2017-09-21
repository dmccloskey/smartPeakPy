# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
from smartPeak.data.ReferenceDataMethods import ReferenceDataMethods
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class TestReferenceDataMethods():

    def test_getAndProcessReferenceDataSamples(self):
        """Test getAndProcess_referenceData_samples"""

        refDataMethods = ReferenceDataMethods()
        # reference data for samples
        data_ref_processed = refDataMethods.getAndProcess_referenceData_samples(
            experiment_ids_I = ['BloodProject01'],
            sample_names_I = ['150601_0_BloodProject01_PLT_QC_Broth-1'],
            acquisition_methods_I = ['140718_McCloskey2013'],
            used__I = True,
            settings_filename_I = '/home/user/openMS_MRMworkflow/settings_metabolomics.ini',
            data_filename_O = None)
        assert(1==1)

    def test_getAndProcessReferenceDataCalibrators(self):
        """Test getAndProcess_referenceData_calibrators"""

        refDataMethods = ReferenceDataMethods()
        # reference data for calibrators
        data_ref_processed = refDataMethods.getAndProcess_referenceData_calibrators(
            experiment_ids_I = ['BloodProject01'],
            sample_names_I = [],
            sample_types_I = ['Standard'],
            acquisition_methods_I = ['140718_McCloskey2013'],
            used__I = True,
            settings_filename_I = '/home/user/openMS_MRMworkflow/settings_metabolomics.ini',
            data_filename_O = None)
        assert(1==1)
