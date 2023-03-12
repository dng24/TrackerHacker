#import adblock
import braveblock
from adblockparser import AdblockRules


#f = open('easylist.txt', 'r')
#FILTER_LIST = f.read()
#f.close()

def parse_fqdns(collected_list, domain_file):
    #filter_set = adblock.FilterSet()
    #filter_set.add_filter_list(FILTER_LIST)
    #engine = adblock.Engine(filter_set=filter_set)


    #AdBlockRules

    f = open(domain_file, 'r')
    raw_rules = f.readlines()
    
    #Creates engine instance
    rules = AdblockRules(raw_rules)
    #rules = AdblockRules(["https://adservice.google.com"])
    f.close()

    #BraveBlock
    bblocker = braveblock.Adblocker(
        rules = raw_rules
    )
        


    blockers = ["ad", "ads", "analytic", "tag", "tags", "pixel", "pxl", "px", "pix", "beacon", "metrics", "smetrics", "tracking", "track", "tracker", "sync"]

    for u in collected_list:
        
        #Adblockparser

        #blockresult = rules.should_block(u)   
        #print(f"{u} W/o https head:  ", blockresult)
       
        #Manual check for custom params   
        blockresult = any(sd in blockers for sd in u.split("."))
        
        #Adblockparser engine check against list
        blockresult = blockresult or rules.should_block("https://" + u) #Only returns correct results for some ads, not all
        print(f"AdblockParser {u} W/ https head:   ", blockresult)



        #Braveblock

        blockresult = bblocker.check_network_urls(
                url = u,
                source_url = "https://www.google.com",
                request_type = "", #No variation on request type seems to yield results
        )

        print(f"Braveblock {u}:   ", blockresult)


        
        #blockresult = engine.check_network_urls(
        #        url = u,
        #        source_url = "https://google.com",
        #        request_type = "other"
        #    )
        #print(blockresult)


parse_fqdns(["adservice.google.com", "a2.adform.net/", "www.hostg.xyz/", "c1.adform.net", "2mdn.net"], '/home/hson/Desktop/TrackerHacker/adlists/easylist.txt')
