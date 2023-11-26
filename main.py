from google_patent_scraper import scraper_class
import json
import os
import re
import glob
from datetime import date

def rotate_input_active(input_name, active_list):
    bup = input_name.replace(".pat", ".bak")
    print(input_name)
    os.replace(input_name, bup)
    active_file = open(input_name, "w")
    active_file.write('\n'.join(active_list))
    active_file.close()

for patent_list_file in glob.glob('*.pat'): 
    print(patent_list_file)
    patent_list = []
    with open(patent_list_file, "r+") as patent_file:
        for patent in patent_file.readlines():
            if '#' in patent:
                break
            patent_list.append(re.sub('[\s+]', '', patent.replace(',', '')))

        # ~ Initialize scraper class ~ #
        scraper = scraper_class()

        # ~ Add patents to list ~ #
        for patent in patent_list:
            scraper.add_patents(patent)

        # ~ Scrape all patents ~ #
        scraper.scrape_all_patents()

        # ~ Get results of scrape ~ #
        scrap_list = []
        patent_exp = dict()
        patent_exp_list = []
        for patent in patent_list:
            scrap = scraper.parsed_patents[patent]
            patent_exp[patent] = scrap['expiration_date']
            patent_exp_list.append((patent, scrap['expiration_date']))
            scrap_list.append(scrap)

        patent_exp_list.sort(key=lambda x: x[1])
        print(patent_exp_list)

        today = str(date.today())
        active_patent_list = []
        for p in patent_exp_list:
            if p[1] < today:
                print(p[0]+"... expired")
            else:
                #print(p[0] + "... active")
                active_patent_list.append(p[0])

        rotate_input_active(patent_list_file, active_patent_list)
