# -*- coding: utf-8 -*-
try:
    import pyopenms
except ImportError as e:
    print(e)

"""
"""
class OpenSwathChromatogramExtractor():
    """Extract chromatograms (XIC) from a MS2 map file.

    Source:
        https://github.com/sneumann/OpenMS/blob/master/pyOpenMS/pyTOPP/OpenSwathChromatogramExtractor.py
    """
    def main(
        self,
        infiles,
        targeted,
        extraction_window=0.05,
        min_upper_edge_dist=0.0,
        ppm=False,
        is_swath=False,
        rt_extraction_window=-1,
        extraction_function="tophat"
        ):
        """Extract chromatograms (XIC) from a MS2 map file.

        Args:
            infiles (list, str): An input file containing spectra
            targeted: TraML input file containt the transitions
            extraction_window (float): default=0.05, Extraction window in Th
            min_upper_edge_dist (float): default=0.0, Minimal distance to the edge to still consider a precursor, in Thomson (for Swath)
            ppm (bool): default=False, use ppm instead of Th
            is_swath (bool): default=False, The input file is a SWATH file
            rt_extraction_window (float): default=-1, Extraction window in RT
            extraction_function (str): default="tophat", Extraction function (tophat or bartlett)

        Returns:        
            output: Output chrom.mzML file with chromatograms

        Source:
            https://github.com/sneumann/OpenMS/blob/master/pyOpenMS/pyTOPP/OpenSwathChromatogramExtractor.py
        """

        # Create empty files as input and finally as output
        empty_swath = pyopenms.MSExperiment()
        trafo = pyopenms.TransformationDescription()
        output = pyopenms.MSExperiment()

        # load input
        for infile in infiles:
            exp = pyopenms.MSExperiment()
            pyopenms.FileHandler().loadExperiment(infile, exp)

            transition_exp_used = pyopenms.TargetedExperiment()

            do_continue = True
            if is_swath:
                do_continue = pyopenms.OpenSwathHelper().checkSwathMapAndSelectTransitions(exp, targeted, transition_exp_used, min_upper_edge_dist)
            else:
                transition_exp_used = targeted

            if do_continue:
                # set up extractor and run
                tmp_out = pyopenms.MSExperiment()
                extractor = pyopenms.ChromatogramExtractor()
                extractor.extractChromatograms(exp, tmp_out, targeted, extraction_window, ppm, trafo, rt_extraction_window, extraction_function)
                # add all chromatograms to the output
                for chrom in tmp_out.getChromatograms():
                    output.addChromatogram(chrom)

        dp = pyopenms.DataProcessing()
        pa = pyopenms.ProcessingAction().SMOOTHING
        dp.setProcessingActions(set([pa]))

        chromatograms = output.getChromatograms()
        for chrom in chromatograms:
            this_dp = chrom.getDataProcessing()
            this_dp.append(dp)
            chrom.setDataProcessing(this_dp)

        output.setChromatograms(chromatograms)

        return output