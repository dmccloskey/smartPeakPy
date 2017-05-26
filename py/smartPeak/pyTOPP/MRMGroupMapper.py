import copy, sys
try:
    import pyopenms
except ImportError as e:
    print(e)

class MRMGroupMapper():
    """MRMGroupMapper maps measured chromatograms (mzML) and the transitions used (TraML)
    and stores them in a MRMTransitionGroup structure

    Source:
        https://github.com/OpenMS/OpenMS/blob/9151aa9addbea5e257cb77c14b0ac4dc63ad89c3/src/utils/MRMTransitionGroupPicker.cpp
    """

    def doMap(self, chromatogram_mapped, targeted):
        """Create a dictionary map between the nativeID for the mapped chromatogram (mzML) and transitions (TraML)
        
        Args:
            chromatogram_map (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions

        Returns:
            chromatogram_mapped_dict (dict): dictionary of chromatograms where the key=nativeID
            targeted_mapped_dict (dict): dictionary of transitions where the key=nativeID
        """
        chromatogram_mapped_dict = {d.getNativeID():d for d in chromatogram_mapped.getChromatograms()}
        targeted_mapped_dict = {d.getNativeID():d for d in targeted.getTransitions()}
        return chromatogram_mapped_dict,targeted_mapped_dict

    def getTransitionGroup(self, chromatogram_mapped_dict, targeted_dict):
        """Create a dictionary map between the nativeID for the mapped chromatogram (mzML) and transitions (TraML)
        
        Args:
            chromatogram_map (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions

        Returns:
            output (MRMTransitionGroup): 
        """
        output = pyopenms.MRMTransitionGroup()
        if len(targeted_dict.keys())<len(chromatogram_mapped_dict.keys()):
            trans_iter = targeted_dict
        else:
            trans_iter = chromatogram_mapped_dict
        for id in list(trans_iter.keys()):
            # output.addChromatogram(chromatogram_mapped_dict[id],id)
            spectrum = pyopenms.MSSpectrum()
            for peak in chromatogram_mapped_dict[id]:
                spectrum.push_back(peak)
            output.addChromatogram(spectrum,id)
            output.addTransition(targeted_dict[id],id)
        return output

    def allAssaysHaveChromatograms(self):
        """
        
        Args:

        Returns:
            output (bool): True if...
        """
        pass

    def main(self,chromatogram_mapped, targeted):
        """
        
        Args:
            chromatogram_map (MSExperiment): chromatograms
            targeted (TraML): TraML input file containing the transitions

        Returns:
            chromatogram_mapped_dict (dict): dictionary of chromatograms where the key=nativeID
            targeted_mapped_dict (dict): dictionary of transitions where the key=nativeID
        """
        chromatogram_mapped_dict, targeted_dict = self.doMap(chromatogram_mapped, targeted)
        output = self.getTransitionGroup(chromatogram_mapped_dict, targeted_dict)
        return output