#utilities
import copy
#modules
from smartPeak.smartPeak import smartPeak
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
        tr_expected,
        select_criteria=[
            {"name":"nn_threshold", "value":3},
            {"name":"locality_weights", "value":True},
            {"name":"select_transition_groups", "value":True}]
        ):
        """Aligns feature Tr (retention time, normalized retention time)
        and removes features that violate retention time order

        Args
            features (FeatureMap):
            tr_expected (list(dict)): expected retention times
            select_criteria (list,dict): e.g., [{"name":, "value":, }]
                name: "nn_threshold", value:10, description: # of nearest compounds by Tr to include in network
                name: "locality_weights": value:True, description: weight compounds with a nearer Tr greater than compounds with a further Tr
                name: "select_transition_groups": value:True, description: select transition groups or transitions

        Returns
            output_O (FeatureMap): filtered features

        """
        from math import floor
        select_criteria_dict = {d['name']:d['value'] for d in select_criteria}
        nn_threshold = 2
        locality_weights = True
        select_transition_groups = True
        if "nn_threshold" in select_criteria_dict.keys():
            nn_threshold = select_criteria_dict["nn_threshold"]
        if "locality_weights" in select_criteria_dict.keys():
            locality_weights = select_criteria_dict["locality_weights"]
        if "select_transition_groups" in select_criteria_dict.keys():
            select_transition_groups = select_criteria_dict["select_transition_groups"]
        #build the retention time dictionaries
        from operator import itemgetter
        if select_transition_groups:
            Tr_expected_dict = {d['component_group_name']:{
            'retention_time':float(d['retention_time']),
            'component_name':d['component_group_name'], #note component_name ~ component_group_name
            'component_group_name':d['component_group_name'],
            } for d in tr_expected}
        else:
            Tr_expected_dict = {d['component_name']:{
            'retention_time':float(d['retention_time']),
            'component_name':d['component_name'],
            'component_group_name':d['component_group_name'],
            } for d in tr_expected}
        To_list = sorted(Tr_expected_dict.values(), key=itemgetter('retention_time')) 
        Tr_dict = {}
        for feature in features:
            component_group_name = feature.getMetaValue("PeptideRef").decode('utf-8')
            retention_time = feature.getRT()
            transition_id = feature.getUniqueId()
            if select_transition_groups:                
                if not component_group_name in Tr_expected_dict.keys():
                    continue
                tmp = {'component_group_name':component_group_name,
                    'component_name':component_group_name, #note component_name ~ component_group_name
                    'retention_time':retention_time,'transition_id':transition_id}
                if not component_group_name in Tr_dict.keys():
                    Tr_dict[component_group_name] = []
                Tr_dict[component_group_name].append(tmp)
            else:
                for subordinate in feature.getSubordinates():
                    component_name = subordinate.getMetaValue('native_id').decode('utf-8')
                    if not component_name in Tr_expected_dict.keys():
                        continue
                    tmp = {'component_group_name':component_group_name,'component_name':component_name,
                        'retention_time':retention_time,'transition_id':transition_id}
                    if not component_name in Tr_dict.keys():
                        Tr_dict[component_name] = []
                    Tr_dict[component_name].append(tmp)
        # select optimal retention times
        Tr_optimal = []
        # To_list = To_list[:70] #TESTING ONLY
        window = 12
        step = 6
        segments = int(floor(len(To_list)/6))
        print("Selecting optimal Tr in segments")
        for i in range(segments):
            print("Optimizing for segment (%s/%s)"%(i,segments))
            start_iter = step*i
            stop_iter = min([step*i+window,len(To_list)])
            Tr_optimal.extend(self.optimize_Tr(
                To_list[start_iter:stop_iter],
                Tr_dict,
                Tr_expected_dict,
                nn_threshold,
                locality_weights,
                select_transition_groups
                ))    
        # Filter the FeatureMap
        print("Filtering features")
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
        return output_filtered

    def select_MRMFeatures_score(
        self,features,
        score_weights=[]):
        """Selects the best feature from a FeatureMap based on a scoring criteria
        
        Args
            features (FeatureMap):
            score_weights (list,dict): e.g., [{"name":, "value":, }]
            n_peaks_max (int): maximum number of features per transition to extract
                in ascending order

        Returns
            output_O (FeatureMap): selected features
        """
        smartpeak = smartPeak()
        score_tmp = 0
        output_ranked = pyopenms.FeatureMap()
        #compute a pooled score for each transition group
        transition_group_id_current = ''
        best_transition_group = None
        best_transition_group_score = 0
        for feature in features:
            subordinates_tmp = []
            transition_group_id = feature.getMetaValue("PeptideRef").decode('utf-8')
            # add the best transition
            if transition_group_id != transition_group_id_current and not best_transition_group is None:
                output_ranked.push_back(best_transition_group)
            # initialize the best transition
            if transition_group_id != transition_group_id_current:
                transition_group_id_current = transition_group_id
                best_transition_group = None
                best_transition_group_score = 0
            for score_weight in score_weights:
                score = float(feature.getMetaValue(score_weight['name']))*float(score_weight['value'])
                if best_transition_group_score < score:
                    best_transition_group_score = score
                    best_transition_group = feature
        #add in the last best transition
        output_ranked.push_back(best_transition_group)
        return output_ranked

    def optimize_Tr(
        self,
        To_list,
        Tr_dict,
        Tr_expected_dict,
        nn_threshold,
        locality_weights,
        select_transition_groups
        ):
        """
        optimize the retention time using MIP

        Args
            tr_I (list(float))

        Returns
            tr_optimial (list): list of optimal transition variable names  
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
        print("Building and adding model constraints")
        st = time.time()
        for cnt_1,v1 in enumerate(To_list):
            print("Building and adding variables and constraints for (%s/%s) components"%(cnt_1,len(To_list)-1))
            component_name_1 = v1['component_name']
            constraints = []
            constraint_name_1 = '%s_constraint'%(component_name_1)
            if not component_name_1 in Tr_dict.keys():
                continue
            for i_1,row_1 in enumerate(Tr_dict[component_name_1]):
                #variable capture 1
                variable_name_1 = '%s_%s'%(component_name_1,Tr_dict[component_name_1][i_1]['transition_id'])
                if not variable_name_1 in variables.keys():
                    variables[variable_name_1] = Variable(variable_name_1, lb=0, ub=1, type="integer")
                    model.add(variables[variable_name_1])
                    component_names_1.append(component_name_1)
                    n_variables += 1
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
                            variables[variable_name_2] = Variable(variable_name_2, lb=0, ub=1, type="integer")
                            model.add(variables[variable_name_2])
                            n_variables += 1
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
                            obj_variables[obj_variable_name]:-1,var_qp:locality_weight*(tr_delta-tr_delta_expected)
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
                            obj_variables[obj_variable_name]:-1,var_qp:-locality_weight*(tr_delta-tr_delta_expected)
                        })
                        n_constraints += 5 
                        n_variables += 2
            # model.add(Constraint(sum(constraints),name=constraint_name_1, lb=1, ub=1))  
            model.add(Constraint(S.Zero,name=constraint_name_1, lb=1, ub=1))
            model.constraints[constraint_name_1].set_linear_coefficients({d:1 for d in constraints})
            n_constraints += 1    
        print("Model variables:", n_variables)
        print("Model constraints:", n_constraints)
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
        print("Elapsed time: %.2fs" % elapsed_time)
        # Optimize and print the solution
        print("Solving the model")
        st = time.time()
        status = model.optimize()
        print("Status:", status)
        print("Objective value:", model.objective.value)        
        elapsed_time = time.time() - st
        print("Elapsed time: %.2fs" % elapsed_time)
        Tr_optimal = [var.name for var in model.variables if var.primal != 0 and var.name in variables.keys()]
        return Tr_optimal
