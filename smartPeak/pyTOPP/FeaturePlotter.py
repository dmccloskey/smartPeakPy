# -*- coding: utf-8 -*-
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

        # main loop
        for feature in features:
            component_group_name = feature.getMetaValue("PeptideRef").decode("utf-8")
            pp = PdfPages(filename_I + "_" + component_group_name + ".pdf")
            n_plots = len(feature.getSubordinates())
            for sub_cnt, subordinate in enumerate(feature.getSubordinates()):
                component_name = subordinate.getMetaValue("native_id")
                chrom = [
                    c for c in chromatograms.getChromatograms()
                    if c.getNativeID() == component_name]

                fig = plt.figure(num=sub_cnt)
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
                plt.close(fig)
            pp.close()