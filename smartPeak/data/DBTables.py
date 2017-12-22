# -*- coding: utf-8 -*-
from .DBTableInterface import DBTableInterface
from .DBConnection import DBConnection
import copy


class DBTables():

    def __init__(self):
        self.sequence_file = None
        self.traml = None
        self.feature_filter = None
        self.feature_qc = None
        self.features = None
        self.quant_methods = None
        self.standards_concs = None
        self.undolog = None

    def set_tables(self, settings):
        """DB table for the sequence file format"""

        self.sequence_file = DBTableInterface(    
            settings["database"]["dialect"],
            "sequence_file",
            None,
            ["sample_name", "sample_type",
                "comments", "acquisition_method", "processing_method",
                "rack_code", "plate_code", "vial_position", "rack_position",
                "plate_position", "injection_volume", "dilution_factor", 
                "weight_to_volume", "set_name", "filename"],
            ["TEXT", "TEXT",
                "TEXT", "TEXT", "TEXT",
                "INTEGER", "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "REAL", "REAL",
                "REAL", "TEXT", "TEXT"],
            None,
            None
        )

        # TODO
        self.traml = DBTableInterface(    
            settings["database"]["dialect"],
            "traml",
            None,
            ["sample_name", "sample_type",
                "comments", "acquisition_method", "processing_method",
                "rack_code", "plate_code", "vial_position", "rack_position",
                "plate_position", "injection_volume", "dilution_factor", 
                "weight_to_volume", "set_name", "filename"],
            ["TEXT", "TEXT",
                "TEXT", "TEXT", "TEXT",
                "INTEGER", "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "REAL", "REAL",
                "REAL", "TEXT", "TEXT"],
            None,
            None
        )

        # TODO add in all metaValues
        self.feature_filter = DBTableInterface(    
            settings["database"]["dialect"],
            "feature_filter",
            None,
            ["component_name", "component_group_name",
                "n_heavy_l ", "n_heavy_u", "n_light_l", "n_light_u",
                "n_detecting_l", "n_detecting_u", "n_quantifying_l",
                "n_quantifying_u", "n_identifying_l", "n_identifying_u",
                "n_transitions_l", "n_transitions_u", "ion_ratio_pair_name_1",
                "ion_ratio_pair_name_2", "ion_ratio_l", "ion_ratio_u",
                "retention_time_l", "retention_time_u",
                "intensity_l", "intensity_u", "overall_quality_l", "overall_quality_u",
                "metaValue_peak_apex_int_l", "metaValue_peak_apex_int_u", 
                "metaValue_logSN_l", "metaValue_logSN_u",
                "metaValue_var_xcorr_coelution_l", "metaValue_var_xcorr_coelution_u",
                "metaValue_var_xcorr_coelution_weighted_l", 
                "metaValue_var_xcorr_coelution_weighted_u",
                "metaValue_var_xcorr_shape_l", "metaValue_var_xcorr_shape_u",
                "metaValue_var_xcorr_shape_weighted_l", 
                "metaValue_var_xcorr_shape_weighted_u"],
            ["TEXT", "TEXT",
                "INTEGER", "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "TEXT",
                "TEXT", "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL", "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL"],
            None,
            None
        )

        self.feature_qc = copy.copy(self.feature_filter)

        # TODO
        self.features = DBTableInterface(    
            settings["database"]["dialect"],
            "features",
            None,
            ["transition_group_id", "run_id", "filename", "RT", "id", 
                "Sequence", "FullPeptideName", "Charge", "Intensity", 
                "ProteinName", "decoy", "potentialOutlier", 
                "initialPeakQuality", "PeptideRef", "leftWidth", 
                "rightWidth", "total_xic", "peak_apices_sum", 
                "var_xcorr_coelution", "var_xcorr_coelution_weighted", 
                "var_xcorr_shape", "var_xcorr_shape_weighted", "delta_rt", 
                "assay_rt", "norm_RT", "rt_score", "var_norm_rt_score", 
                "var_intensity_score", "nr_peaks", "sn_ratio", 
                "var_log_sn_score", "var_elution_model_fit_score", 
                "main_var_xx_lda_prelim_score", "QC_transition_group_pass", 
                "QC_transition_group_message", "MZ", "native_id", 
                "peak_apex_int", "width_at_5", "width_at_10", "width_at_50", 
                "start_time_at_10", "start_time_at_5", "end_time_at_10", 
                "end_time_at_5", "total_width", "tailing_factor", "asymmetry_factor", 
                "baseline_delta_2_height", "slope_of_baseline", "points_across_baseline", 
                "points_across_half_height", "logSN", "FeatureLevel", 
                "calculated_concentration", "concentration_units", "QC_transition_pass", 
                "QC_transition_message", "PrecursorMZ", "peak_area"],
            ["TEXT"],
            None,
            None
        )

        self.quant_methods = DBTableInterface(    
            settings["database"]["dialect"],
            "quant_methods",
            None,
            ["IS_name", "component_name", "feature_name", "concentration_units", 
                "llod", "ulod", "lloq", "uloq", "correlation_coefficient", 
                "n_points", "transformation_model", 
                "transformation_model_param_slope", 
                "transformation_model_param_intercept", 
                "transformation_model_param_x_weight", 
                "transformation_model_param_y_weight", 
                "transformation_model_param_x_datum_min", 
                "transformation_model_param_x_datum_max", 
                "transformation_model_param_y_datum_min", 
                "transformation_model_param_y_datum_max"],
            ["TEXT", "TEXT", "TEXT", "TEXT", 
                "REAL", "REAL", "REAL", "REAL", "REAL", 
                "n_points", "TEXT", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL"],
            None,
            None
        )

        # TODO: update row names in OpenMS
        self.standards_concs = DBTableInterface(    
            settings["database"]["dialect"],
            "standards_concs",
            None,
            ["run_id", "component_id", "IS_component_id", "actual_concentration", 
                "IS_actual_concentration", "concentration_units", "dilution_factor"],
            ["TEXT", "TEXT", "TEXT", "REAL", 
                "REAL", "TEXT", "REAL"],
            None,
            None
        )

        self.undolog = DBTableInterface(    
            settings["database"]["dialect"],
            "undolog",
            None,
            ["history"],
            ["TEXT"],
            None,
            None
        )

    def connect_tables(self, settings):
        """Connect all DB tables"""

        db_connection = DBConnection()
        db_connection.set_conn(settings['database'])
        conn = db_connection.get_conn()
        db_connection.set_cursor(settings['database'])
        cursor = db_connection.get_cursor()

        self.sequence_file.set_conn(conn)
        self.traml.set_conn(conn)
        self.feature_filter.set_conn(conn)
        self.feature_qc.set_conn(conn)
        self.features.set_conn(conn)
        self.quant_methods.set_conn(conn)
        self.standards_concs.set_conn(conn)

        self.sequence_file.set_cursor(cursor)
        self.traml.set_cursor(cursor)
        self.feature_filter.set_cursor(cursor)
        self.feature_qc.set_cursor(cursor)
        self.features.set_cursor(cursor)
        self.quant_methods.set_cursor(cursor)
        self.standards_concs.set_cursor(cursor)
    
    def create_tables(self):
        """Create all tables"""      

        self.sequence_file.create_table()
        self.traml.create_table()
        self.feature_filter.create_table()
        self.feature_qc.create_table()
        self.features.create_table()
        self.quant_methods.create_table()
        self.standards_concs.create_table()
    
    def drop_tables(self):
        """Drop all tables"""      

        self.sequence_file.drop_table()()
        self.traml.drop_table()()
        self.feature_filter.drop_table()()
        self.feature_qc.drop_table()()
        self.features.drop_table()()
        self.quant_methods.drop_table()()
        self.standards_concs.drop_table()()
