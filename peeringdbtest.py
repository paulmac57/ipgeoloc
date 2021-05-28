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

for ix in exc:
    
    if ix['country'] == 'ZA':
        
        
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
        for ix_lan in ix['ixlan_set']:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(ix_lan)
            i = pdb.fetch(resource.InternetExchangeLan, ix_lan)
            print('Ix Lan',ixs,i)
            nets = 1
            print(i[0]['net_set'])
            for net in i[0]['net_set']:
    
                print('---------------------------------------------------------')
                print(net)
                n = pdb.fetch(resource.Network, 11084)
                print('Network',nets,n)
                print('---------------------------------------------------------')
                nfacs = 1
                
                for nf in n[0]['netfac_set']: # ties the facility into the netset
                    print('fffffffffffffffffffffffffffffffffffffffffffffff')
                    print(nf)
                    nfac = pdb.fetch(resource.NetworkFacility, nf)
                    print('Network Facilities',nfacs,nfac)
                    print('ffffffffffffffffffffffffffffffffffffffffffffffff')
                    nfacs += 1
                ixlans = 1
                for ixl in n[0]['netixlan_set']: 
                    print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
                    print(ixl)
                    ixlan = pdb.fetch(resource.NetworkIXLan, ixl)
                    print('Network IXLAN',ixlans,ixlan)
                    print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
                    ixlans += 1
                nets += 1
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
            ixs += 1
'''
#print(exc[287])
print(fac[0])
'''



        
