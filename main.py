try:
    import logging
    import os
    import sys

    from trackerhacker import userinput
    from trackerhacker import datacollection
    from trackerhacker import adparsing
    from trackerhacker import analysis
    from trackerhacker import output
except ModuleNotFoundError as e:
    print("Required modules could not be imported. To install required libraries, please run:\n\tpip3 install -r requirements.txt")
    exit(1)


LOGGER_FORMAT = "[TRACKER HACKER] %(levelname)-8s: %(message)s"
LOGGER_LEVEL = logging.DEBUG
PROXY_IP = "127.0.0.1"
PROXY_PORT = 8080
REQUEST_TIMEOUT = 5
AD_TRACKER_LISTS_DIR = os.path.join(os.path.dirname(sys.argv[0]), "adlists")


def main() -> None:
    logging.basicConfig(format=LOGGER_FORMAT)
    logger = logging.getLogger("tracker_hacker")
    logger.setLevel(LOGGER_LEVEL)

    # 1. parse args
    
    # Determines what interface to use
    # If user is using command line args, it uses cli run, otherwise it defaults to gui
    if len(sys.argv) > 1:
        tracker_query = userinput.get_userinput_cli(AD_TRACKER_LISTS_DIR)
    else:
        tracker_query = userinput.get_user_input_gui(AD_TRACKER_LISTS_DIR)

    # 2. open urls with selenium and capture traffic with web proxy
    # TODO: add absolute timeout and support for browser paths
    logger.debug(tracker_query.browsers)
    logger.info("Start data collection")
    request_urls_data = datacollection.collect_request_urls(logger, tracker_query.query_urls, tracker_query.browsers, PROXY_IP, PROXY_PORT, REQUEST_TIMEOUT, tracker_query.headless)
    if len(request_urls_data) == 0:
        exit(1)

    logger.info("Data collection done!")
    
    # 3. separate ad/tracking domains from other domains
    logger.info("Extracting ad and tracker data")
    ad_tracker_data = adparsing.extract_ads_and_trackers(logger, AD_TRACKER_LISTS_DIR, request_urls_data)
    if len(ad_tracker_data) == 0:
        exit(1)

    logger.info("Ads and trackers extracted!")

    # 4. use ad/tracking domain names to get data we want
    logger.info("Analyzing data")
    analysis_query = analysis.Analysis(logger, ad_tracker_data)
    #TODO opmitize by not running unnecessary analyses
    analysis_query.do_whois_analysis()
    analysis_query.do_server_location_analysis()

    analysis_results = analysis_query.get_results()
    print(analysis_results)
    logger.info("Data analyzed!")

    # 5. make visualizations/reports
    output_generator = output.Output(logger, analysis_results, tracker_query.datapoints, "out")
    output_generator.make_csv_output()
    output_generator.make_brower_comparison()

    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # don't print out stack trace on CTRL+C exit
        pass