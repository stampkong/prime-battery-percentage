#!/usr/bin/env python3

"""
This script displays the battery level of a SteelSeries Prime Wireless mouse.


USING
-----

To use this script you must install hidapi (https://github.com/trezor/cython-hidapi):

    pip3 install hidapi

and then running it using Python 3:

    python3 ./Prime.py


LICENSE
-------

        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

"""  

import hid


VENDOR_ID = 0x1038
PRODUCT_ID = 0x1369
ENDPOINT = 0

def open_device(vendor_id, product_id,endpoint):
    """Opens and returns the HID device

    .. NOTE::

       Cherry-picked from https://github.com/flozz/rivalcfg/

    :param int vendor_id: The vendor id of the device (e.g. ``0x1038``)).
    :param int product_id: The product id of the device (e.g. ``0x1710``).
    :param int endpoint: The number of the endpoint to open on the device (e.g.
                         ``0``).

    :raise DeviceNotFound: The requested device is not plugged to the computer
                           or it does not provide the requested endpoint.
    :raise IOError: The device or its interface cannot be opened (permission
                    issue, device busy,...).

    :rtype: hid.device
    """
    path = None
    device = hid.device()

    # Search the device
    for interface in hid.enumerate(vendor_id, product_id):
        if interface["interface_number"] == endpoint:
            path = interface["path"]
            break

    # Open the found device. This can raise an IOError.
    if path:
        device.open_path(path)
        return device

    # No matching device found
    raise Exception("Requested device or endpoint not found: %04x:%04x:%02x" % (  # noqa
        vendor_id, product_id, endpoint))


def get_status():
    status = {
        "transmitter_connected": False,
        "mouse_connected": False,
        "mouse_battery": 0,
        }

    try:
        device = open_device(VENDOR_ID, PRODUCT_ID, ENDPOINT)
    except Exception:
        return status

    status["transmitter_connected"] = True

    # Is mouse powered on?
    device.write(b"\x06\x18")
    data = device.read(31)
    if data[2] == 0x03:
        status["pip install hidapi_connected"] = True

    # Get battery level
    # device.write(b"\x06\x18")
    # data = device.read(31)
    # status["mouse_battery"] = data[2]

    device.close()
    print(device)
    return status


if __name__ == "__main__":


    show_device =  get_status()
    print(show_device)
    status = get_status()
    if not status["transmitter_connected"]:
        print("The transmitter is not connected or cannot be openend")
    elif not status["mouse_connected"]:
        print("The mouse is powered off")
    else:
        print("mouse is powered on")

    # battery = status["headset_battery"]
    # print("Battery [%-10s] %02i%%" % (
    #     "=" * round(battery / 10),
    #     battery
    #     ))