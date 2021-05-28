from peeringdb import PeeringDB, resource, config

import django
import peeringdb

from pprint import pprint


pdb = peeringdb.PeeringDB()
pdb.update_all()
# https://github.com/grizz/pdb-examples
# EXAMPLE SCRIPT lookup network by ASN
#pdb.update_all()
#print ("TAGS")
#pprint(dir(pdb.tags.ix.all))


'''

'Class',
 'Facility',
 'InternetExchange',
 'InternetExchangeFacility',
 'InternetExchangeLan',
 'InternetExchangeLanPrefix',
 'Meta',
 'Network',
 'NetworkContact',
 'NetworkFacility',
 'NetworkIXLan',
 'OrderedDict',
 'Organization',
 'RESOURCES_BY_TAG',

 '''
ixes = 0
exc = pdb.fetch_all(resource.InternetExchange)
fac_id = pdb.fetch_all(resource.InternetExchangeFacility)
facility = pdb.fetch_all(resource.Facility)
org = pdb.fetch_all(resource.Organization)




for i in fac_id:
    if i['ix_id'] == 129:
        b = i['fac_id']
        print(i['fac_id'])
        for j in facility:
            if j['id'] == b:
                print(j)


'''
print(exc[0]) 
print(fac_id[0])
print(facility[0])

'''
for o in org:
    if o['id'] == 288:
        print(o)
        print(o['net_set'])
        print(o['fac_set'])
        print(o['ix_set'])