import os,sys
try:
    import pyopenms
except ImportError as e:
    print(e)

class OpenSwathRTNormalizer():
    """The OpenSwathRTNormalizer will find retention time peptides in data.

    This tool will take a description of RT peptides and their normalized retention time to write out a transformation file on how to transoform the RT space into the normalized space.

    Source:
        https://github.com/sneumann/OpenMS/blob/master/pyOpenMS/pyTOPP/OpenSwathRTNormalizer.py
        http://ftp.mi.fu-berlin.de/pub/OpenMS/release-documentation/html/TOPP_OpenSwathRTNormalizer.html
     """

    def simple_find_best_feature(self, output, pairs, targeted):
        """
        """
        f_map = {}
        for f in output:
            key = f.getMetaValue("PeptideRef")
            if key in f_map.keys():
                f_map[key].append(f)
            else: 
                f_map[key] = [f]
        
        
        for v in f_map.values():
            bestscore = -10000
            for feature in v:
                score = feature.getMetaValue("main_var_xx_lda_prelim_score")
                if score > bestscore:
                    best = feature
                    bestscore = score
            
            pep = targeted.getPeptideByRef( feature.getMetaValue("PeptideRef")  )
            pairs.append( [best.getRT(), pep.getRetentionTime() ] )

    def extract_features(self, output, pairs, targeted):
        """
        TODO
        """
        pass

    def make_retentionTimePairs(
        self, chromatograms, targeted,
        estimateBestPeptides=True,
        min_rsq=0.95,
        min_coverage=0.6,
        use_chauvenet=True,
        outlier_method="iter_residual",
        max_iterations=1,
        max_rt_threshold=1,
        sampling_size=1,
        MRMFeatureFinderScoring_params=None
        ):
        """make the retention time pairs required for the transformation model
        from the MSExperiment actual retention times
        and TraML normalized retention times

        algorithm used in OpenSWATHRTNormalizer

        Args:
            chromatograms (MSExperiment): chromatograms
            targeted (TraML): TraML input file containing the transitions
            #targeted_norm (TraML): TraML input file containing the normalized transitions
            estimateBestPeptides (bool): Whether the algorithms should try to choose the best peptides based on their peak 
                            shape for normalization. Use this option you do not expect all your peptides to be
                            detected in a sample and too many 'bad' peptides enter the outlier removal step
                            (e.g. due to them being endogenous peptides or using a less curated list of peptide
                            s).
            outlier_method (string): Outlier detection method ("iter_jackknife", "iter_residual", "ransac")
                "iter_jackknife" or "iter_residual" Args:
                    min_rsq (float): Minimum r-squared of RT peptides regression (default: '0.95')
                    min_coverage (float): Minimum relative amount of RT peptides to keep (default: '0.6')
                    use_chauvenet (bool): Whether to only remove outliers that fulfill Chauvenet's criterion for outliers 
                        (otherwise it will remove any outlier candidate regardless of the criterion)
                "ransac" Args:
                    max_iterations (int): Maximum iterations for the RANSAC algorithm
                    max_rt_threshold (float): Maximum deviation from fit for the retention time.
                        This must be in the unit of the second dimension (e.g. theoretical_rt).
                    sampling_size (float): The number of data points to sample for the RANSAC algorithm.
            MRMFeatureFinderScoring_params (Param): Param object for MRMFeatureFinderScoring 

        Returns:
            pairs_corrected (list([,])): list of ["rt","rt_norm"]
        
        """
        # Create empty files as input and finally as output
        empty_swath = pyopenms.MSExperiment()
        trafo = pyopenms.TransformationDescription()
        output = pyopenms.FeatureMap()

        # set up featurefinder and run
        featurefinder = pyopenms.MRMFeatureFinderScoring()
        # set the correct rt use values
        # TODO: update parameters (no peaks are found!)
        if MRMFeatureFinderScoring_params and not MRMFeatureFinderScoring_params is None:
            MRMFeatureFinderScoring_params.setValue("Scores:use_rt_score".encode("utf-8"),'false'.encode("utf-8"),''.encode("utf-8"))
            MRMFeatureFinderScoring_params.setValue("Scores:use_elution_model_score".encode("utf-8"),'false'.encode("utf-8"),''.encode("utf-8"))
            featurefinder.setParameters(MRMFeatureFinderScoring_params)
        else:
            scoring_params = pyopenms.MRMFeatureFinderScoring().getDefaults()
            scoring_params.setValue("Scores:use_rt_score".encode("utf-8"),'false'.encode("utf-8"),''.encode("utf-8"))
            scoring_params.setValue("Scores:use_elution_model_score".encode("utf-8"),'false'.encode("utf-8"),''.encode("utf-8"))
            featurefinder.setParameters(scoring_params)
        featurefinder.pickExperiment(chromatograms, output, targeted, trafo, empty_swath)

        # get the pairs
        pairs=[]
        if estimateBestPeptides:
            self.simple_find_best_feature(output, pairs, targeted)
        else:
            self.extract_features(output, pairs, targeted)
        if outlier_method == "iter_jackknife" or outlier_method == "iter_residual":
            pairs_corrected = pyopenms.MRMRTNormalizer().removeOutliersIterative( pairs, min_rsq, min_coverage, use_chauvenet, outlier_method) 
            pairs = [ list(p) for p in pairs_corrected] 
        elif outlier_method == "ransac":
            #TODO: estimate defaults for parameters
            #https://github.com/OpenMS/OpenMS/blob/cfcf9ff09613191aa3502dbf5c6df9a613379376/src/topp/OpenSwathRTNormalizer.cpp
            pairs_corrected = pyopenms.MRMRTNormalizer().removeOutliersIterremoveOutliersRANSACative( pairs, min_rsq, min_coverage, 
                max_iterations,
                max_rt_threshold,
                sampling_size) 
            pairs = [ list(p) for p in pairs_corrected] 

        return pairs

    def make_transformation(
        self, 
        pairs,
        model_params=None,
        model_type="lowess"
        ):
        """make the transformation model

        Args:
            pairs (list([,])): list of ["rt","rt_norm"]
            model_params (Param): pyopenms.Param object
                linear:
                    "slope" (float)
                    "intercept" (float)
                    "symmetric_regression" (bool)
                b-spline:
                    "boundary_condition" (size)
                    "wavelength" (float)
                    "num_nodes" (int)
                    "extrapolate" ("b_spline" or "global_linear")
                interpolated:
                    "interpolation_type" ("linear", "cspline", "akima")
                    "extrapolation_type" ("global-linear", "two-point-linear", "four-point-linear")
                lowess:
                    "span" (float)
                    "num_iterations" (int)
                    "delta" (float)
                    "interpolation_type" ("linear", "cspline", "akima")
                    "extrapolation_type" ("global-linear", "two-point-linear", "four-point-linear")
            model_type (str): The following models are available:
                none (TransformationModel): $ f(x) = x $ (identity)
                identity: Same as none, but intended for reference files (used to indicate that no other model should be fit, because the identity is already optimal).
                linear (TransformationModelLinear): $ f(x) = slope * x + intercept $
                interpolated (TransformationModelInterpolated): Interpolation between pairs, extrapolation using first and last pair. Supports different interpolation types.
                b-spline (TransformationModelBSpline): Non-linear smoothing spline, with different options for extrapolation.
                lowess (TransformationModelLowess): Non-linear smoothing via local regression, with different options for extrapolation.

        Returns:
            trafo_out (TransformationDescription): 
        
        """
        # store transformation
        trafo_out = pyopenms.TransformationDescription()
        trafo_out.setDataPoints(pairs)
        if not model_params or model_params is None:
            model_params = pyopenms.Param()
            model_params.setValue("symmetric_regression", 'false', '')
        if not model_type or model_type is None:
            model_type = "linear"
        trafo_out.fitModel(model_type, model_params)
        return trafo_out

    def main(self,
        chromatograms,
        targeted,
        #targeted_norm,
        model_params=None,
        model_type="lowess",
        estimateBestPeptides=True,
        min_rsq=0.95,
        min_coverage=0.6,
        removeOutlierPeptides=True,
        MRMFeatureFinderScoring_params=None
        ):
        """generalized RTNormalization

        Args:

        Returns:

        Source:
        """

        rt_pairs = self.make_retentionTimePairs(
            chromatograms=chromatograms,
            targeted=targeted,
            MRMFeatureFinderScoring_params=MRMFeatureFinderScoring_params,
            min_rsq=min_rsq,
            min_coverage=min_coverage,
            estimateBestPeptides=estimateBestPeptides,
            removeOutlierPeptides=removeOutlierPeptides
        )
        trafo_out = make_transformation( 
            pairs,
            model_params=model_params,
            model_type=model_type
        )

    def store_TransformationXMLFile(self,outfile,trafo_out):

        pyopenms.TransformationXMLFile().store(outfile, trafo_out)