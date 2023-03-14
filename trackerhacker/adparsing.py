import os

from adblockparser import AdblockRules


def _get_ad_tracker_rules(ad_tracker_lists_dir: str) -> list:
    raw_rules = []
    for filename in os.listdir(ad_tracker_lists_dir):
        filepath = os.path.join(ad_tracker_lists_dir, filename)
        if os.path.isfile(filepath):
            #TODO: err handling
            with open(filepath, "r") as f:
                raw_rules.extend(f.readlines())

    return raw_rules


def extract_ads_and_trackers(logger, ad_tracker_lists_dir: str, collected_request_urls: dict) -> dict:
    results = {}
    raw_rules = _get_ad_tracker_rules(ad_tracker_lists_dir)

    #Creates engine instance
    rules = AdblockRules(raw_rules)

    num_ads = 0
    tot = 0
    for source_url, source_url_info in collected_request_urls.items():
        options = {"third-party": True, "domain": source_url}
        for browser, browser_info in source_url_info.items():
            for fqdn, fqdn_info in browser_info.items():
                for full_url in list(fqdn_info):
                    #TODO: performance improvements
                    blockresult = rules.should_block(full_url, options)
                    print(blockresult, f"{full_url}")
                    tot += 1
                    if blockresult:
                        num_ads += 1
                    if not blockresult:
                        del fqdn_info[full_url]

                browser_info[fqdn] = {i: k for i, k in fqdn_info.items() if k}

            source_url_info[browser] = {i: k for i, k in browser_info.items() if k}

        collected_request_urls[source_url] = {i: k for i, k in source_url_info.items() if k}

    collected_request_urls = {i: k for i, k in collected_request_urls.items() if k}

    print(num_ads, tot)
    print(collected_request_urls)
    return collected_request_urls


if __name__ == "__main__":
    import json
    with open("../out_cnn.json", "r") as f:
        asdf = json.load(f)

    extract_ads_and_trackers('c', asdf)
