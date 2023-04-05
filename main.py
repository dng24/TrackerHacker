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


LOGGER_LEVEL = logging.DEBUG
PROXY_IP = "127.0.0.1"
PROXY_PORT = 8080
REQUEST_TIMEOUT = 5
TRACKER_HACKER_ROOT = os.path.dirname(sys.argv[0])
AD_TRACKER_LISTS_DIR = os.path.join(TRACKER_HACKER_ROOT, "adlists")
DEFAULT_OUTPUT_DIR = "out"

class ColorFormatter(logging.Formatter):
    green = "\x1b[32m"
    purple = "\x1b[35m"
    blue = "\x1b[36m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[1;31m"
    clear = "\x1b[0m"
    LOGGER_FORMAT = "{green}[TRACKER HACKER] {purple}%(levelname)-8s: {color}%(message)s{clear}"

    FORMATS = {
        logging.DEBUG: LOGGER_FORMAT.format(green=green, purple=purple, color=blue, clear=clear),
        logging.INFO: LOGGER_FORMAT.format(green=green, purple=purple, color=clear, clear=clear),
        logging.WARNING: LOGGER_FORMAT.format(green=green, purple=purple, color=yellow, clear=clear),
        logging.ERROR: LOGGER_FORMAT.format(green=green, purple=purple, color=red, clear=clear),
        logging.CRITICAL: LOGGER_FORMAT.format(green=green, purple=purple, color=bold_red, clear=clear)
    }

    def format(self, log: str) -> str:
        log_fmt = self.FORMATS.get(log.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(log)
    

def main() -> int:
    logger = logging.getLogger("tracker_hacker")
    logger.setLevel(LOGGER_LEVEL)
    log_handler = logging.StreamHandler()
    log_handler.setLevel(LOGGER_LEVEL)
    log_handler.setFormatter(ColorFormatter())
    logger.addHandler(log_handler)
    
    # 1. parse args
    # Determines what interface to use
    # If user is using command line args, it uses cli run, otherwise it defaults to gui
    if len(sys.argv) > 1:
        tracker_query = userinput.get_userinput_cli(AD_TRACKER_LISTS_DIR, DEFAULT_OUTPUT_DIR)
    else:
        tracker_query = userinput.get_user_input_gui(AD_TRACKER_LISTS_DIR, DEFAULT_OUTPUT_DIR)

    if tracker_query is None:
        return 0
    
    # 2. open urls with selenium and capture traffic with web proxy
    # TODO: add absolute timeout and support for browser paths
    logger.debug(tracker_query.browsers)
    logger.info("Start data collection")
    request_urls_data = datacollection.collect_request_urls(logger, tracker_query.query_urls, tracker_query.browsers, PROXY_IP, PROXY_PORT, REQUEST_TIMEOUT, tracker_query.headless)
    if len(request_urls_data) == 0:
        logger.warning("No HTTP requests collected, exiting...")
        return 1

    logger.info("Data collection done!")
    
    # 3. separate ad/tracking domains from other domains
    logger.info("Extracting ad and tracker data")
    ad_tracker_data = adparsing.extract_ads_and_trackers(logger, AD_TRACKER_LISTS_DIR, request_urls_data)
    if len(ad_tracker_data) == 0:
        logger.warning("No ad or tracker requests found, exiting...")
        return 1

    logger.info("Ads and trackers extracted!")

    # 4. use ad/tracking domain names to get data we want
    logger.info("Analyzing data")
    analysis_query = analysis.Analysis(logger, ad_tracker_data, TRACKER_HACKER_ROOT)
    #TODO opmitize by not running unnecessary analyses
    analysis_query.do_whois_analysis()
    analysis_query.do_server_location_analysis()

    analysis_results = analysis_query.get_results()
    if len(analysis_results) == 0:
        logger.warning("No analysis results, exiting...")
        return 1

    logger.debug(analysis_results)
    logger.info("Data analyzed!")
    
    #import json
    #with open("ana2.json", "w") as f:
    #    obj = json.dumps(analysis_results, default=str)
    #    json.dump(obj, f)

    #with open("ana_foxnews.json", "r") as f:
    #    analysis_results = json.load(f)

    # 5. make visualizations/reports
    logger.info("Generating outputs")
    output_generator = output.Output(logger, TRACKER_HACKER_ROOT, analysis_results, tracker_query.datapoints, tracker_query.output_dir)
    #from trackerhacker.TrackerObject import DataChoices
    #output_generator = output.Output(logger, TRACKER_HACKER_ROOT, analysis_results, [DataChoices.SERVER_STATE], "out")
    output_generator.make_csv_output()
    output_generator.make_heatmap()
    output_generator.make_brower_comparison()
    output_generator.make_top_sites_graph()
    output_generator.make_top_ads_trackers_graph()
    logger.info("Done!")
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        # don't print out stack trace on CTRL+C exit
        pass