import profile_core
import rules
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# benchmarks
#   - benchmark
#       title
#       id
#       desc
#       profiles:
#         - profile 
#             title          
#             description
#             id
#             selects
#               - select
#                   idref
#                   selected
#       groups
#         - group
#             title          
#             description
#             id
#             rules
#             - groups
#
# rules
#   - rule
#     id 
#     title
#     description



def get(root,file):
    benchmark_nodes=profile_core.nodes(root,"data_stream_collection/component/Benchmark")
    benchmark_list=[]
    rules_list={}
    profile_count=0
    load_profiles=True
    #  Main loop for bulding profile catalog
    for benchmark_node in benchmark_nodes:
        benchmark_id           = benchmark_node["id"]
        profile_nodes          = profile_core.nodes      (benchmark_node,"Profile"     )
        benchmark_title        = profile_core.node_values(benchmark_node,"title"       )
        benchmark_description  = profile_core.node_values(benchmark_node,"description" )
        benchmark_profiles     = []


        if load_profiles is True:
            for profile in profile_nodes:
                profile_count+=1
                profile_id           = profile_core.get_id_or_ref(profile,root)
                profile_select_nodes = profile_core.nodes      (profile,"select"      )
                profile_title        = profile_core.node_values(profile,"title"       )
                profile_description  = profile_core.node_values(profile,"description" )
                
                selects=[]
                for select_node in profile_select_nodes:
                    select_id_ref     = select_node['idref']
                    select_selected   = select_node['selected']
                    select                 = {}
                    select['ref_id']        = select_id_ref
                    select['selected']     = select_selected
                    #print(select)
                    if select_id_ref not in rules_list:
                        rules_list[select_id_ref]=rules.get_by_id(select_id_ref,root)
                    selects.append(select)
                    

                profile                        = {}
                profile['id']                  = profile_id
                profile['title']               = profile_title
                profile['description']         = profile_description
                profile['selects']             = selects
                benchmark_profiles.append(profile)
        
        benchmark_groups = group_get(benchmark_node,rules_list)

        for rule in benchmark_groups['rules']:
            if rule not in rules_list:
                rules_list[rule]=benchmark_groups['rules'][rule]

        benchmark                = {}
        benchmark['id']          = benchmark_id
        benchmark['file']        = file
        benchmark['title']       = benchmark_title
        benchmark['description'] = benchmark_description
        benchmark['profiles']    = benchmark_profiles
        benchmark['groups']      = benchmark_groups['groups']
        benchmark['group_rules'] = benchmark_groups['rules']

        benchmark_list.append(benchmark)

    
    # dict to array
    stripped_rules_list=[]
    for rule in rules_list:
        stripped_rules_list.append(rules_list[rule])

    benchmark_count=len(benchmark_list)
    rules_count=len(stripped_rules_list)
    return {'benchmarks':benchmark_list,'rules':stripped_rules_list,'benchmark_count':benchmark_count,'profile_count':profile_count,'rule_count':rules_count}

# TODO maybe load rule defs at end...
# TODO identify why I dont see so many rules... diff profile?
def group_get(root,rules_list):
    group_nodes = profile_core.nodes(root,"Group")

    groups=[]
    for group_node in group_nodes:
        group_id              = group_node['id']
        group_selected        = group_node['selected']
        group_title           = profile_core.node_values(group_node,"title" )
        group_description     = profile_core.node_values(group_node,"description" )
        group                 = {}
        group['id']           = group_id
        group['selected']     = group_selected
        group['title']        = group_title
        group['description']  = group_description
        
        local_rules=[]        
        group_rules=rules.get_at_this_level(group_node)
        #print(group_rules)
        for group_rule in group_rules:
            rule_id=group_rule['id']
            if None != rule_id and rule_id not in rules_list:
                rules_list[rule_id]=group_rule
            local_rules.append(rule_id)

        group['rules']        = local_rules
        
        groupsresults=group_get(group_node,rules_list)
        group['groups']       =groupsresults['groups']
        groupsresults_rule_list =groupsresults['rules']
        for rule in groupsresults_rule_list:
            if rule not in rules_list:
                rules_list[rule]=groupsresults_rule_list[rule]
        #
        #if group_id not in rules_list:
        #   rules_list[select_id_ref]=rules.get_by_id(select_id_ref,root,namespaces)
        groups.append(group)
    return {'groups':groups,'rules':rules_list}
            