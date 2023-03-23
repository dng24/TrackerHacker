import csv
import os

from trackerhacker.userinput import DataChoices

LIST_DELIMITATOR = ","

class Output:
    def __init__(self, analysis_results: dict, output_choices: list, output_dir: str):
        self.analysis_results = analysis_results
        self.output_choices = output_choices
        self.output_dir = output_dir

    def make_csv_output(self):
        output_csv_filename = os.path.join(self.output_dir, "output.csv")
        with open(output_csv_filename, "w") as f:
            csv_writer = csv.writer(f)

            header_row = ["source_url", "browser", "fqdn", "ip"]
            for output_choice in self.output_choices:
                header_row.append(output_choice.value)

            csv_writer.writerow(header_row)

            for source_url, source_url_info in self.analysis_results.items():
                for browser, browser_info in source_url_info.items():
                    for fqdn, fqdn_info in browser_info.items():
                        for ip in fqdn_info["ips"]:
                            row = [source_url, browser, fqdn, ip]
                            for output_choice in self.output_choices:
                                if output_choice == DataChoices.SERVER_LOCATION:
                                    row.append(LIST_DELIMITATOR.join)
                        
    def make_html_output(self):
        pass