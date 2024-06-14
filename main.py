import re
from datetime import datetime
from netmiko import ConnectHandler
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_alarms(output):
    # Define the starting line pattern to search for
    start_pattern = r"Collecting Alarms\.\.\.\n\.*"
    start_match = re.search(start_pattern, output)

    # Check if the start pattern was found
    if not start_match:
        print("No matching start line found.")
        return "No matching start line found."

    # Define the end line pattern (can be customized if there is a specific end pattern)
    end_pattern = r"Total"
    end_match = re.search(end_pattern, output, re.MULTILINE)

    # Determine the starting index using the matched start pattern
    start_index = start_match.end()

    # Determine the end index using the matched end pattern if found
    if end_match:
        end_index = end_match.start()
    else:
        # If no specific end pattern is found, extract till the end of the document
        end_index = len(output)

    # Extract and print the desired section
    section = output[start_index:end_index]
    return section.strip()  # Remove leading/trailing whitespace

def server_side_execution(site_code):
    # site_code = "0452ML"
    site_prompt = f"{site_code}>"
    amos_string = f"amos -v com_username=rbs,com_password=rbs {site_code}"
    lt_all = "lt all"
    alt = "alt"
    st_pl = "st pl"
    st_ru = "st ru"

    net_connect = ConnectHandler(
        device_type="linux",
        ip="172.22.234.23",
        port=22,
        username="mmoyo",
        password="#Fruit720",
        # global_delay_factor = 4,
    )

    prompt = net_connect.find_prompt()
    print(prompt)

    output = net_connect.send_command(amos_string,
                                      expect_string=site_prompt,
                                      strip_prompt=False, strip_command=False,
                                      read_timeout=240
                                      )
    # print(amos_string)
    print(output)

    output += net_connect.send_command(lt_all,
                                       expect_string=site_prompt,
                                       strip_prompt=False, strip_command=False,
                                       read_timeout=240
                                       )
    # print(lt_all)
    print(output)

    try:
        start_time = datetime.now()
        output += net_connect.send_command(alt,
                                           expect_string=site_prompt,
                                           strip_prompt=False, strip_command=False,
                                           read_timeout=240
                                           )
    finally:
        runtime = f"\nSDiR execution time: {datetime.now() - start_time}\n"

        print(output)
        print(runtime)

        net_connect.disconnect()
        print('\nDisconnected.....')

    return output


extract_alarms(server_side_execution('04542ML'))
