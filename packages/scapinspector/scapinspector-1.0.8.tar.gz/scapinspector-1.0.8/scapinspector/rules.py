import profile_core

def get_by_id(id,root):
    node=profile_core.get_node_by_attribute('id',id,root)
    if None==node:
        return None
    rule={}
    #print(node)
    title              = profile_core.node_values(node,"title"       )
    description        = profile_core.node_values(node,"description" )
    #title              = "sam"
    #description        = "bob"
    rule['id']         = id
    rule['title']      = title
    rule['description']= description
    return rule


def get_at_this_level(root):
    # TODO manage for reference
    nodes=root.get_elements()
    if None==nodes:
        return []
    rules_list=[]
    for node in nodes:
        tag=profile_core.get_tag_and_namespace(node._name)

        if tag['name'] == 'Rule':
            rule={}
            node_id            = node['id']
            if None == node_id:
                node_id=node['ref_id']
            if None == node_id:
                node_id=None

            if node_id == None:
                print ("DidntFind Rule by Ref")

            title              = profile_core.node_values(node,"title"       )
            description        = profile_core.node_values(node,"description" )
            rule['id']         = node_id
            rule['title']      = title
            rule['description']= description
            rules_list.append(rule)
    return rules_list