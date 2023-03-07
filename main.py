try:
    import logging
    import sys

    from trackerhacker import userinput
    from trackerhacker import datacollection
except ModuleNotFoundError as e:
    print("Required modules could not be imported. To install required libraries, please run:\n\tpip3 install -r requirements.txt")
    exit(1)


LOGGER_FORMAT = "[TRACKER HACKER] %(levelname)-8s: %(message)s"
LOGGER_LEVEL = logging.DEBUG
PROXY_IP = "127.0.0.1"
PROXY_PORT = 8080
REQUEST_TIMEOUT = 5


def main() -> None:
    logging.basicConfig(format=LOGGER_FORMAT)
    logger = logging.getLogger("tracker_hacker")
    logger.setLevel(LOGGER_LEVEL)

    # 1. parse args
    
    # Determines what interface to use
    if len(sys.argv) > 1:
        datapoints, browsers, urls, blocklist_urls, headless = userinput.get_userinput_cli()
    else:
        datapoints, browsers, urls, blocklist_urls, headless = userinput.get_user_input_gui()

    # 2. open urls with selenium and capture traffic with web proxy
    # TODO: add absolute timeout and support for browser paths
    logger.debug(browsers)
    logger.info("Start data collection")
    fqdns = datacollection.collect_fqdns(logger, urls, browsers, PROXY_IP, PROXY_PORT, REQUEST_TIMEOUT, headless)
    if fqdns is None:
        exit(1)

    logger.info("Data collection done!")
    
    # 3. separate ad/tracking domains from other domains

    # 4. use ad/tracking domain names to get data we want

    # 5. make visualizations/reports


if __name__ == "__main__":
    main()
