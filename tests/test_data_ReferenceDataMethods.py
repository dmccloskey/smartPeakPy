# -*- coding: utf-8 -*-
from smartPeak.data.ReferenceDataMethods import ReferenceDataMethods
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestReferenceDataMethods():

    def test_getAndProcessReferenceDataSamples(self):
        """Test getAndProcess_referenceData_samples
        
        TODO: change settings_filename_I directory?
        """

        refDataMethods = ReferenceDataMethods()
        # reference data for samples
        data_ref_processed = refDataMethods.getAndProcess_referenceData_samples(
            experiment_ids_I=['BloodProject01'],
            sample_names_I=['150601_0_BloodProject01_PLT_QC_Broth-1'],
            acquisition_methods_I=['140718_McCloskey2013'],
            used__I=True,
            settings_filename_I='/home/user/Data/settings_metabolomics.json',
            data_filename_O=None)
        assert(len(data_ref_processed) == 179)
        assert(data_ref_processed[0][
            'sample_name'] == '150601_0_BloodProject01_PLT_QC_Broth-1')
        assert(data_ref_processed[0][
            'sample_type'] == 'Quality Control')
        assert(data_ref_processed[0]['component_name'] == '23dpg.23dpg_1.Heavy')
        assert(data_ref_processed[178][
            'sample_name'] == '150601_0_BloodProject01_PLT_QC_Broth-1')
        assert(data_ref_processed[178]['sample_type'] == 'Quality Control')
        assert(data_ref_processed[178]['component_name'] == 'xan.xan_1.Light')

    def test_getAndProcessReferenceDataCalibrators(self):
        """Test getAndProcess_referenceData_calibrators"""

        refDataMethods = ReferenceDataMethods()
        # reference data for calibrators
        data_ref_processed = refDataMethods.getAndProcess_referenceData_calibrators(
            experiment_ids_I=['BloodProject01'],
            sample_names_I=[],
            sample_types_I=['Standard'],
            acquisition_methods_I=['140718_McCloskey2013'],
            used__I=True,
            settings_filename_I='/home/user/Data/settings_metabolomics.json',
            data_filename_O=None)
        assert(len(data_ref_processed) == 193)
        assert(data_ref_processed[0]['sample_name'] == 'Calibrators')
        assert(data_ref_processed[0]['component_name'] == 'cytd.cytd_1.Light')
        assert(data_ref_processed[192]['sample_name'] == 'Calibrators')
        assert(data_ref_processed[192]['component_name'] == 'gthox.gthox_1.Light')
