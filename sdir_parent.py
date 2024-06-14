from datetime import datetime
from netmiko import ConnectHandler
from flask import Flask, request

app = Flask(__name__)

def server_side_execution(site_code):
    # site_code = "0452ML"
    site_prompt = f"{site_code}>"
    amos_string = f"amos -v com_username=rbs,com_password=rbs {site_code}"
    lt_all = "lt all"
    sdir = "sdir"
    st_pl = "st pl"
    st_ru = "st ru"

    net_connect = ConnectHandler(
        device_type="linux",
        ip="172.22.234.23",
        port=22,
        username="mmoyo",
        password="#Berry360",
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

    output = net_connect.send_command(lt_all,
                                      expect_string=site_prompt,
                                      strip_prompt=False, strip_command=False,
                                      read_timeout=240
                                      )
    # print(lt_all)
    print(output)

    output = net_connect.send_command(st_pl,
                                      expect_string=site_prompt,
                                      strip_prompt=False, strip_command=False,
                                      read_timeout=240
                                      )
    # print(st_pl)
    print(output)

    start_time = datetime.now()
    runtime = "00.000sec"

    try:
        start_time = datetime.now()
        output = net_connect.send_command(sdir,
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


# output = net_connect.send_command(cmd,expect_string=r'Destination filename')
# output += net_connect.send_command('\n',expect_string=r'#',delay_factor=2)