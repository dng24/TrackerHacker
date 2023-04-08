import braveblock
import os


def _get_ad_tracker_rules(logger, ad_tracker_lists_dir: str) -> list:
    raw_rules = []
    try:
        for filename in os.listdir(ad_tracker_lists_dir):
            filepath = os.path.join(ad_tracker_lists_dir, filename)
            if filename.endswith(".txt") and os.path.isfile(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        raw_rules.extend(f.readlines())
                except PermissionError:
                    logger.warning("Permission denied: '%s'. Please check that the file has read permission. Skipping....." % filepath)
                except Exception as e:
                    logger.warning("%s: %s. Skipping....." % (filepath, str(e)))

        if len(raw_rules) == 0:
            logger.error("No ad rules read. Please check that there are ad rules in .txt files in '%s' and that '%s' has read and execute permissions." % (ad_tracker_lists_dir, ad_tracker_lists_dir))
    except FileNotFoundError:
        logger.error("No such directory: '%s'. Please check that the directory exists and that it is populated with ad rules." % ad_tracker_lists_dir)
    except NotADirectoryError:
        logger.error("Not a directory: '%s'. It should be a directory populated with ad rules." % ad_tracker_lists_dir)
    except PermissionError:
        logger.error("Permission denied: '%s'. Please check that the directory has read and execute permission." % ad_tracker_lists_dir)
    except Exception as e:
        logger.error(e)

    return raw_rules


def extract_ads_and_trackers(logger, ad_tracker_lists_dir: str, collected_request_urls: dict) -> dict:
    raw_rules = _get_ad_tracker_rules(logger, ad_tracker_lists_dir)
    if len(raw_rules) == 0:
        return {}

    #Creates engine instance
    adblocker = braveblock.Adblocker(rules=raw_rules)
    num_ad_tracker_urls = 0
    total_urls = 0
    for source_url, source_url_info in collected_request_urls.items():
        for browser, browser_info in source_url_info.items():
            for fqdn, fqdn_info in browser_info.items():
                for full_url in list(fqdn_info):
                    blockresult = adblocker.check_network_urls(url=full_url, source_url=source_url, request_type="url")
                    logger.debug("%s    %s" % (blockresult, full_url))
                    total_urls += 1
                    if blockresult:
                        num_ad_tracker_urls += 1
                    else:
                        del fqdn_info[full_url]

                browser_info[fqdn] = {i: k for i, k in fqdn_info.items() if k}

            source_url_info[browser] = {i: k for i, k in browser_info.items() if k}

        collected_request_urls[source_url] = {i: k for i, k in source_url_info.items() if k}

    collected_request_urls = {i: k for i, k in collected_request_urls.items() if k}

    logger.info("Processed %d ad/tracker URLs, %d total URLs" % (num_ad_tracker_urls, total_urls))
    return collected_request_urls