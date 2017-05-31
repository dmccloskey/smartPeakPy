
import copy, sys
try:
    import pyopenms
except ImportError as e:
    print(e)

class MRMTransitionGroupPicker():
    """
    Source: Hannes Röst
    """

    def getTransitionGroup(self, exp, targeted, key, trgr_ids, chrom_map):
        """Create a dictionary map between the nativeID for the mapped chromatogram (mzML) and transitions (TraML)
        
        Args:
            exp (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions
            key (int)
            trgr_ids
            chrom_map 

        Returns:
            transition_group (MRMTransitionGroupCP): 
        """
        # transition_group = pyopenms.MRMTransitionGroupCP()
        transition_group = pyopenms.LightMRMTransitionGroupCP()
        for tr in trgr_ids:
            transition = targeted.getTransitions()[tr]
            chrom_idx = chrom_map[ transition.getNativeID() ]
            chrom = exp.getChromatograms()[ chrom_idx ]
            chrom.setMetaValue("product_mz", transition.getProductMZ() )
            chrom.setMetaValue("precursor_mz", transition.getPrecursorMZ() )
            transition_group.addTransition( transition, transition.getNativeID() )
            transition_group.addChromatogram( chrom, chrom.getNativeID() )
        return transition_group

    def doMap(self,exp, targeted):
        """Create a dictionary map between the nativeID for the mapped chromatogram (mzML) and transitions (TraML)
        
        Args:
            exp (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions

        Returns:
            chrom_map (dict): dictionary of chromatograms where the key=nativeID
            trmap (dict): dictionary of transitions where the key=nativeID
            pepmap
        """

        chrom_map = {}
        pepmap = {}
        trmap = {}
        for i, chrom in enumerate(exp.getChromatograms()):
            chrom_map[ chrom.getNativeID() ] = i
        # for i, pep in enumerate(targeted.getPeptides() ):
        #     pepmap[ pep.id ] = i
        #AttributeError: 'pyopenms.pyopenms.LightTargetedExperiment' object has no attribute 'getPeptides'
        for i, tr in enumerate(targeted.getTransitions() ):
            tmp = trmap.get( tr.getPeptideRef() , [])
            tmp.append( i )
            trmap[ tr.getPeptideRef() ] = tmp

        return chrom_map,trmap,pepmap


    def pickTransitionGroups(self, exp, targeted, picker):
        """

        Args
            exp (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions
            picker (MRMTransitionGroupPicker): transition group picker

        Returns
            output (FeatureMap): map of MRMFeatures and subordinate features
            
        """
        # output = pyopenms.FeatureMap()
        output = []

        chrom_map,trmap,pepmap = self.doMap(exp, targeted)

        for key, value in trmap.items():
            print(key, value)
            transition_group = self.getTransitionGroup(exp, targeted, key, value, chrom_map)
            picker.pickTransitionGroup(transition_group)
            for mrmfeature in transition_group.getFeatures():
                features = mrmfeature.getFeatures()
                for f in features:
                    # TODO
                    # f.getConvexHulls().clear()
                    f.ensureUniqueId()

                # TODO 
                # mrmfeature.setSubordinates(features) # add all the subfeatures as subordinates
                output.append(mrmfeature)

        return output

    def pickExperiment(self, exp, targeted, picker, feature_finder,
        trafo, swath_maps, output, ms1only = False):
        """

        Args
            exp (MSExperiment): chromatograms
            targeted (TraML): TraML input file containt the transitions
            picker (MRMTransitionGroupPicker): transition group picker
            feature_finder (MRMFeatureFinderScoring): feature finder and scorer

        Returns
            output (FeatureMap): map of MRMFeatures and subordinate features
            
        """
        #output = pyopenms.FeatureMap()

        chrom_map,trmap,pepmap = self.doMap(exp, targeted)

        for key, value in trmap.items():
            print(key, value)
            transition_group = self.getTransitionGroup(exp, targeted, key, value, chrom_map)
            picker.pickTransitionGroup(transition_group)
            feature_finder.scorePeakgroups(transition_group,trafo,swath_maps,output,ms1only)
            #TypeError: Argument 'swath_maps' has incorrect type (expected list, got pyopenms.pyopenms.MSExperiment)

        return output

    def main(self,options):
        out = options.outfile
        chromat_in = options.infile
        traml_in = options.traml_in

        pp = pyopenms.MRMTransitionGroupPicker()
        chromatograms = pyopenms.MSExperiment()
        fh = pyopenms.FileHandler()
        fh.loadExperiment(chromat_in, chromatograms)
        targeted = pyopenms.TargetedExperiment();
        tramlfile = pyopenms.TraMLFile();
        tramlfile.load(traml_in, targeted);
        
        output = algorithm(chromatograms, targeted, pp)

