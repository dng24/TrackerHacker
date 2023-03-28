import csv
import os

import pandas as pd

import plotly
import plotly.express as px

from trackerhacker.userinput import DataChoices

LIST_DELIMITATOR = ","

class Output:
    def __init__(self, logger, analysis_results: dict, output_choices: list[DataChoices], output_dir: str) -> None:
        self.logger = logger
        self.analysis_results = analysis_results
        self.output_choices = output_choices
        self.output_dir = output_dir
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            #TODO error checking



    def make_heatmap(self) -> None:
        self.logger.info("Making heatmap output...")
        
    def make_brower_comparison(self) -> None:
        self.logger.info("Making browser comparison output...")
        
        browser_nums = {}

        for source_url, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                if browser not in browser_nums.keys():
                    browser_nums[browser] = 0
                for fqdn, fqdn_info in browser_info.items():
                    browser_nums[browser] += fqdn_info["ad_tracker_count"]

        df_browser_ad_tracker_totals = pd.DataFrame()
        for browser, num_ad_trackers in browser_nums.items():
            browser_ad_tracker_series = pd.Series(dtype="object")
            browser_ad_tracker_series["Browser"] = browser
            browser_ad_tracker_series["Number of ads/trackers"] = num_ad_trackers
            df_browser_ad_tracker_totals = df_browser_ad_tracker_totals.append(browser_ad_tracker_series, ignore_index=True)

        data_represent = px.bar(df_browser_ad_tracker_totals, x="Browser", y="Number of ads/trackers")
        plotly.offline.plot(data_represent, filename=os.path.join(self.output_dir, "browser_comparison.html"))




    def make_csv_output(self) -> None:
        self.logger.info("Making CSV output...")
        output_csv = []
        header_row = ["source_url", "browser", "ad_tracker_fqdn", "ad_tracker_count", "ip"]
        for output_choice in self.output_choices:
            header_row.append(output_choice.value["output_name"])

        output_csv.append(header_row)

        for source_url, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, fqdn_info in browser_info.items():
                    for ip in fqdn_info["ips"]:
                        row = [source_url, browser, fqdn, fqdn_info["ad_tracker_count"], ip]
                        for server_location_dict in fqdn_info["server_location"]:
                            if server_location_dict["IPv4"] == ip:
                                current_server_dict = server_location_dict

                        for output_choice in self.output_choices:
                            analysis_field_name = output_choice.value["analysis_name"]
                            output_field_name = output_choice.value["output_name"]
                            if output_field_name.startswith("server:"):
                                row.append(current_server_dict[analysis_field_name])
                            elif output_field_name.startswith("whois:"):
                                row.append(fqdn_info["whois"][analysis_field_name])

                        output_csv.append(row)

        output_csv_filename = os.path.join(self.output_dir, "output.csv")
        with open(output_csv_filename, "w", newline="") as f:
            csv_writer = csv.writer(f)
            print(output_csv)
            csv_writer.writerows(output_csv)
            #TODO error checking
            self.logger.info("CSV written to '%s'" % output_csv_filename)
            
                        
    def make_html_output(self) -> None:
        self.logger.info("Making HTML output...")
