# Copyright (c) 2013-2018 Ardexa Pty Ltd
#
# This code is licensed under the MIT License (MIT).
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

# This script will query a Kaco Solar inverter. Usage: python kaco-ardexa.py {serial device} {Addresses} {log directory} {debug type}, where...
# {serial device} = ..something lie: /dev/ttyS0
# {Addresses} = As a range (eg; 1-32) or a list (eg; 2,5,7,9) of the RS485 address
# {log directory} = logging directory
# {debug type} = 0 (no messages, except errors), 1 (discovery messages) or 2 (all messages)
# eg: sudo python kaco-ardexa.py /dev/ttyS0 17-20 /opt/ardexa/kaco/logs 1
# eg; sudo python kaco-ardexa.py /dev/ttyS0 2,4,7,9 /opt/ardexa/kaco/logs 1
#
# For use on Linux systems
# Make sure the following tools have been installed
#        sudo apt-get install python-pip
#        sudo pip install pyserial
#

from __future__ import print_function
import sys
import time
import os
import serial
import click
import ardexaplugin as ap

DEBUG = 0

# Change these 3 settings to suit your installation, if required
PIDFILE = 'kaco-ardexa.pid'
USAGE = "python kaco-ardexa.py {serial device} {addresses} {log directory} {debug type} eg; python kaco-ardexa.py /dev/ttyS1 1 13 /opt/ardexa/kaco 1"

# These values are the Kaco Status Codes
TL300_STATUS_CODES = {'0': 'start', '1': 'self-test', '2': 'shutdown', '3': 'constant voltage', '4': 'mpp-track', '5': 'mpp-no-track',
                      '6': 'wait-feed-in', '7': 'wait-self-test', '8': 'test-relays', '10': 'over-temperature', '11': 'excess-power',
                      '12': 'overload-shutdown', '13': 'overvolts-shutdown', '14': 'grid-fail', '15': 'night', '18': 'RCD-shutdown',
                      '19': 'insulation-error', '30': 'measure-error', '31': 'RCD-error', '32': 'self-test error', '33': 'feedin-error',
                      '34': 'comms-error', '-999': 'no-response'}

TL300_HEADER = "# datetime, status, DC Voltage MPPT1, DC Current MPPT1, DC Power MPPT1, DC Voltage MPPT2, DC Current MPPT2, DC Power MPPT2, DC Voltage MPPT3, DC Current MPPT3, DC Power MPPT3, AC Voltage phase 1, AC Current phase 1, AC Voltage phase 2, AC Current phase 2, AC Voltage phase 3, AC Current phase 3, DC Power total, AC Power total, cos phi, Circuit board temperature, Daily yield\n"
KACO = 'kaco'
KACO_TYPES = ['300TL', '375TL', '390TL', '600TL']

#~~~~~~~~~~~~~~~~~~~   START Functions ~~~~~~~~~~~~~~~~~~~~~~~

def open_serial_port(serial_dev):
    """Open the serial port and flush the buffers"""
    # open serial port
    serial_port = serial.Serial(port=serial_dev, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)
    # Flush the inputs and outputs
    serial_port.flushInput()
    serial_port.flushOutput()

    return serial_port


def read_inverter(inverter_addr, serial_port):
    """Attempt to read data from the inverter"""
    # Flush the inputs and outputs
    serial_port.flushInput()
    serial_port.flushOutput()

    # Kaco inverter expects a '#{inv_Numb}\r' command to get data
    inv_command = '#' + inverter_addr + '0\r'

    # Encode the command
    enc_cmd = inv_command.encode()
    if DEBUG:
        print("Sending the command to the RS485 port: {} encoded as: {}".format(inv_command.replace('\r', ''), enc_cmd))
    serial_port.write(enc_cmd)

    # wait 1 second. Do not make it less than that
    time.sleep(1)

    # read answer line
    response = ''
    while serial_port.in_waiting > 0:
        part = serial_port.read(serial_port.in_waiting)
        response += part

    if DEBUG > 2:
        print("Received the following data: {}".format(response.replace('\r', '\n')))

    return response


