# -*- coding: utf-8 -*-
# 3rd part libraries
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
except ImportError as e:
    print(e)


class FeaturePlotter():
    """A class to plot peaks with annotated features"""

    def __init__(self):
        """
        """
        self.MSExperiment = []
        self.featureMap = {}

    def plot_peaks(
        self,
        filename_I,
        chromatograms,       
        features,     
        plot_params=[
            {"name": "", "value": 1}],
        verbose_I=False
    ):
        """Plot peaks in a .pdf file
        
        Args:
            filename_I (string): name of the file
            chromatograms (pyopenms.MSExperiment): mapped chromatograms
            featureMap (pyopenms.FeatureMap): mapped features

        """
        if verbose_I:
            print("Ploting peaks with features")

        fig = plt.figure()
        pp = PdfPages(filename_I)

        # main loop
        for feature in features:
            for subordinate in feature.getSubordinates():
                component_name = subordinate.getMetaValue("native_id")
                chrom = [
                    c for c in chromatograms.getChromatograms()
                    if c.getNativeID() == component_name]
                ax1 = fig.add_subplot(111)

                # raw points
                ax1.scatter(
                    chrom[0].get_peaks()[0],
                    chrom[0].get_peaks()[1], 
                    s=10, c='b', marker="s", label='points'
                    )
                feature_rt = [
                    p for p in chrom[0].get_peaks()[0]
                    if p >= subordinate.getMetaValue("leftWidth") and
                    p <= subordinate.getMetaValue("rightWidth")
                    ]
                feature_int = [
                    p for p in chrom[0].get_peaks()[1]
                    if p >= subordinate.getMetaValue("leftWidth") and
                    p <= subordinate.getMetaValue("rightWidth")
                    ]
                # features
                ax1.scatter(
                    feature_rt, feature_int, s=10, c='r', 
                    marker="o", label='selected peak')
                plt.legend(loc='upper left')
                plt.show()

                fig.savefig(pp, format='pdf')
        pp.close()