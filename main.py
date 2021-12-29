import info


valid, host, mask = info.get_interface_data()
if valid is False:
    print("could not obtain intercae info")
    exit(-1)

start, end =info.calc_network_span(host, mask)
