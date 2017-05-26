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
            output (dict): dictionary of chromatograms where the key=nativeID
        """
        pass

    def getTransitionGroup(self, chromatogram_mapped, targeted):
        """Create a dictionary map between the nativeID for the mapped chromatogram (mzML) and transitions (TraML)
        
        Args:
            chromatogram_map (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions

        Returns:
            output (dict): dictionary of chromatograms where the key=nativeID
        """
        pass

    def allAssaysHaveChromatograms(self, chromatogram_mapped, targeted):
        """Create a dictionary map between the nativeID for the mapped chromatogram (mzML) and transitions (TraML)
        
        Args:
            chromatogram_map (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions

        Returns:
            output (dict): dictionary of chromatograms where the key=nativeID
        """
        pass