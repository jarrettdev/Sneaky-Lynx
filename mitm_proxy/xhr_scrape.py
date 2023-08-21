# run mitmdump -s xhr_scrape.py
import json
import os
from urllib.parse import urlparse
from datetime import datetime


def get_substring_after_tld(url):
    parsed_url = urlparse(url)
    tld_index = parsed_url.netloc.rfind('.') # Find the last dot in the netloc part
    if tld_index != -1:
        return parsed_url.netloc[tld_index+1:] + parsed_url.path
    return '' # Return empty string if TLD is not found


def sanitize_substring(substring):
    return substring.replace(':', '_').replace('/', '_').replace('.','_').replace('www', '_').replace('https', '_').replace('http', '_').replace('?','_')


with open('../config.json', 'r') as f:
    config = json.load(f)

target_urls = config['xhr_urls']

target_strs = [target_str for target_str in target_urls]

target_str = target_strs[0]
substring_after_tld = get_substring_after_tld(target_str)
target_dir_str = sanitize_substring(substring_after_tld)
out_dir = f'output/{target_dir_str}'


# Global variable to store the last tracked URL
last_url = None


def response(flow):
    global last_url  # Declare last_url as global so we can modify it
    flow_url = flow.request.url

    if target_str in flow_url.lower():
        print(f'XHR URL: {flow_url}\n\n\n\n\n\n')
        # Parse the JSON response from the XHR request
        print(flow_url)
        response_dict = json.loads(flow.response.text)

        # Append the last tracked URL to the response_dict
        if last_url is not None:
            response_dict['tracked_url'] = last_url

        # print(response_dict)

        # Save the metadata and XHR response to a file
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        response_dict['timeOfScrape'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(f'{out_dir}/data.json', 'a') as f:
            json.dump(response_dict, f)
            f.write(',\n')




