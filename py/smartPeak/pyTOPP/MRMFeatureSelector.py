# -*- coding: utf-8 -*-
#utilities
import copy
from math import log, exp, sqrt, log10
#modules
from smartPeak.core.smartPeak import smartPeak
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class MRMFeatureSelector():
    """MRMFeatureSelector selects features (FeatureMap)

    """

    def select_MRMFeatures_qmip(
        self,
        features,
        tr_expected=[],
        select_criteria=[
            {"name":"nn_threshold", "value":3},
            {"name":"locality_weights", "value":True},
            {"name":"select_transition_groups", "value":True},
            {"name":"segment_window_lengths", "value":12},
            {"name":"segment_step_lengths", "value":3},
            {"name":"select_highest_count", "value":False}],
        verbose_I=False
        ):
        """Aligns feature Tr (retention time, normalized retention time)
        and removes features that violate retention time order

        Args:
            features (FeatureMap):
            tr_expected (list(dict)): expected retention times
            select_criteria (list,dict): e.g., [{"name":, "value":, }]
                name: "nn_threshold", value:10, type: float, description: # of nearest compounds by Tr to include in network
                name: "locality_weights": value:True, type: boolean, description: weight compounds with a nearer Tr greater than compounds with a further Tr
                name: "select_transition_groups": value:True, type: boolean, description: select transition groups or transitions
                name: "segment_window_length": value:12, type: float, description: 
                name: "segment_step_length": value:6, type: float, description: 

        Returns:
            FeatureMap :output_O: filtered features

        Todo:
            remove features that violate retention time order...

        """
        from math import floor, ceil
        # Parse the input parameters
        select_criteria_dict = {d['name']:d['value'] for d in select_criteria}
        nn_threshold = 2
        locality_weights = True
        select_transition_groups = True
        segment_window_length = 12
        segment_step_length = 2
        select_highest_count = False
        variable_type = 'continuous',
        optimal_threshold = 0.5
        if "nn_threshold" in select_criteria_dict.keys():
            nn_threshold = select_criteria_dict["nn_threshold"]
        if "locality_weights" in select_criteria_dict.keys():
            locality_weights = select_criteria_dict["locality_weights"]
        if "select_transition_groups" in select_criteria_dict.keys():
            select_transition_groups = select_criteria_dict["select_transition_groups"]
        if "segment_window_length" in select_criteria_dict.keys():
            segment_window_length = select_criteria_dict["segment_window_length"]
        if "segment_step_length" in select_criteria_dict.keys():
            segment_step_length = select_criteria_dict["segment_step_length"]
        if "select_highest_count" in select_criteria_dict.keys():
            select_highest_count = select_criteria_dict["select_highest_count"]
        if "variable_type" in select_criteria_dict.keys():
            variable_type = select_criteria_dict["variable_type"]
        if "optimal_threshold" in select_criteria_dict.keys():
            optimal_threshold = select_criteria_dict["optimal_threshold"]
        #build the retention time dictionaries
        Tr_expected_dict = {}
        Tr_dict = {}
        feature_count = 0
        for feature in features:
            component_group_name = feature.getMetaValue("PeptideRef").decode('utf-8')
            retention_time = feature.getRT()
            assay_retention_time = feature.getMetaValue("assay_rt")
            transition_id = feature.getUniqueId()
            keys = []
            feature.getKeys(keys)
            feature_metaValues = {k.decode('utf-8'):feature.getMetaValue(k) for k in keys}
            if select_transition_groups:   
                tmp = {'component_group_name':component_group_name,
                    'component_name':component_group_name, #note component_name ~ component_group_name
                    'retention_time':retention_time,'transition_id':transition_id}
                tmp.update(feature_metaValues)
                if not component_group_name in Tr_dict.keys():
                    Tr_dict[component_group_name] = []
                Tr_dict[component_group_name].append(tmp)
                feature_count += 1
                Tr_expected_dict[component_group_name] = {
                    'retention_time':assay_retention_time,
                    'component_name':component_group_name, #note component_name ~ component_group_name
                    'component_group_name':component_group_name,
                    }
            else:
                for subordinate in feature.getSubordinates():
                    component_name = subordinate.getMetaValue('native_id').decode('utf-8')
                    keys = []
                    subordinate.getKeys(keys)
                    subordinate_metaValues = {k.decode('utf-8'):subordinate.getMetaValue(k) for k in keys}
                    tmp = {'component_group_name':component_group_name,'component_name':component_name,
                        'retention_time':retention_time,'transition_id':transition_id}
                    tmp.update(feature_metaValues)
                    tmp.update(subordinate_metaValues)
                    if not component_name in Tr_dict.keys():
                        Tr_dict[component_name] = []
                    Tr_dict[component_name].append(tmp)
                    feature_count += 1
                    Tr_expected_dict[component_group_name] = {
                        'retention_time':assay_retention_time,
                        'component_name':component_name, #note component_name ~ component_group_name
                        'component_group_name':component_group_name,
                        }
        from operator import itemgetter
        To_list = sorted(Tr_expected_dict.values(), key=itemgetter('retention_time')) 
        if verbose_I: print("Extracted %s features"%(feature_count))
        # Select optimal retention times
        Tr_optimal_count = {}
        # To_list = To_list[:35] #TESTING ONLY
        if segment_step_length == -1 and segment_window_length == -1:
            segment_step_length = len(To_list)
            segment_window_length = len(To_list)
        segments = int(ceil(len(To_list)/segment_step_length))
        if verbose_I: print("Selecting optimal Tr in segments")
        Tr_optimal = []
        for i in range(segments): #could be distributed and parallelized
            if verbose_I: print("Optimizing for segment (%s/%s)"%(i,segments))
            start_iter = segment_step_length*i
            stop_iter = min([segment_step_length*i+segment_window_length,len(To_list)])
            tmp = self.optimize_Tr(
                To_list[start_iter:stop_iter],
                Tr_dict,
                Tr_expected_dict,
                nn_threshold,
                locality_weights,
                variable_type,
                optimal_threshold
                )
            if select_highest_count:
                for var in tmp:
                    transition_id = var.split('_')[-1]
                    if not var in Tr_optimal_count.keys():
                        Tr_optimal_count[var] = 0
                    Tr_optimal_count[var] += 1
            else:                
                Tr_optimal.extend(tmp)
        if select_highest_count:
            # Reorganize
            Tr_optimal_dict = {}
            for var,count in Tr_optimal_count.items():
                component_name = '_'.join(var.split('_')[:-1])
                transition_id = var.split('_')[-1]
                if not var in Tr_optimal_dict.keys():
                    Tr_optimal_dict[component_name] = []
                tmp = {'transition_id':transition_id,
                        'count':count
                    }
                Tr_optimal_dict[component_name].append(tmp)
            # Select highest count transitions
            for component_name,rows in Tr_optimal_dict.items():
                best_count = 0
                for i,row in enumerate(rows):
                    if row['count']>best_count:
                        best_count = row['count']
                best_vars = []
                for i,row in enumerate(rows):
                    if row['count']==best_count:
                        var = '_'.join([component_name,row['transition_id']])
                        best_vars.append(var)
                Tr_optimal.extend(best_vars)             
        # Filter the FeatureMap
        output_filtered = pyopenms.FeatureMap()
        for feature in features:
            subordinates_tmp = []
            for subordinate in feature.getSubordinates():
                if select_transition_groups:
                    var_name = "%s_%s"%(feature.getMetaValue("PeptideRef").decode('utf-8'),feature.getUniqueId()) 
                else:
                    var_name = "%s_%s"%(subordinate.getMetaValue("native_id").decode('utf-8'),feature.getUniqueId())                
                if var_name in Tr_optimal: 
                    subordinates_tmp.append(subordinate)
            #check that subordinates were found
            if not subordinates_tmp:
                continue
            #copy out all feature values
            feature_tmp = copy.copy(feature)
            feature_tmp.setSubordinates(subordinates_tmp)
            output_filtered.push_back(feature_tmp)
        if verbose_I: print("Filtered %s features"%(len(list(set(Tr_optimal)))))
        return output_filtered

    def optimize_Tr(
        self,
        To_list,
        Tr_dict,
        Tr_expected_dict,
        nn_threshold,
        locality_weights,
        variable_type = 'integer',
        optimal_threshold = 0.5,
        verbose_I=False
        ):
        """
        optimize the retention time using QMIP

        Args:
            To_list (list(dict))
            To_list (dict)
            nn_threshold (float): # of nearest compounds by Tr to include in network
            locality_weights (boolean): weight compounds with a nearer Tr greater than compounds with a further Tr
            variable_type (str): the type of variable, 'integer' or 'continuous'
            optimal_threshold (float): value above which the transition group or transition is considered optimal (0 < x < 1)

        Returns:
            list: tr_optimial: list of optimal transition variable names  

        Potential Speed Optimizations
            Add in a check to see if multiple peaks for a transition or transition group actually exist


        """
        #build the model variables and constraints
        from optlang.glpk_interface import Model, Variable, Constraint, Objective
        from sympy import S
        import time as time
        variables = {}
        component_names_1 = []
        obj_variables = {}
        n_constraints = 0
        n_variables = 0
        model = Model(name='Retention time alignment')
        if verbose_I: print("Building and adding model constraints")
        st = time.time()
        for cnt_1,v1 in enumerate(To_list):
            if verbose_I: print("Building and adding variables and constraints for (%s/%s) components"%(cnt_1,len(To_list)-1))
            component_name_1 = v1['component_name']
            constraints = []
            constraint_name_1 = '%s_constraint'%(component_name_1)
            if not component_name_1 in Tr_dict.keys():
                continue
            for i_1,row_1 in enumerate(Tr_dict[component_name_1]):
                #variable capture 1
                variable_name_1 = '%s_%s'%(component_name_1,Tr_dict[component_name_1][i_1]['transition_id'])
                if not variable_name_1 in variables.keys():
                    variables[variable_name_1] = Variable(variable_name_1, lb=0, ub=1, type=variable_type)
                    model.add(variables[variable_name_1])
                    component_names_1.append(component_name_1)
                    n_variables += 1
                score_1 = (1/log10(Tr_dict[component_name_1][i_1]['peak_apices_sum']))\
                    *(1/log(Tr_dict[component_name_1][i_1]['sn_ratio']))\
                    *Tr_dict[component_name_1][i_1]['rt_score']
                # score_1 = (1/log(Tr_dict[component_name_1][i_1]['sn_ratio']))\
                #     *Tr_dict[component_name_1][i_1]['rt_score']
                #constraint capture 1
                constraints.append(variables[variable_name_1])
                #iterate over nearest neighbors
                start_iter, stop_iter = 0, 0
                start_iter = max([cnt_1-nn_threshold,0])
                stop_iter = min([cnt_1+nn_threshold+1,len(To_list)]) #NOTE: +1 to compensate for component_name_1 != component_name_2
                for cnt_2,v2 in enumerate(To_list[start_iter:stop_iter]):
                    component_name_2 = v2['component_name']
                    #prevent redundant combinations
                    if component_name_1 == component_name_2:
                        continue
                    if not component_name_2 in Tr_dict.keys():
                        continue
                    for i_2,row_2 in enumerate(Tr_dict[component_name_2]):
                        #variable capture 2
                        variable_name_2 = '%s_%s'%(component_name_2,Tr_dict[component_name_2][i_2]['transition_id'])
                        if not variable_name_2 in variables.keys():
                            variables[variable_name_2] = Variable(variable_name_2, lb=0, ub=1, type=variable_type)
                            model.add(variables[variable_name_2])
                            n_variables += 1
                        score_2 = (1/log10(Tr_dict[component_name_2][i_2]['peak_apices_sum']))\
                            *(1/log(Tr_dict[component_name_2][i_2]['sn_ratio']))\
                            *Tr_dict[component_name_2][i_2]['rt_score']
                        # score_2 = (1/log(Tr_dict[component_name_2][i_2]['sn_ratio']))\
                        #     *Tr_dict[component_name_2][i_2]['rt_score']
                        #record the objective
                        obj_constraints = []
                        tr_delta_expected = Tr_expected_dict[component_name_1]['retention_time'] - Tr_expected_dict[component_name_1]['retention_time']
                        tr_delta = row_1['retention_time'] - row_2['retention_time']  
                        obj_constraint_name = '%s_%s-%s_%s'%(component_name_1,i_1,component_name_2,i_2)
                        #linearized binary variable multiplication
                        var_qp_name = '%s_%s-%s_%s'%(component_name_1,i_1,component_name_2,i_2)
                        var_qp = Variable(var_qp_name, lb=0, ub=1, type="continuous")
                        model.add(var_qp)
                        # model.add(Constraint(
                        #     variables[variable_name_1]-var_qp,
                        #     name=obj_constraint_name+'-QP1',
                        #     lb=0
                        # ))
                        model.add(Constraint(S.Zero,
                            name=obj_constraint_name+'-QP1',
                            lb=0))
                        model.constraints[obj_constraint_name+'-QP1'].set_linear_coefficients({
                            variables[variable_name_1]:1,var_qp:-1
                        })
                        # model.add(Constraint(
                        #     variables[variable_name_2]-var_qp,
                        #     name=obj_constraint_name+'-QP2',
                        #     lb=0
                        # ))
                        model.add(Constraint(S.Zero,
                            name=obj_constraint_name+'-QP2',
                            lb=0))
                        model.constraints[obj_constraint_name+'-QP2'].set_linear_coefficients({
                            variables[variable_name_2]:1,var_qp:-1
                        })
                        # model.add(Constraint(
                        #     variables[variable_name_1]+variables[variable_name_2]-1-var_qp,
                        #     name=obj_constraint_name+'-QP3',
                        #     ub=0
                        # ))
                        model.add(Constraint(S.Zero,
                            name=obj_constraint_name+'-QP3',
                            ub=1))
                        model.constraints[obj_constraint_name+'-QP3'].set_linear_coefficients({
                            variables[variable_name_1]:1,variables[variable_name_2]:1,var_qp:-1
                        })
                        #linearized ABS terms
                        locality_weight = 1.0
                        if locality_weights:
                            locality_weight = 1.0/(nn_threshold-abs(start_iter+cnt_2-cnt_1)+1)
                        obj_variable_name = '%s_%s-%s_%s-ABS'%(component_name_1,i_1,component_name_2,i_2)
                        obj_variables[obj_variable_name] = Variable(obj_variable_name, type="continuous")
                        model.add(obj_variables[obj_variable_name])
                        # model.add(Constraint(
                        #     var_qp*locality_weight*(tr_delta-tr_delta_expected)-obj_variables[obj_variable_name],
                        #     name=obj_constraint_name+'-obj+',
                        #     ub=0
                        # ))
                        model.add(Constraint(S.Zero,
                            name=obj_constraint_name+'-obj+',
                            ub=0))
                        model.constraints[obj_constraint_name+'-obj+'].set_linear_coefficients({
                            obj_variables[obj_variable_name]:-1,var_qp:locality_weight*score_1*score_2*(tr_delta-tr_delta_expected)
                        })
                        # model.add(Constraint(
                        #     -var_qp*locality_weight*(tr_delta-tr_delta_expected)-obj_variables[obj_variable_name],
                        #     name=obj_constraint_name+'-obj-',
                        #     ub=0
                        # ))
                        model.add(Constraint(S.Zero,
                            name=obj_constraint_name+'-obj-',
                            ub=0))
                        model.constraints[obj_constraint_name+'-obj-'].set_linear_coefficients({
                            obj_variables[obj_variable_name]:-1,var_qp:-locality_weight*score_1*score_2*(tr_delta-tr_delta_expected)
                        })
                        n_constraints += 5 
                        n_variables += 2
            # model.add(Constraint(sum(constraints),name=constraint_name_1, lb=1, ub=1))  
            model.add(Constraint(S.Zero,name=constraint_name_1, lb=1, ub=1))
            model.constraints[constraint_name_1].set_linear_coefficients({d:1 for d in constraints})
            n_constraints += 1    
        if verbose_I: print("Model variables:", n_variables)
        if verbose_I: print("Model constraints:", n_constraints)
        # #make the constraints
        # print("Adding model constraints")
        # st = time.time()
        # model.add([Constraint(sum(v),name=constraint_name, lb=1, ub=1) for constraint_name, v in constraints.items()])
        # # for constraint_name, v in constraints.items():
        # #     model.add(Constraint(sum(v),name=constraint_name, lb=1, ub=1))
        # for constraint_name, v in obj_constraints.items(): #model.add([v for constraint_name, v in obj_constraints.items()])
        #     model.add(v)
        #make the objective
        # objective = Objective(sum(obj_variables.values()),direction='min')
        objective = Objective(S.Zero,direction='min')
        model.objective = objective     
        model.objective.set_linear_coefficients({d:1 for d in obj_variables.values()}) 
        elapsed_time = time.time() - st
        if verbose_I: print("Elapsed time: %.2fs" % elapsed_time)
        # Optimize and print the solution
        if verbose_I: print("Solving the model")
        st = time.time()
        status = model.optimize()
        if verbose_I: print("Status:", status)
        if verbose_I: print("Objective value:", model.objective.value)        
        elapsed_time = time.time() - st
        if verbose_I: print("Elapsed time: %.2fs" % elapsed_time)
        Tr_optimal = [var.name for var in model.variables if var.primal > optimal_threshold and var.name in variables.keys()]
        # # DEBUGING:
        # print(len(Tr_optimal),len(variables.keys()))
        # Tr_primals = [{var.name:var.primal} for var in model.variables if var.name in variables.keys()]
        # for var in model.variables: if var.name in variables.keys(): print("%s:%s"%(var.name,var.primal))
        return Tr_optimal

    def schedule_MRMFeatures_qmip(
        self,
        features,
        targeted = None,
        tr_expected = [],
        schedule_criteria = [],
        verbose_I = False):

        import time as time
        smartpeak = smartPeak()
        
        # Parse the input parameters
        select_criteria_dict = {d['name']:smartpeak.parseString(d['value'],encode_str_I = False) for d in schedule_criteria}
        nn_thresholds = [2,4,6,4]
        locality_weights = [False,True,True,True]
        select_transition_groups = [True,True,True,True]
        segment_window_lengths = [12,24,48,-1]
        segment_step_lengths = [2,6,12,-1]
        select_highest_counts = [False,False,False,False]
        variable_types = ['continous','continous','continous','continous']
        optimal_thresholds = [0.5,0.5,0.5,0.5]
        if "nn_thresholds" in select_criteria_dict.keys():
            nn_thresholds = select_criteria_dict["nn_thresholds"]
        if "locality_weights" in select_criteria_dict.keys():
            locality_weights = select_criteria_dict["locality_weights"]
        if "select_transition_groups" in select_criteria_dict.keys():
            select_transition_groups = select_criteria_dict["select_transition_groups"]
        if "segment_window_lengths" in select_criteria_dict.keys():
            segment_window_lengths = select_criteria_dict["segment_window_lengths"]
        if "segment_step_lengths" in select_criteria_dict.keys():
            segment_step_lengths = select_criteria_dict["segment_step_lengths"]  
        if "select_highest_counts" in select_criteria_dict.keys():
            select_highest_counts = select_criteria_dict["select_highest_counts"]   
        if "variable_types" in select_criteria_dict.keys():
            variable_types = select_criteria_dict["variable_types"]
        if "optimal_thresholds" in select_criteria_dict.keys():
            optimal_thresholds = select_criteria_dict["optimal_thresholds"]   				
				
        # Select optimal retention times
        if verbose_I: print("Selecting optimal Tr in iterations")
        st = time.time()
        output_features = features
        for i in range(len(segment_window_lengths)):
            if verbose_I: print("Optimizing for iteration (%s/%s)"%(i,len(segment_window_lengths)-1))
            select_criteria = [
            {"name":"nn_threshold", "value":nn_thresholds[i]},
            {"name":"locality_weights", "value":locality_weights[i]},
            {"name":"select_transition_groups", "value":select_transition_groups[i]},
            {"name":"segment_window_length", "value": segment_window_lengths[i]},
            {"name":"segment_step_length", "value": segment_step_lengths[i]},
            {"name":"select_highest_count", "value":select_highest_counts[i]},
            {"name":"variable_type", "value":variable_types[i]},
            {"name":"optimal_threshold", "value":optimal_thresholds[i]}]
            output_features = self.select_MRMFeatures_qmip(
                output_features,
                tr_expected,
                select_criteria) 
        elapsed_time = time.time() - st
        if verbose_I: print("Scheduler time: %.2fs" % elapsed_time)
        return output_features

    def select_MRMFeatures_score(
        self,features,
        score_weights=[],
        verbose_I = False):
        """Selects the best feature from a FeatureMap based on a scoring criteria
        
        Args:
            features (FeatureMap):
            score_weights (list,dict): e.g., [{"name":, "value":, }]
            n_peaks_max (int): maximum number of features per transition to extract
                in ascending order

        Returns:
            FeatureMap: output_O: selected features
        """
        from math import floor, ceil
        # Parse the input parameters
        # select_criteria_dict = {d['name']:d['value'] for d in select_criteria}
        select_transition_groups = True
        segment_window_length = -1
        segment_step_length = -1
        select_highest_count = False
        variable_type = 'integer'
        optimal_threshold = 0.5
        # if "select_transition_groups" in select_criteria_dict.keys():
        #     select_transition_groups = select_criteria_dict["select_transition_groups"]
        # if "segment_window_length" in select_criteria_dict.keys():
        #     segment_window_length = select_criteria_dict["segment_window_length"]
        # if "segment_step_length" in select_criteria_dict.keys():
        #     segment_step_length = select_criteria_dict["segment_step_length"]
        # if "select_highest_count" in select_criteria_dict.keys():
        #     select_highest_count = select_criteria_dict["select_highest_count"]
        # if "variable_type" in select_criteria_dict.keys():
        #     variable_type = select_criteria_dict["variable_type"]
        # if "optimal_threshold" in select_criteria_dict.keys():
        #     optimal_threshold = select_criteria_dict["optimal_threshold"]
        #build the retention time dictionaries
        Tr_expected_dict = {}
        Tr_dict = {}
        feature_count = 0
        for feature in features:
            component_group_name = feature.getMetaValue("PeptideRef").decode('utf-8')
            retention_time = feature.getRT()
            assay_retention_time = feature.getMetaValue("assay_rt")
            transition_id = feature.getUniqueId()
            keys = []
            feature.getKeys(keys)
            feature_metaValues = {k.decode('utf-8'):feature.getMetaValue(k) for k in keys}
            if select_transition_groups:   
                tmp = {'component_group_name':component_group_name,
                    'component_name':component_group_name, #note component_name ~ component_group_name
                    'retention_time':retention_time,'transition_id':transition_id}
                tmp.update(feature_metaValues)
                if not component_group_name in Tr_dict.keys():
                    Tr_dict[component_group_name] = []
                Tr_dict[component_group_name].append(tmp)
                feature_count += 1
                Tr_expected_dict[component_group_name] = {
                    'retention_time':assay_retention_time,
                    'component_name':component_group_name, #note component_name ~ component_group_name
                    'component_group_name':component_group_name,
                    }
            else:
                for subordinate in feature.getSubordinates():
                    component_name = subordinate.getMetaValue('native_id').decode('utf-8')
                    keys = []
                    subordinate.getKeys(keys)
                    subordinate_metaValues = {k.decode('utf-8'):subordinate.getMetaValue(k) for k in keys}
                    tmp = {'component_group_name':component_group_name,'component_name':component_name,
                        'retention_time':retention_time,'transition_id':transition_id}
                    tmp.update(feature_metaValues)
                    tmp.update(subordinate_metaValues)
                    if not component_name in Tr_dict.keys():
                        Tr_dict[component_name] = []
                    Tr_dict[component_name].append(tmp)
                    feature_count += 1
                    Tr_expected_dict[component_group_name] = {
                        'retention_time':assay_retention_time,
                        'component_name':component_name, #note component_name ~ component_group_name
                        'component_group_name':component_group_name,
                        }
        from operator import itemgetter
        To_list = sorted(Tr_expected_dict.values(), key=itemgetter('retention_time')) 
        if verbose_I: print("Extracted %s features"%(feature_count))
        # Select optimal retention times
        Tr_optimal_count = {}
        # To_list = To_list[:35] #TESTING ONLY
        if segment_step_length == -1 and segment_window_length == -1:
            segment_step_length = len(To_list)
            segment_window_length = len(To_list)
        segments = int(ceil(len(To_list)/segment_step_length))
        if verbose_I: print("Selecting optimal Tr in segments")
        Tr_optimal = []
        for i in range(segments): #could be distributed and parallelized
            if verbose_I: print("Optimizing for segment (%s/%s)"%(i,segments))
            start_iter = segment_step_length*i
            stop_iter = min([segment_step_length*i+segment_window_length,len(To_list)])
            tmp = self.optimize_scores(
                To_list[start_iter:stop_iter],
                Tr_dict,
                score_weights,
                variable_type,
                optimal_threshold
                )
            if select_highest_count:
                for var in tmp:
                    transition_id = var.split('_')[-1]
                    if not var in Tr_optimal_count.keys():
                        Tr_optimal_count[var] = 0
                    Tr_optimal_count[var] += 1
            else:                
                Tr_optimal.extend(tmp)
        if select_highest_count:
            # Reorganize
            Tr_optimal_dict = {}
            for var,count in Tr_optimal_count.items():
                component_name = '_'.join(var.split('_')[:-1])
                transition_id = var.split('_')[-1]
                if not var in Tr_optimal_dict.keys():
                    Tr_optimal_dict[component_name] = []
                tmp = {'transition_id':transition_id,
                        'count':count
                    }
                Tr_optimal_dict[component_name].append(tmp)
            # Select highest count transitions
            for component_name,rows in Tr_optimal_dict.items():
                best_count = 0
                for i,row in enumerate(rows):
                    if row['count']>best_count:
                        best_count = row['count']
                best_vars = []
                for i,row in enumerate(rows):
                    if row['count']==best_count:
                        var = '_'.join([component_name,row['transition_id']])
                        best_vars.append(var)
                Tr_optimal.extend(best_vars)             
        # Filter the FeatureMap
        output_filtered = pyopenms.FeatureMap()
        for feature in features:
            subordinates_tmp = []
            for subordinate in feature.getSubordinates():
                if select_transition_groups:
                    var_name = "%s_%s"%(feature.getMetaValue("PeptideRef").decode('utf-8'),feature.getUniqueId()) 
                else:
                    var_name = "%s_%s"%(subordinate.getMetaValue("native_id").decode('utf-8'),feature.getUniqueId())                
                if var_name in Tr_optimal: 
                    subordinates_tmp.append(subordinate)
            #check that subordinates were found
            if not subordinates_tmp:
                continue
            #copy out all feature values
            feature_tmp = copy.copy(feature)
            feature_tmp.setSubordinates(subordinates_tmp)
            output_filtered.push_back(feature_tmp)
        if verbose_I: print("Filtered %s features"%(len(list(set(Tr_optimal)))))
        return output_filtered

    def optimize_scores(
        self,
        To_list,
        Tr_dict,
        score_weights=[],
        variable_type = 'integer',
        optimal_threshold = 0.5,
        verbose_I = False
        ):
        """
        optimize for the best peak score using MIP

        Args:
            To_list (list,dict)
            Tr_list (dict)
            score_weights (list,dict): e.g., [{"name":, "value":, }]
                name (str) = name of the score
                value (str) = lambda transformation function
                e.g., scaling: lambda score: score*2
                      inverse log scaling: lambda score: 1/log(score)
            variable_type (str): the type of variable, 'integer' or 'continuous'
            optimal_threshold (float): value above which the transition group or transition is considered optimal (0 < x < 1)

        Returns:
            list: tr_optimial: list of optimal transition variable names  

        """
        #build the model variables and constraints
        from optlang.glpk_interface import Model, Variable, Constraint, Objective
        from sympy import S
        import time as time
        variables = {}
        component_names_1 = []
        obj_coefficients = {}
        n_constraints = 0
        n_variables = 0
        model = Model(name='Retention time alignment')
        if verbose_I: print("Building and adding model constraints")
        st = time.time()
        for cnt_1,v1 in enumerate(To_list):
            if verbose_I: print("Building and adding variables and constraints for (%s/%s) components"%(cnt_1,len(To_list)-1))
            component_name_1 = v1['component_name']
            constraints = []
            constraint_name_1 = '%s_constraint'%(component_name_1)
            if not component_name_1 in Tr_dict.keys():
                continue
            for i_1,row_1 in enumerate(Tr_dict[component_name_1]):
                #variable capture 1
                variable_name_1 = '%s_%s'%(component_name_1,Tr_dict[component_name_1][i_1]['transition_id'])
                if not variable_name_1 in variables.keys():
                    variables[variable_name_1] = Variable(variable_name_1, lb=0, ub=1, type=variable_type)
                    model.add(variables[variable_name_1])
                    component_names_1.append(component_name_1)
                    n_variables += 1
                score_1 = 1.0
                for score_weight in score_weights:
                    weight_func = eval(score_weight['value']) #check for valid lambda string...
                    score_1 *= weight_func(Tr_dict[component_name_1][i_1][score_weight['name']])
                #constraint capture 1
                constraints.append(variables[variable_name_1])
                #record the objective coefficients
                obj_coefficients[variables[variable_name_1]] = score_1
            # model.add(Constraint(sum(constraints),name=constraint_name_1, lb=1, ub=1))  
            model.add(Constraint(S.Zero,name=constraint_name_1, lb=1, ub=1))
            model.constraints[constraint_name_1].set_linear_coefficients({d:1 for d in constraints})
            n_constraints += 1    
        if verbose_I: print("Model variables:", n_variables)
        if verbose_I: print("Model constraints:", n_constraints)
        #make the objective
        objective = Objective(S.Zero,direction='min')
        model.objective = objective     
        model.objective.set_linear_coefficients({k:v for k,v in obj_coefficients.items()}) 
        elapsed_time = time.time() - st
        if verbose_I: print("Elapsed time: %.2fs" % elapsed_time)
        # Optimize and print the solution
        if verbose_I: print("Solving the model")
        st = time.time()
        status = model.optimize()
        if verbose_I: print("Status:", status)
        if verbose_I: print("Objective value:", model.objective.value)        
        elapsed_time = time.time() - st
        if verbose_I: print("Elapsed time: %.2fs" % elapsed_time)
        Tr_optimal = [var.name for var in model.variables if var.primal > optimal_threshold and var.name in variables.keys()]
        # # DEBUGING:
        # print(len(Tr_optimal),len(variables.keys()))
        # Tr_primals = [{var.name:var.primal} for var in model.variables if var.name in variables.keys()]
        # for var in model.variables: if var.name in variables.keys(): print("%s:%s"%(var.name,var.primal))
        return Tr_optimal