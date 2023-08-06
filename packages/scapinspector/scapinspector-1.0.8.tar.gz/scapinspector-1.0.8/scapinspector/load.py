import models
import db

def  into_database(data):
    dbc=db.get_db()
    session=dbc['session']

    # all data parsed. lets insert
    print("Loading into db..")
    db_rule_list={}

    for rule in data['rules']:
        #print(rule)
        r=models.Rule( ref_id=rule['id'],
                        title=rule['title'],
                        description=rule['description'])
        db_rule_list[r.ref_id]=r
        session.add(r)
    session.commit()   

    for benchmark in data['benchmarks']:
        b=models.Benchmark(ref_id     =benchmark['id'],
                            title      =benchmark['title'],
                            description=benchmark['description'],
                            file       =benchmark['file'])
        session.add(b)
    
        for profile in benchmark['profiles']:
            p=models.Profile(  ref_id     =profile['id'],
                                title      =profile['title'],
                                description=profile['description'],
                                benchmark  =b)
            session.add(p)
            
            for select  in profile['selects']:
                s=models.Select(   ref_id   =select['ref_id'],
                                    selected =select['selected'],
                                    profile  =p,
                                    rule     =db_rule_list[select['ref_id']])
                session.add(s)
        
        #recursive nested group builder....
        add_groups(benchmark,b,db_rule_list,session)     
        session.commit()   



def add_groups(node,db_model_benchmark,db_rules,session, group_parent=None):
    for group in node['groups']:

        g=models.Group(
                ref_id       = group['id'],
                title        = group['title'],
                description  = group['description'],
                parent       = group_parent,
                benchmark    = db_model_benchmark)
        session.add(g)

        for rule in group['rules']:
            r=models.Group_Rule(   ref_id = rule,
                                    rule   = db_rules[rule],
                                    parent = g)
            session.add(r)
        
        add_groups(group,db_model_benchmark,db_rules,session,g)
