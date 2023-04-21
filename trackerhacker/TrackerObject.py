from enum import Enum


OUTPUT_KEY = "output_name"
ANALYSIS_KEY = "analysis_name"

#Class that tracker hacker uses to define possible user data choices
class DataChoices(Enum):
    SERVER_COUNTRY_CODE = {OUTPUT_KEY: "server:country_code", ANALYSIS_KEY: "country_code"}
    SERVER_COUNTRY_NAME = {OUTPUT_KEY: "server:country_name", ANALYSIS_KEY: "country_name"}
    SERVER_STATE = {OUTPUT_KEY: "server:state", ANALYSIS_KEY: "state"}
    SERVER_CITY = {OUTPUT_KEY: "server:city", ANALYSIS_KEY: "city"}
    SERVER_POSTAL_CODE = {OUTPUT_KEY: "server:postal_code", ANALYSIS_KEY: "postal"}
    SERVER_LATITUTE = {OUTPUT_KEY: "server:latitude", ANALYSIS_KEY: "latitude"}
    SERVER_LONGITUDE = {OUTPUT_KEY: "server:longitude", ANALYSIS_KEY: "longitude"}
    DOMAIN_NAME = {OUTPUT_KEY: "whois:domain_name", ANALYSIS_KEY: "domain_name"}
    REGISTRAR = {OUTPUT_KEY: "whois:registrar", ANALYSIS_KEY: "registrar"}
    WHOIS_SERVER = {OUTPUT_KEY: "whois:whois_server", ANALYSIS_KEY: "whois_server"}
    REFERRAL_URL = {OUTPUT_KEY: "whois:referral_url", ANALYSIS_KEY: "referral_url"}
    UPDATED_DATE = {OUTPUT_KEY: "whois:updated_date", ANALYSIS_KEY: "updated_date"}
    CREATION_DATE = {OUTPUT_KEY: "whois:creation_date", ANALYSIS_KEY: "creation_date"}
    EXPIRATION_DATE = {OUTPUT_KEY: "whois:expiration_date", ANALYSIS_KEY: "expiration_date"}
    NAME_SERVERS = {OUTPUT_KEY: "whois:name_servers", ANALYSIS_KEY: "name_servers"}
    STATUS = {OUTPUT_KEY: "whois:status", ANALYSIS_KEY: "status"}
    DNSSEC = {OUTPUT_KEY: "whois:dnssec", ANALYSIS_KEY: "dnssec"}
    NAME = {OUTPUT_KEY: "whois:name", ANALYSIS_KEY: "name"}
    ORG = {OUTPUT_KEY: "whois:org", ANALYSIS_KEY: "org"}
    ADDRESS = {OUTPUT_KEY: "whois:address", ANALYSIS_KEY: "address"}
    WHOIS_CITY = {OUTPUT_KEY: "whois:city", ANALYSIS_KEY: "city"}
    WHOIS_STATE = {OUTPUT_KEY: "whois:state", ANALYSIS_KEY: "state"}
    WHOIS_COUNTRY = {OUTPUT_KEY: "whois:country", ANALYSIS_KEY: "country"}
    WHOIS_REGISTRANT_POSTAL_CODE = {OUTPUT_KEY: "whois:registrant_postal_code", ANALYSIS_KEY: "registrant_postal_code"}
    EMAILS = {OUTPUT_KEY: "whois:emails", ANALYSIS_KEY: "emails"}

#Object that stores user choices when running the program
class TrackerObject:
    def __init__(self, datapoints, browsers, query_urls, headless, output_dir):
        self.datapoints = datapoints
        self.browsers = browsers
        self.query_urls = query_urls
        self.headless = headless 
        self.output_dir = output_dir
