from peeringdb import PeeringDB, resource, config

import django
import peeringdb

from pprint import pprint


pprint(dir(peeringdb.resource))

pdb = peeringdb.PeeringDB()
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
ixes = 1
exc = pdb.fetch_all(resource.InternetExchange)
fac_id = pdb.fetch_all(resource.InternetExchangeFacility)
facility = pdb.fetch_all(resource.Facility)
ixpfx = pdb.fetch_all(resource.InternetExchangeLanPrefix)

ixp1_address = '196.60.9.24'
ixp2_address = '196.10.140.7'
ipx3_address = '196.223.14.99'



for ix in ixpfx:
    
    if ix['ixlan_id'] == 129:
        print(ix)
'''


        print('===========================================')
        print(ixes,ix['name'], ix['org_id'])

        print(ix)
        print('===========================================')
        #exchanges[ixes] = ix
        ixes += 1
        facs = 1
        for fac in ix['fac_set']:
            print(fac)
            f = pdb.fetch(resource.Facility, fac)
            print('Facility',facs,f)
            facs += 1
        ixs = 1
'''