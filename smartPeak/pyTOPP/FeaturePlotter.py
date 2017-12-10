# -*- coding: utf-8 -*-
from smartPeak.core.smartPeak import smartPeak
# 3rd part libraries
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
except ImportError as e:
    print(e)


class FeaturePlotter():
    """A class to plot peaks with annotated features"""

    def __init__(self):
        """
        """
        self.annotate_features = None
        self.export_type = None
    
    def clearParamaeters(self):
        """Reset parameters"""
        self.annotate_features = None
        self.export_type = None

    def setParameters(self, params):
        """Set plotting parameters"""

        smartpeak = smartPeak()
        parameters = {
            d['name']: smartpeak.castString(d['value'], d['type'])
            for d in params}
        if "annotate_features" in parameters:
            self.annotate_features = parameters["annotate_features"]
        if "export_type" in parameters:
            self.export_type = parameters["export_type"]

    def plot_features(
        self,
        filename_I,
        chromatograms,
        features,
        plot_params=[
            {"name": "", "value": 1}]
    ):
        """Plot peaks with annoted features in a .pdf file
        
        Args:
            filename_I (string): name of the file
            chromatograms (pyopenms.MSExperiment): mapped chromatograms
            featureMap (pyopenms.FeatureMap): mapped features

        """
        # main loop
        for feature in features:
            component_group_name = feature.getMetaValue("PeptideRef").decode("utf-8")
            # n_plots = len(feature.getSubordinates())

            # open the pdf file
            with PdfPages(filename_I + "_" + component_group_name + ".pdf") as pp:
                for sub_cnt, subordinate in enumerate(feature.getSubordinates()):
                    component_name = subordinate.getMetaValue("native_id")
                    chrom = [
                        c for c in chromatograms.getChromatograms()
                        if c.getNativeID() == component_name]

                    # generate the new figure
                    fig = plt.figure()
                    # fig = plt.figure(num=sub_cnt)
                    # ax1 = fig.add_subplot(1, n_plots, sub_cnt + 1)
                    ax1 = fig.add_subplot(1, 1, 1)

                    # raw points
                    ax1.scatter(
                        chrom[0].get_peaks()[0],
                        chrom[0].get_peaks()[1], 
                        s=10, c='b', marker=".", label='points'
                        )

                    # features
                    feature_rt = []
                    feature_int = []
                    for i, p in enumerate(chrom[0].get_peaks()[0]):
                        if p >= feature.getMetaValue("leftWidth") and\
                        p <= feature.getMetaValue("rightWidth"):
                            feature_rt.append(p)
                            feature_int.append(chrom[0].get_peaks()[1][i])
                    ax1.scatter(
                        feature_rt, feature_int, s=10, c='r', 
                        marker="o", label='selected peak')
                    
                    ax1.set_title(component_name.decode("utf-8"))

                    # plt.legend(loc='upper left')
                    # fig.savefig(filename_I + "_" + component_name.decode("utf-8") + ".pdf")
                    pp.savefig(fig)

                    # close figures
                    plt.close()
                    plt.clf()
                    plt.cla()

    def plot_peaks(
        self,
        filename_I,
        chromatograms,
        transitions, 
        features=[]
    ):
        """Plot peaks in a .pdf file
        
        Args:
            filename_I (string): name of the file
            chromatograms (pyopenms.MSExperiment): mapped chromatograms
            transitions (pyopenms.TargetedExperiment): list of transitions
            featureMap (pyopenms.FeatureMap): mapped features

        """
        # organize transitions by transition group
        component_group_names = [t.getPeptideRef() for t in transitions.getTransitions()]
        component_group_names = list(set(component_group_names))

        for component_group_name in component_group_names:
            transition_group = [
                t for t in transitions.getTransitions()
                if t.getPeptideRef() == component_group_name]
            if self.annotate_features:
                feature = [
                    f for f in features
                    if f.getMetaValue(
                        "PeptideRef") == component_group_name]
                if feature:
                    feature = feature[0]
            else:
                feature = []

            # open the pdf file
            with PdfPages(
                    filename_I + "_" + component_group_name.decode("utf-8") +
                    ".pdf") as pp:
                for t in transition_group:
                    component_name = t.getNativeID()
                    chrom = [
                        c for c in chromatograms.getChromatograms()
                        if c.getNativeID() == component_name]
                    if feature:
                        subordinate = [
                            s for s in feature.getSubordinates()
                            if s.getMetaValue("native_id") == component_name]
                        if subordinate:
                            subordinate = subordinate[0]
                    else:
                        subordinate = []

                    # generate the new figure
                    fig = plt.figure()
                    # fig = plt.figure(num=sub_cnt)
                    # ax1 = fig.add_subplot(1, n_plots, sub_cnt + 1)
                    ax1 = fig.add_subplot(1, 1, 1)

                    # raw points
                    ax1.scatter(
                        chrom[0].get_peaks()[0],
                        chrom[0].get_peaks()[1], 
                        s=10, c='b', marker=".", label='points'
                        )

                    # features
                    if subordinate:
                        # hull_points = subordinate.getConvexHull().getHullPoints()
                        feature_rt = []
                        feature_int = []
                        for i, p in enumerate(chrom[0].get_peaks()[0]):
                            if p >= feature.getMetaValue("leftWidth") and\
                            p <= feature.getMetaValue("rightWidth"):
                                feature_rt.append(p)
                                feature_int.append(chrom[0].get_peaks()[1][i])
                        ax1.scatter(
                            feature_rt, feature_int, s=10, c='r', 
                            marker="o", label='selected peak')
                    
                    ax1.set_title(component_name.decode("utf-8"))

                    pp.savefig(fig)

                    # close figures
                    plt.close()
                    plt.clf()
                    plt.cla()
