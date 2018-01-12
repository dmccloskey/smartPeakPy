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
        self.feature_maps = None
        self.quantitation_methods = None
        self.standards_concentrations = None
        self.algorithm_parameters = None
        self.transaction_log = None

    def get_table(self, table_name):
        """Return the DBTable object for the specified table

        Args:
            table_name (str): name of the table

        Returns:
            DBTableInterface

        """
        table = None
        if table_name == "sequence_file":
            table = self.sequence_file
        elif table_name == "traml":
            table = self.traml
        elif table_name == "feature_filter":
            table = self.feature_filter
        elif table_name == "feature_qc":
            table = self.feature_qc
        elif table_name == "feature_maps":
            table = self.feature_maps
        elif table_name == "quantitation_methods":
            table = self.quantitation_methods
        elif table_name == "standards_concentrations":
            table = self.standards_concentrations
        elif table_name == "algorithm_parameters":
            table = self.algorithm_parameters
        elif table_name == "transaction_log":
            table = self.transaction_log
        else:
            print("Table " + table_name + " is not a valid table.")
        return table

    def set_tables(self, settings):
        """DB table for the sequence file format"""

        self.sequence_file = DBTableInterface(    
            settings["database"]["dialect"],
            "sequence_file",
            None,
            ["sequence_id", "sequence_group_name", "sample_name",
                "sample_group_name", "sample_type", "filename",
                "used_"],
            ["TEXT", "TEXT", "TEXT",
                "TEXT", "TEXT", "TEXT",
                "INTEGER"],
            ["sequence_file_unique"],
            ["UNIQUE(sequence_id, sample_name, filename)"]
        )

        self.traml = DBTableInterface(    
            settings["database"]["dialect"],
            "traml",
            None,
            ["traml_id", "component_name", "component_group_name", "traml_data", 
                "used_"],
            ["TEXT", "TEXT", "TEXT", "TEXT",
                "INTEGER"],
            ["traml_unique"],
            ["UNIQUE(traml_id, component_name)"]
        )

        # NOTE: alternative: add in all metavalues
        self.feature_filter = DBTableInterface(    
            settings["database"]["dialect"],
            "feature_filter",
            None,
            ["ff_id", "component_name", "component_group_name",
                "n_heavy_l ", "n_heavy_u", "n_light_l", "n_light_u",
                "n_detecting_l", "n_detecting_u", "n_quantifying_l",
                "n_quantifying_u", "n_identifying_l", "n_identifying_u",
                "n_transitions_l", "n_transitions_u", "ion_ratio_pair_name_1",
                "ion_ratio_pair_name_2", "ion_ratio_l", "ion_ratio_u",
                "retention_time_l", "retention_time_u",
                "intensity_l", "intensity_u", "overall_quality_l", "overall_quality_u",
                "metaValue_limits",
                "used_"],
            ["TEXT", "TEXT", "TEXT",
                "INTEGER", "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "TEXT",
                "TEXT", "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL", "REAL", "REAL",
                "TEXT",
                "INTEGER"],
            ["feature_filter_unique"],
            ["UNIQUE(ff_id, component_name)"]
        )

        self.feature_qc = DBTableInterface(    
            settings["database"]["dialect"],
            "feature_qc",
            None,
            ["fqc_id", "component_name", "component_group_name",
                "n_heavy_l ", "n_heavy_u", "n_light_l", "n_light_u",
                "n_detecting_l", "n_detecting_u", "n_quantifying_l",
                "n_quantifying_u", "n_identifying_l", "n_identifying_u",
                "n_transitions_l", "n_transitions_u", "ion_ratio_pair_name_1",
                "ion_ratio_pair_name_2", "ion_ratio_l", "ion_ratio_u",
                "retention_time_l", "retention_time_u",
                "intensity_l", "intensity_u", "overall_quality_l", "overall_quality_u",
                "metaValue_limits",
                "used_"],
            ["TEXT", "TEXT", "TEXT",
                "INTEGER", "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "INTEGER",
                "INTEGER", "INTEGER", "TEXT",
                "TEXT", "REAL", "REAL",
                "REAL", "REAL",
                "REAL", "REAL", "REAL", "REAL",
                "TEXT",
                "INTEGER"],
            ["feature_qc_unique"],
            ["UNIQUE(fqc_id, component_name)"]
        )

        self.feature_maps = DBTableInterface(    
            settings["database"]["dialect"],
            "feature_maps",
            None,
            ["feature_map_id", "sample_name", "component_name", "component_group_name",
                "feature_data", "subordinate_data",
                "used_"],
                # "transition_group_id", "run_id", "filename", "RT", "id", 
                # "Sequence", "FullPeptideName", "Charge", "Intensity", 
                # "ProteinName", "decoy", "potentialOutlier", 
                # "initialPeakQuality", "PeptideRef", "leftWidth", 
                # "rightWidth", "total_xic", "peak_apices_sum", 
                # "var_xcorr_coelution", "var_xcorr_coelution_weighted", 
                # "var_xcorr_shape", "var_xcorr_shape_weighted", "delta_rt", 
                # "assay_rt", "norm_RT", "rt_score", "var_norm_rt_score", 
                # "var_intensity_score", "nr_peaks", "sn_ratio", 
                # "var_log_sn_score", "var_elution_model_fit_score", 
                # "main_var_xx_lda_prelim_score", "QC_transition_group_pass", 
                # "QC_transition_group_message", "MZ", "native_id", 
                # "peak_apex_int", "width_at_5", "width_at_10", "width_at_50", 
                # "start_time_at_10", "start_time_at_5", "end_time_at_10", 
                # "end_time_at_5", "total_width", "tailing_factor", "asymmetry_factor", 
                # "baseline_delta_2_height", "slope_of_baseline", "points_across_baseline", 
                # "points_across_half_height", "logSN", "FeatureLevel", 
                # "calculated_concentration", "concentration_units", "QC_transition_pass", 
                # "QC_transition_message", "PrecursorMZ", "peak_area"],
            ["TEXT", "TEXT", "TEXT", "TEXT",
                "BLOB", "BLOB",
                "INTEGER"],
            ["feature_maps_unique"],
            ["UNIQUE(feature_map_id, sample_name, component_name)"]
        )

        self.quantitation_methods = DBTableInterface(    
            settings["database"]["dialect"],
            "quantitation_methods",
            None,
            ["quantitation_method_id",
                "IS_name", "component_name", "feature_name", "concentration_units", 
                "llod", "ulod", "lloq", "uloq", "correlation_coefficient", 
                "n_points", "transformation_model", 
                "transformation_model_param_slope", 
                "transformation_model_param_intercept", 
                "transformation_model_param_x_weight", 
                "transformation_model_param_y_weight", 
                "transformation_model_param_x_datum_min", 
                "transformation_model_param_x_datum_max", 
                "transformation_model_param_y_datum_min", 
                "transformation_model_param_y_datum_max",
                "used_"],
            ["TEXT",
                "TEXT", "TEXT", "TEXT", "TEXT", 
                "REAL", "REAL", "REAL", "REAL", "REAL", 
                "INTEGER", "TEXT", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL", 
                "REAL",
                "INTEGER"],
            ["quantitation_methods_unique"],
            ["UNIQUE(quantitation_method_id, component_name)"]
        )

        self.standards_concentrations = DBTableInterface(    
            settings["database"]["dialect"],
            "standards_concentrations",
            None,
            ["standards_concentrations_id",
                "sample_name", "component_name", "IS_component_name", 
                "actual_concentration", 
                "IS_actual_concentration", "concentration_units", "dilution_factor",
                "used_"],
            ["TEXT",
                "TEXT", "TEXT", "TEXT", 
                "REAL", 
                "REAL", "TEXT", "REAL",
                "INTEGER"],
            ["standards_concentrations_unique"],
            ["""UNIQUE(standards_concentrations_id, sample_name, component_name, 
            IS_component_name, actual_concentration, IS_actual_concentration, 
            concentration_units, dilution_factor)"""]
        )

        self.algorithm_parameters = DBTableInterface(    
            settings["database"]["dialect"],
            "algorithm_parameters",
            None,
            ["function", "name", "type", "value", "default",
                "restrictions", "description",
                "used_"],
            ["TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
                "INTEGER"],
            ["algorithm_parameters_unique"],
            ["""UNIQUE(function, name)"""]
        )

        self.transaction_log = DBTableInterface(    
            settings["database"]["dialect"],
            "transaction_log",
            None,
            ["user", "transaction"],
            ["TEXT", "TEXT"],
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
        self.feature_maps.set_conn(conn)
        self.quantitation_methods.set_conn(conn)
        self.standards_concentrations.set_conn(conn)
        self.algorithm_parameters.set_conn(conn)
        self.transaction_log.set_conn(conn)

        self.sequence_file.set_cursor(cursor)
        self.traml.set_cursor(cursor)
        self.feature_filter.set_cursor(cursor)
        self.feature_qc.set_cursor(cursor)
        self.feature_maps.set_cursor(cursor)
        self.quantitation_methods.set_cursor(cursor)
        self.standards_concentrations.set_cursor(cursor)
        self.algorithm_parameters.set_cursor(cursor)
        self.transaction_log.set_cursor(cursor)
    
    def create_tables(self):
        """Create all tables"""      

        self.sequence_file.create_table()
        self.traml.create_table()
        self.feature_filter.create_table()
        self.feature_qc.create_table()
        self.feature_maps.create_table()
        self.quantitation_methods.create_table()
        self.standards_concentrations.create_table()
        self.algorithm_parameters.create_table()
        self.transaction_log.create_table()
    
    def drop_tables(self):
        """Drop all tables"""      

        self.sequence_file.drop_table()
        self.traml.drop_table()
        self.feature_filter.drop_table()
        self.feature_qc.drop_table()
        self.feature_maps.drop_table()
        self.quantitation_methods.drop_table()
        self.standards_concentrations.drop_table()
        self.algorithm_parameters.drop_table()
        self.transaction_log.drop_table()