def write_line(raw_line, inverter_addr, base_directory):
    """Parse the values returned by the inverter and write them to file"""
    # Find the start token
    start_index = raw_line.find('n ')
    if start_index == -1:
        print("Could not find the start token for {}".format(inverter_addr))
        return False

    # Extract everything from the index.
    sub_string = raw_line[start_index:]

    # Split everything into an array using spaces
    items = sub_string.split()
    # Check that the first token is as required
    if items[0] != 'n':
        print("Line seems to be corrupted")
        return False

    # items[1] tells you how many elements to expect AFTER that element. Get rid of everything after that.
    # items[2] tells you the inverter type
    # Discard item[0]
    num_elements = items[1]
    inverter_type = items[2]
    try:
        noe = int(num_elements)
    except:
        if DEBUG > 1:
            print("Could not convert some elements of the raw string into numbers")
        return False

    # Check that the list contains at least noe items
    if len(items) < noe:
        if DEBUG > 1:
            print("Some elements appear to be missing from the inverter raw data")
        return False

    del items[:3]
    # Reduce the number of elements by 1
    noe = noe - 1
    del items[noe:]
    # Get rid of the CRC (last element)
    items.pop()

    if DEBUG > 1:
        print("Raw inverter line list: {}".format(items))

    if inverter_type in KACO_TYPES:
        inverter_line = kaco_tl300(items)
        header_line = TL300_HEADER
    else:
        print("This inverter type is not (yet) supported")
        return False

    if DEBUG:
        print("Address: {}, Inverter line: {}".format(inverter_addr, inverter_line))

    inverter_line = inverter_line + '\n'

    # Write the log entry, as a date entry in the log directory
    date_str = time.strftime("%Y-%m-%d")
    log_filename = date_str + ".csv"
    log_directory = os.path.join(base_directory, inverter_addr)
    ap.write_log(log_directory, log_filename, header_line, inverter_line, DEBUG, True, log_directory, "latest.csv")

    return True


# This function converts a list of objects into a string, based on the specific inverter type
# The inverter type supported in here are as per the KACO_TYPES list
# Eg; ['4', '494.4', '1.60', '794', '500.6', '1.55', '782', '406.1', '1.15', '471', '233.1', '2.98', '232.9', '3.15', '233.9', '3.18', '2049', '1545', '1.000', '32.6', '1906']
def kaco_tl300(item_list):
    """Convert the array to the final output string"""
    # convert status to a string, if you can
    if item_list[0] in TL300_STATUS_CODES:
        item_list[0] = TL300_STATUS_CODES[item_list[0]]

    # Add datetime
    datetime = ap.get_datetime_str()
    item_list.insert(0, datetime)

    # NOTE: Don't need the csv module, since the data is all controlled by this function
    inverter_line = ','.join(item_list)

    return inverter_line


#~~~~~~~~~~~~~~~~~~~   END Functions ~~~~~~~~~~~~~~~~~~~~~~~

@click.group()
@click.option('-v', '--verbose', count=True)
def cli(verbose):
    """Command line entry point"""
    global DEBUG
    DEBUG = verbose


@cli.command()
@click.argument('serial_device')
@click.argument('bus_addresses')
@click.argument('output_directory')
def log(serial_device, bus_addresses, output_directory):
    """Contact each inverter and log the latest readings"""
    # Check script is run as root
    if os.geteuid() != 0:
        print("You need to have root privileges to run this script, or as \'sudo\'. Exiting.")
        sys.exit(2)

    # If the logging directory doesn't exist, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Check that no other scripts are running
    pidfile = os.path.join(output_directory, PIDFILE)
    if ap.check_pidfile(pidfile, DEBUG):
        print("This script is already running")
        sys.exit(7)

    start_time = time.time()
    # Open the serial port
    serial_port = open_serial_port(serial_device)

    # This will check each inverter. If a bad line is received, it will try one more time
    # Sometimes the inverters take 4 goes at getting a good line from the RS485 line
    for inverter_addr in ap.parse_address_list(bus_addresses):
        count = 10
        # convert an address less than 10 to a leading zero
        if inverter_addr < 10:
            inverter_addr_str = "0" + str(inverter_addr)
        else:
            inverter_addr_str = str(inverter_addr)

        while count >= 1:
            # Implement a delay to give the serial line time to respond
            time.sleep(1)
            result = read_inverter(inverter_addr_str, serial_port)
            success = write_line(result, inverter_addr_str, output_directory)
            if success:
                break
            count = count - 1


    # Close the serial port
    serial_port.close()

    elapsed_time = time.time() - start_time
    if DEBUG:
        print("This request took: {} seconds.".format(elapsed_time))

    # Remove the PID file
    if os.path.isfile(pidfile):
        os.unlink(pidfile)


if __name__ == "__main__":
    cli()
