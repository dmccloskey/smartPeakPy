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

    def convert_to_row(self,feature, targ, run_id, keys, keys_subordinates, filename):
        """Convert Feature into a row for csv outpout

        Args
            feature (Feature): 
            targ (TraML): transition experiment
            run_id (str): id for the run
            keys ([byte]): list of Feature keys to extract
            keys_subordinates ([byte]): list of Feature subordinate keys to extract
            filename (str): name of the FeatureXML file

        Returns
            rows_O ([]): list of row values based on the header and keys
        """
        rows_O = []

        peptide_ref = feature.getMetaValue("PeptideRef")
        pep = targ.getPeptideByRef(peptide_ref)

        full_peptide_name = "NA"
        # if (pep.metaValueExists("full_peptide_name")):
        #     full_peptide_name = pep.getMetaValue("full_peptide_name")
        # # AttributeError: 'pyopenms.pyopenms.LightCompound' object has no attribute 'metaValueExists'

        decoy = "0"
        peptidetransitions = [t for t in targ.getTransitions() if t.getPeptideRef() == peptide_ref]
        # if len(peptidetransitions) > 0:
        #     if peptidetransitions[0].getDecoyTransitionType() == pyopenms.DecoyTransitionType().DECOY:
        #         decoy = "1"
        #     elif peptidetransitions[0].getDecoyTransitionType() == pyopenms.DecoyTransitionType().TARGET:
        #         decoy = "0"
        # # AttributeError: 'pyopenms.pyopenms.LightTransition' object has no attribute 'getDecoyTransitionType'

        protein_name = "NA"
        if len(pep.protein_refs) > 0:
            protein_name = pep.protein_refs[0]

        # fragment_annotation = "NA"
        # fragment = [t for t in peptidetransitions if t.getPrecursorMZ()==feature.getMetaValue("PrecursorMZ") and t.getProductMZ()==feature.getMetaValue("ProductMZ")]
        # if len(fragment) == 1:
        #     fragment_annotation = fragment[0].getName()
        # if (pep.metaValueExists("native_id")):
        #     fragment_annotation = feature.getMetaValue("native_id")

        header_row = [
            feature.getMetaValue("PeptideRef"),
            run_id,
            filename,
            feature.getRT(),
            feature.getUniqueId(),
            pep.sequence,
            full_peptide_name,
            pep.getChargeState(),
            # feature.getMetaValue("PrecursorMZ"),
            feature.getIntensity(),
            protein_name,
            decoy,
            # fragment_annotation,
            # feature.getMetaValue("ProductMZ")
        ]

        key_row = []
        for k in keys:
            value = feature.getMetaValue(k)
            if type(value)==type(''.encode('utf-8')):
                value = feature.getMetaValue(k).decode('utf-8')
            key_row.append(value)

        for subordinate in feature.getSubordinates():
            key_subordinate_row = []
            for k in keys_subordinates:
                value = subordinate.getMetaValue(k)
                if type(value)==type(''.encode('utf-8')):
                    value = subordinate.getMetaValue(k).decode('utf-8')
                key_subordinate_row.append(value)
            transition = [t for t in peptidetransitions if t.getNativeID()==subordinate.getMetaValue("native_id")][0]
            key_subordinate_row.append(transition.getPrecursorMZ()) #include quant, qual, detecting, identifying, etc.,
            key_subordinate_row.append(subordinate.getIntensity())
            rows_O.append(header_row + key_row + key_subordinate_row)

        return rows_O

    def get_header(self, features):
        """Get header columns from feature
        Args
            features (FeatureMap): FeatureMap object

        Returns
            header ([str]): List of header ids
            keys ([byte]): list of FeatureMap keys
        """
        # get feature keys
        keys = []
        features[0].getKeys(keys)
        keys.remove("PrecursorMZ".encode('utf-8')) #transition group precursorMZ is not the same for all transitions!
        # get subordinate keys
        keys_subordinates = []
        features[0].getSubordinates()[0].getKeys(keys_subordinates)
        # define the header
        header = [
            "transition_group_id",
            "run_id",
            "filename",
            "RT",
            "id",
            "Sequence",
            "FullPeptideName",
            "Charge",
            # "PrecursorMZ",
            "Intensity",
            "ProteinName",
            "decoy",
            # "Fragment_Annotation",
            # "ProductMZ"
        ]
        keys1 = [k.decode('utf-8') for k in keys]
        header.extend(keys1)
        keys_subordinates1 = [k.decode('utf-8') for k in keys_subordinates]
        header.extend(keys_subordinates1)
        header.extend(["PrecursorMZ","peak_area"]) #different percursorMZ for each transition
        return header,keys,keys_subordinates

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
        rows_O = []
        header,keys,keys_subordinates = self.get_header(features)
        for feature in features:
            rows = self.convert_to_row(feature, targ, run_id, keys, keys_subordinates, filename)
            for row in rows:
                rows_O.append(dict(zip(header,row)))
        return header,rows_O

    def store(self, filename_O, output, targeted, run_id = 'run0', filename = 'run0.FeatureXML'):
        """Writes a featureXML to a mProphet tsv
        """
        # convert to dicts
        header,rows = self.convert_FeatureXMLToTSV(output, targeted, run_id = run_id, filename = filename)

        # write dict to csv
        with open(filename_O, 'w',newline='') as f:
            writer = csv.DictWriter(f, fieldnames = header)
            try:
                writer.writeheader()
                writer.writerows(rows)
            except csv.Error as e:
                sys.exit(e)