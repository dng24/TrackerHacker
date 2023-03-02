#import adblock
from adblockparser import AdblockRules


#f = open('easylist.txt', 'r')
#FILTER_LIST = f.read()
#f.close()

def parse_fqdns(collected_list, domain_file):
    #filter_set = adblock.FilterSet()
    #filter_set.add_filter_list(FILTER_LIST)
    #engine = adblock.Engine(filter_set=filter_set)

    f = open(domain_file, 'r')
    raw_rules = f.readlines()
    rules = AdblockRules(raw_rules)
    #rules = AdblockRules(["https://adservice.google.com"])
    f.close()


    blockers = ["ad", "ads", "analytic", "tag", "tags", "pixel", "pxl", "px", "pix", "beacon", "metrics", "smetrics", "tracking", "track", "tracker", "sync"]



    for u in collected_list:
        #blockresult = rules.should_block(u)   
        #print(f"{u} W/o https head:  ", blockresult)
        
        blockresult = any(sd in blockers for sd in u.split("."))
        blockresult = blockresult or rules.should_block("https://" + u)
        print(f"{u} W/ https head:   ", blockresult)




        #blockresult = engine.check_network_urls(
        #        url = u,
        #        source_url = "https://google.com",
        #        request_type = ""
        #    )
        #print(blockresult)


parse_fqdns(["adservice.google.com", "a2.adform.net/", "www.hostg.xyz/", "c1.adform.net", "2mdn.net"], 'easylist.txt')