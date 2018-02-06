# -*- coding: utf-8 -*-
from smartPeak.core.SequenceSegmentProcessor import SequenceSegmentProcessor
from smartPeak.core.SequenceSegmentHandler import SequenceSegmentHandler
from smartPeak.core.SequenceHandler import SequenceHandler
from smartPeak.core.RawDataHandler import RawDataHandler
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestSequenceSegmentProcessor():
    """tests for SequenceSegmentProcessor class
    """

    def test_checkSequenceSegmentProcessing(self):
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        events = [
            "calculate_calibration",
            "calculate_carryover",
            "calculate_variability",
            "store_quantitation_methods",
            "load_quantitation_methods",
            "store_components_to_concentrations",
            "plot_calibrators"]
        assert(sequenceSegmentProcessor.checkSequenceSegmentProcessing(events))
        
        events = [
            "calculate_calibration",
            "carryover",
            "calculate_variability",
            "store_quantitation_methods",
            "load_quantitation_methods",
            "store_components_to_concentrations",
            "plot_calibrators"]
        assert(~sequenceSegmentProcessor.checkSequenceSegmentProcessing(events))

    def test_getDefaultSequenceSegmentProcessingWorkflow(self):
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Unknown") == [])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Standard") == ["calculate_calibration"])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "QC") == ["calculate_variability"])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Blank") == [])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Double Blank") == [])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Solvent") == ["calculate_carryover"])

    def test_getSampleIndicesBySampleType(self):
        sequenceHandler = SequenceHandler()
        sequenceSegmentHandler = SequenceSegmentHandler()
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        # test data
        meta_data_required = {h: None for h in sequenceHandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Standard'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        sequenceHandler.addSampleToSequence(meta_data1, featuremap1)
        sequenceHandler.addSampleToSequence(meta_data2, featuremap2)
        sequenceHandler.addSampleToSequence(meta_data3, featuremap3)
        sequenceSegmentHandler.sample_indices = [0, 1, 2]

        sample_indices = sequenceSegmentProcessor.getSampleIndicesBySampleType(
            sequenceSegmentHandler,
            sequenceHandler,
            "Unknown"
        )
        assert(sample_indices == [0, 2])

    def test_optimizeCalibrationCurves(self):
        sequenceHandler = SequenceHandler()
        sequenceSegmentHandler = SequenceSegmentHandler()
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        # set-up the class parameters 
        absquant_params = {"AbsoluteQuantitation": [
            {"name": "min_points", "value": "4"},
            {"name": "max_bias", "value": "30.0"},
            {"name": "min_correlation_coefficient", "value": "0.9"},
            {"name": "max_iters", "value": "100"},
            {"name": "outlier_detection_method", "value": "iter_jackknife"},
            {"name": "use_chauvenet", "value": "false"},
        ]}

        # set up the quantitation method 
        aqm = pyopenms.AbsoluteQuantitationMethod()
        feature_name = "peak_apex_int"
        transformation_model = "linear"
        param = pyopenms.Param()
        param.setValue("slope".encode("utf-8"), 1.0)
        param.setValue("intercept".encode("utf-8"), 0.0)
        param.setValue("x_weight".encode("utf-8"), "ln(x)".encode("utf-8"))
        param.setValue("y_weight".encode("utf-8"), "ln(y)".encode("utf-8"))
        param.setValue("x_datum_min".encode("utf-8"), -1e12)
        param.setValue("x_datum_max".encode("utf-8"), 1e12)
        param.setValue("y_datum_min".encode("utf-8"), -1e12)
        param.setValue("y_datum_max".encode("utf-8"), 1e12)

        # set-up the quant_method map
        quant_methods = []
        # component_1
        aqm = pyopenms.AbsoluteQuantitationMethod()
        aqm.setComponentName("ser-L.ser-L_1.Light")
        aqm.setISName("ser-L.ser-L_1.Heavy")
        aqm.setFeatureName(feature_name)
        aqm.setConcentrationUnits("uM")
        aqm.setTransformationModel(transformation_model)
        aqm.setTransformationModelParams(param)
        quant_methods.append(aqm)
        # component_2
        aqm = pyopenms.AbsoluteQuantitationMethod()
        aqm.setComponentName("amp.amp_1.Light")
        aqm.setISName("amp.amp_1.Heavy")
        aqm.setFeatureName(feature_name)
        aqm.setConcentrationUnits("uM")
        aqm.setTransformationModel(transformation_model)
        aqm.setTransformationModelParams(param)
        quant_methods.append(aqm)
        # component_3
        aqm = pyopenms.AbsoluteQuantitationMethod()
        aqm.setComponentName("atp.atp_1.Light")
        aqm.setISName("atp.atp_1.Heavy")
        aqm.setFeatureName(feature_name)
        aqm.setConcentrationUnits("uM")
        aqm.setTransformationModel(transformation_model)
        aqm.setTransformationModelParams(param)
        quant_methods.append(aqm)

        sequenceSegmentHandler.setQuantitationMethods(quant_methods)

        # set up the featureMaps, runConcentrations, and sequence
        runs = []
        self.make_featuresAndStandardsConcentrations(sequenceHandler, runs)
        sequenceSegmentHandler.setStandardsConcentrations(runs)

        # register the sequence group manually
        sequenceSegmentHandler.setSampleIndices(range(len(sequenceHandler.sequence)))

        # test
        sequenceSegmentProcessor.optimizeCalibrationCurves(
            sequenceSegmentHandler,
            sequenceHandler,
            AbsoluteQuantitation_params_I=absquant_params["AbsoluteQuantitation"])
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getComponentName() == b'amp.amp_1.Light')
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getISName() == b'amp.amp_1.Heavy')
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getFeatureName() == b"peak_apex_int")
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getTransformationModelParams().getValue("slope") == 0.957996830126945)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getTransformationModelParams().getValue(
                "intercept") == -1.0475433871941753)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getNPoints() == 11)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getCorrelationCoefficient() == 0.9991692616730385)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getLLOQ() == 0.02)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getULOQ() == 40.0)
        
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getComponentName() == b'atp.atp_1.Light')
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getISName() == b'atp.atp_1.Heavy')
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getFeatureName() == b"peak_apex_int")
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getTransformationModelParams().getValue("slope") == 0.6230408240794582)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getTransformationModelParams().getValue(
                "intercept") == 0.36130172586029285)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getNPoints() == 6)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getCorrelationCoefficient() == 0.9982084021849695)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getLLOQ() == 0.02)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            1].getULOQ() == 40.0)
        
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getComponentName() == b'ser-L.ser-L_1.Light')
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getISName() == b'ser-L.ser-L_1.Heavy')
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getFeatureName() == b"peak_apex_int")
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getTransformationModelParams().getValue("slope") == 0.9011392589148208)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getTransformationModelParams().getValue("intercept") == 1.8701850759567624)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getNPoints() == 11)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getCorrelationCoefficient() == 0.9993200722867581)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getLLOQ() == 0.04)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            2].getULOQ() == 200.0)
    
    def make_featuresAndStandardsConcentrations(self, sequenceHandler_IO, runs):

        # ser-L.ser-L_1.Light
        x1 = [
            2.32e4, 2.45e4, 1.78e4, 2.11e4, 1.91e4,
            2.06e4, 1.85e4, 1.53e4, 1.40e4, 1.03e4, 
            1.07e4, 6.68e3, 5.27e3, 2.83e3]
        y1 = [
            4.94e3, 6.55e3, 7.37e3, 1.54e4, 2.87e4,
            5.41e4, 1.16e5, 1.85e5, 3.41e5, 7.54e5,
            9.76e5, 1.42e6, 1.93e6, 2.23e6] 
        z1 = [
            1.00e-2, 2.00e-2, 4.00e-2, 1.00e-1, 2.00e-1, 
            4.00e-1, 1.00e0, 2.00e0, 4.00e0, 1.00e1, 
            2.00e1, 4.00e1, 1.00e2, 2.00e2]
        
        # amp.amp_1.Light
        x2 = [
            2.15e5, 2.32e5, 2.69e5, 2.53e5, 2.50e5, 
            2.75e5, 2.67e5, 3.31e5, 3.15e5, 3.04e5, 
            3.45e5, 3.91e5, 4.62e5, 3.18e5]
        y2 = [
            4.40e2, 1.15e3, 1.53e3, 2.01e3, 4.47e3, 
            7.36e3, 2.18e4, 4.46e4, 8.50e4, 2.33e5, 
            5.04e5, 1.09e6, 2.54e6, 3.64e6] 
        z2 = [
            2.00e-3, 4.00e-3, 8.00e-3, 2.00e-2, 4.00e-2, 
            8.00e-2, 2.00e-1, 4.00e-1, 8.00e-1, 2.00e0, 
            4.00e0, 8.00e0, 2.00e1, 4.00e1]
        
        # atp.atp_1.Light
        x3 = [
            8.28e2, 1.32e3, 1.57e3, 1.63e3, 1.48e3, 
            2.43e3, 4.44e3, 1.03e4, 1.75e4, 6.92e4, 
            1.97e5, 2.69e5, 3.20e5, 3.22e5]
        y3 = [
            2.21e2, 4.41e2, 3.31e2, 2.21e2, 3.09e2, 
            5.96e2, 1.26e3, 2.49e3, 1.12e4, 8.79e4, 
            4.68e5, 1.38e6, 3.46e6, 4.19e6] 
        z3 = [
            2.00e-3, 4.00e-3, 8.00e-3, 2.00e-2, 4.00e-2, 
            8.00e-2, 2.00e-1, 4.00e-1, 8.00e-1, 2.00e0, 
            4.00e0, 8.00e0, 2.00e1, 4.00e1]

        for i in range(len(x1)):
            sample_name = "level" + str(i)
            feature_map = pyopenms.FeatureMap()

            # ser-L.ser-L_1.Light
            mrm_feature = pyopenms.MRMFeature()
            component = pyopenms.Feature()
            IS_component = pyopenms.Feature()
            run = pyopenms.AQS_runConcentration()
            # featureMap
            component.setMetaValue(
                "native_id".encode("utf-8"), 
                "ser-L.ser-L_1.Light".encode("utf-8"))
            component.setMetaValue("peak_apex_int".encode("utf-8"), y1[i])
            IS_component.setMetaValue(
                "native_id".encode("utf-8"), 
                "ser-L.ser-L_1.Heavy".encode("utf-8"))
            IS_component.setMetaValue("peak_apex_int".encode("utf-8"), x1[i])
            mrm_feature.setSubordinates([component, IS_component])
            feature_map.push_back(mrm_feature)

            # runConcentrations
            run.sample_name = sample_name.encode("utf-8")
            run.component_name = "ser-L.ser-L_1.Light".encode("utf-8")
            run.IS_component_name = "ser-L.ser-L_1.Heavy".encode("utf-8")
            run.actual_concentration = z1[i]
            run.IS_actual_concentration = 1.0
            run.concentration_units = "uM".encode("utf-8")
            run.dilution_factor = 1.0
            runs.append(run)

            # amp.amp_1.Light
            mrm_feature = pyopenms.MRMFeature()
            component = pyopenms.Feature()
            IS_component = pyopenms.Feature()
            run = pyopenms.AQS_runConcentration()
            # featureMap
            component.setMetaValue(
                "native_id".encode("utf-8"), 
                "amp.amp_1.Light".encode("utf-8"))
            component.setMetaValue("peak_apex_int".encode("utf-8"), y2[i])
            IS_component.setMetaValue(
                "native_id".encode("utf-8"), 
                "amp.amp_1.Heavy".encode("utf-8"))
            IS_component.setMetaValue("peak_apex_int".encode("utf-8"), x2[i])
            mrm_feature.setSubordinates([component, IS_component])
            feature_map.push_back(mrm_feature)

            # runConcentrations
            run.sample_name = sample_name.encode("utf-8")
            run.component_name = "amp.amp_1.Light".encode("utf-8")
            run.IS_component_name = "amp.amp_1.Heavy".encode("utf-8")
            run.actual_concentration = z2[i]
            run.IS_actual_concentration = 1.0
            run.concentration_units = "uM".encode("utf-8")
            run.dilution_factor = 1.0
            runs.append(run)

            # atp.atp_1.Light
            mrm_feature = pyopenms.MRMFeature()
            component = pyopenms.Feature()
            IS_component = pyopenms.Feature()
            run = pyopenms.AQS_runConcentration()
            # featureMap
            component.setMetaValue(
                "native_id".encode("utf-8"), 
                "atp.atp_1.Light".encode("utf-8"))
            component.setMetaValue("peak_apex_int".encode("utf-8"), y3[i])
            IS_component.setMetaValue(
                "native_id".encode("utf-8"), 
                "atp.atp_1.Heavy".encode("utf-8"))
            IS_component.setMetaValue("peak_apex_int".encode("utf-8"), x3[i])
            mrm_feature.setSubordinates([component, IS_component])
            feature_map.push_back(mrm_feature)

            # runConcentrations
            run.sample_name = sample_name.encode("utf-8")
            run.component_name = "atp.atp_1.Light".encode("utf-8")
            run.IS_component_name = "atp.atp_1.Heavy".encode("utf-8")
            run.actual_concentration = z3[i]
            run.IS_actual_concentration = 1.0
            run.concentration_units = "uM".encode("utf-8")
            run.dilution_factor = 1.0
            runs.append(run)

            feature_map.setPrimaryMSRunPath([sample_name.encode("utf-8")])

            # register the sample in the sequence
            meta_data = {}
            meta_data["sample_name"] = sample_name
            meta_data["sample_group_name"] = "group1"
            meta_data["sample_type"] = "Standard"
            meta_data["filename"] = "filename" + str(i)
            meta_data["sequence_segment_name"] = "segment1"
            sequenceHandler_IO.addSampleToSequence(meta_data, None)

            # add in the featureMap manually
            rawDataHandler = RawDataHandler()
            rawDataHandler.setFeatureMap(feature_map)
            sequenceHandler_IO.sequence[i].setRawData(rawDataHandler)

        def test_processSequenceSegment(self):
            """TODO: add test body"""
            pass