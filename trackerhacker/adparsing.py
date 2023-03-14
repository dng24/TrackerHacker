from adblockparser import AdblockRules



def parse_fqdns(logger, collected_list, adtrack_path, default_flag):
    #filter_set = adblock.FilterSet()
    #filter_set.add_filter_list(FILTER_LIST)
    #engine = adblock.Engine(filter_set=filter_set)

    raw_rules = []
    default_adtrack_lists = ['adlists/default_list.txt']

    if default_flag:

    #Default AdBlockRules
        for lst in default_adtrack_lists:
            print(f"this is the list: {lst}")
            try:
                f = open(lst, 'r')

                tmp = f.readlines()
                raw_rules.extend(tmp)
                f.close()
            except:
                print("problem referencing a default file")
                continue

    print(f"this is the custom list path {adtrack_path}")

    if adtrack_path != "":
        try:
            f = open(adtrack_path, 'r')

            tmp = f.readlines()
            raw_rules.extend(tmp)
            f.close()
        except:
            print("problem opening custom adtracklist file")

    
    #Creates engine instance
    rules = AdblockRules(raw_rules)


    #try:
    #    cf = open(filepath, "r")
    #except:
    #    print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
            
    #for url in cf:
    #    try:
    #        custom_blocklist.append(url.strip())
    #    except Exception:
    #        print("Oops, looks like something is wrong with the default list file, and an error occured when processing it. Please make sure it is in the proper directory and the right format.\n")

    #custom_raw_rules= AdblockRules(custom_blocklist)
    #cf.close()

    #blockers = ["ad", "ads", "analytic", "tag", "tags", "pixel", "pxl", "px", "pix", "beacon", "metrics", "smetrics", "tracking", "track", "tracker", "sync"]

    for source_url, source_url_info in collected_list.items():
        for browser, browser_info in source_url_info.items(): 


            for fqdn, fqdn_info in browser_info.items():
                for full_url in fqdn_info:

                    blockresult = rules.should_block(full_url)
                    print(f"{full_url}:   ", blockresult)
        
