import copy, sys
try:
    import pyopenms
except ImportError as e:
    print(e)

class MRMMapper():
    """MRMMapper maps measured chromatograms (mzML) and the transitions used (TraML)

    Source:
        https://github.com/sneumann/OpenMS/blob/master/pyOpenMS/pyTOPP/MRMMapper.py
    """

    def algorithm(self, chromatogram_map, targeted, 
    precursor_tolerance=0.1, product_tolerance=0.1, 
    allow_unmapped=True, allow_double_mappings=False):
        """
        Args:
            chromatogram_map (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions
            precursor_tolerance (float): default=0.1, Precursor tolerance when mapping (in Th)
            product_tolerance (float): default=0.1, Product tolerance when mapping (in Th)

        Returns:
            output (): mapped chromatograms
        """

        output = copy.copy(chromatogram_map)
        output.clear(False); 
        empty_chromats = []
        output.setChromatograms(empty_chromats)

        notmapped = 0
        for chrom in chromatogram_map.getChromatograms():
            mapped_already = False
            for transition in targeted.getTransitions():
                if (abs(chrom.getPrecursor().getMZ() - transition.getPrecursorMZ()) < precursor_tolerance and
                    abs(chrom.getProduct().getMZ()  -  transition.getProductMZ()) < product_tolerance):
                    if mapped_already:
                        this_peptide = targeted.getPeptideByRef(transition.getPeptideRef() ).sequence
                        other_peptide = chrom.getPrecursor().getMetaValue("peptide_sequence")
                        print("Found mapping of " + str(chrom.getPrecursor().getMZ()) + "/" + str(chrom.getProduct().getMZ()) + " to " + str(transition.getPrecursorMZ()) + "/" + str(transition.getProductMZ()))
                        print("Of peptide " + this_peptide.decode("utf-8"))
                        print("But the chromatogram is already mapped to " + other_peptide.decode("utf-8"))
                        if not allow_double_mappings: raise Exception("Cannot map twice")
                    mapped_already = True
                    precursor = chrom.getPrecursor()
                    peptide = targeted.getPeptideByRef(transition.getPeptideRef() )
                    precursor.setMetaValue("peptide_sequence", peptide.sequence)
                    chrom.setPrecursor(precursor)
                    chrom.setNativeID(transition.getNativeID())
            if not mapped_already:
                notmapped += 1
                print("Did not find a mapping for chromatogram " + chrom.getNativeID().decode("utf-8"))
                if not allow_unmapped: raise Exception("No mapping")
            else:
                output.addChromatogram(chrom)

        if notmapped > 0:
            print("Could not find mapping for " + str(notmapped) + " chromatogram(s)")


        dp = pyopenms.DataProcessing()
        # dp.setProcessingActions(ProcessingAction:::FORMAT_CONVERSION)
        pa = pyopenms.ProcessingAction().FORMAT_CONVERSION
        dp.setProcessingActions(set([pa]))

        chromatograms = output.getChromatograms()
        for chrom in chromatograms:
            this_dp = chrom.getDataProcessing()
            this_dp.append(dp)
            chrom.setDataProcessing(this_dp)

        output.setChromatograms(chromatograms)
        return output

    def main(self, infile, traml_in, targeted, 
    precursor_tolerance=0.1, product_tolerance=0.1, 
    allow_unmapped=True, allow_double_mappings=False):
        """
        Args:
            infile (): An input file containing chromatograms
            traml_in (): TraML input file containt the transitions
            outfile (): Output file with annotated chromatograms
            precursor_tolerance (float): default=0.1, Precursor tolerance when mapping (in Th)
            product_tolerance (float): default=0.1, Product tolerance when mapping (in Th)

        Returns:
            output (): mapped chromatograms
        """

        ff = pyopenms.MRMFeatureFinderScoring()
        chromatogram_map = pyopenms.MSExperiment()
        fh = pyopenms.FileHandler()
        fh.loadExperiment(infile, chromatogram_map)
        targeted = pyopenms.TargetedExperiment()
        tramlfile = pyopenms.TraMLFile()
        tramlfile.load(traml_in, targeted)
        
        output = self.algorithm(chromatogram_map, targeted, precursor_tolerance, product_tolerance)
        return output