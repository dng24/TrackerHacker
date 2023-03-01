import adblock


f = open('easylist.txt', 'r')
FILTER_LIST = f.read()
f.close()

def parse_fqdns(collected_list):
    filter_set = adblock.FilterSet()
    filter_set.add_filter_list(FILTER_LIST)
    engine = adblock.Engine(filter_set=filter_set)

    for u in collected_list:
        blockresult = engine.check_network_urls(
                url = u,
                source_url = "https://www.cnn.com",
                request_type = "url"
            )
        print(blockresult)

parse_fqdns(['c1.adform.net'])
