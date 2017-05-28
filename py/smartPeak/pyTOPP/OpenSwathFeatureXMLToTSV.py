import csv, sys
try:
    import pyopenms
except ImportError as e:
    print(e)

class OpenSwathFeatureXMLToTSV():
    """Converts a featureXML to a mProphet tsv

    Source:
        https://github.com/sneumann/OpenMS/blob/master/pyOpenMS/pyTOPP/OpenSwathFeatureXMLToTSV.py
     """

    def convert_to_row(self,feature, targ, run_id, keys, filename):
        peptide_ref = feature.getMetaValue("PeptideRef")
        pep = targ.getPeptideByRef(peptide_ref)
        full_peptide_name = "NA"
        if (pep.metaValueExists("full_peptide_name")):
            full_peptide_name = pep.getMetaValue("full_peptide_name")

        decoy = "0"
        peptidetransitions = [t for t in targ.getTransitions() if t.getPeptideRef() == peptide_ref]
        if len(peptidetransitions) > 0:
            if peptidetransitions[0].getDecoyTransitionType() == pyopenms.DecoyTransitionType().DECOY:
                decoy = "1"
            elif peptidetransitions[0].getDecoyTransitionType() == pyopenms.DecoyTransitionType().TARGET:
                decoy = "0"

        protein_name = "NA"
        if len(pep.protein_refs) > 0:
            protein_name = pep.protein_refs[0]

        row = [
            feature.getMetaValue("PeptideRef"),
            run_id,
            filename,
            feature.getRT(),
            feature.getMetaValue("PrecursorMZ"),
            feature.getUniqueId(),
            pep.sequence,
            full_peptide_name,
            pep.getChargeState(),
            feature.getMetaValue("PrecursorMZ"),
            feature.getIntensity(),
            protein_name,
            decoy
        ]

        for k in keys:
            row.append(feature.getMetaValue(k))

        return row

    def get_header(self, features):
        keys = []
        features[0].getKeys(keys)
        header = [
            "transition_group_id",
            "run_id",
            "filename",
            "RT",
            "id",
            "Sequence" ,
            "FullPeptideName",
            "Charge",
            "m/z",
            "Intensity",
            "ProteinName",
            "decoy"]
        header.extend([k.decode('utf-8') for k in keys])
        return header

    def convert_FeatureXMLToTSV(self, features, targ, run_id = 'run0', filename = 'run0.FeatureXML'):
        """Converts a featureXML to a mProphet tsv

        Args:
            features (list(Feature)): list of Features
            targ (TraML): transition list in targetedExperiment
            run_id (str): id for the run
            filename (str): filename of the original FeatureXML file

        Returns:
            rows (list(dict())): list of rows for csv output
        
        """
        rows = []
        header = self.get_header(features)
        for feature in features:
            row = self.convert_to_row(feature, targ, run_id, header, filename)
            rows.append(dict(zip(header,row)))
        return header,rows

    def store(self, filename_O, output, targeted, run_id = 'run0', filename = 'run0.FeatureXML'):
        """Writes a featureXML to a mProphet tsv
        """
        # convert to dicts
        header,rows = self.convert_FeatureXMLToTSV(output, targeted, run_id = run_id, filename = filename)

        # write dict to csv
        with open(filename, 'w',newline='') as f:
            writer = csv.DictWriter(f, fieldnames = header)
            try:
                writer.writeheader()
                writer.writerows(rows)
            except csv.Error as e:
                sys.exit(e)