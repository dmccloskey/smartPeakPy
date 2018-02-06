# -*- coding: utf-8 -*-
from smartPeak.core.Utilities import Utilities
# 3rd part libraries
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import pyopenms
except ImportError as e:
    print(e)
try:
    import pyopenms
except ImportError as e:
    print(e)


class SequenceSegmentPlotter():
    """A class to sequence segment attributes"""

    def __init__(self):
        """
        """
        self.annotate_features = None
        self.export_type = None
    
    def clear(self):
        """Reset parameters"""
        self.annotate_features = None
        self.export_type = None

    def setParameters(self, params):
        """Set plotting parameters"""

        utilities = Utilities()
        parameters = {
            d['name']: utilities.castString(d['value'], d['type'])
            for d in params}
        if "annotate_features" in parameters:
            self.annotate_features = parameters["annotate_features"]
        if "export_type" in parameters:
            self.export_type = parameters["export_type"]

    def plotCalibrationPoints(
        self, filename_I, 
        sequenceSegmentHandler_I, 
        component_names_I=[]
    ):
        """Export scatter plots for each calibration curve
        
        Args:
            filename_I (string): name of the file
            component_names_I (list): list of component_names to plot
        
        """
        
        # handle the user input
        components_to_concentrations = {}
        if component_names_I:
            for component_name, points in sequenceSegmentHandler_I.getComponentsToConcentrations().items():
                if component_name in component_names_I:
                    components_to_concentrations.update({
                        component_name: points
                    })
        else:
            components_to_concentrations = sequenceSegmentHandler_I.getComponentsToConcentrations()

        # make a map of the quantitation method for speed
        absoluteQuantitation = pyopenms.AbsoluteQuantitation()
        absoluteQuantitation.setQuantMethods(sequenceSegmentHandler_I.getQuantitationMethods())
        # NOTE: C++ can use the internal getQuantMethodsAsMap()
        quantitation_method = {
            d.getComponentName(): d.getFeatureName() for d in 
            sequenceSegmentHandler_I.getQuantitationMethods()}

        for component_name, points in components_to_concentrations.items():
            # extract out the points
            x_values = []
            y_values = []
            for point in points:
                # feature ratios
                feature_ratio = absoluteQuantitation.calculateRatio(
                    point.feature,
                    point.IS_feature,
                    quantitation_method[component_name]
                )
                feature_ratio = feature_ratio/point.dilution_factor
                y_values.append(feature_ratio)

                # concentration ratios
                concentration_ratio = point.actual_concentration/point.IS_actual_concentration
                x_values.append(concentration_ratio)
            
            # open the pdf file
            filename = filename_I + "_" + component_name.decode("utf-8") + ".pdf"
            with PdfPages(filename) as pp:                
                # generate the new figure
                fig = plt.figure()
                # fig = plt.figure(num=sub_cnt)
                # ax1 = fig.add_subplot(1, n_plots, sub_cnt + 1)
                ax1 = fig.add_subplot(1, 1, 1)

                # raw points
                ax1.scatter(
                    x_values,
                    y_values, 
                    s=10, c='b', marker=".", label='points'
                    )
                
                ax1.set_title(component_name.decode("utf-8"))

                pp.savefig(fig)

                # close figures
                plt.close()
                plt.clf()
                plt.cla()