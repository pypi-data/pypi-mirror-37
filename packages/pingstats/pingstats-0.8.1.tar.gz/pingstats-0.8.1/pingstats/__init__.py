""" Written under the MIT license. See LICENSE for more details. For authors, refer
to AUTHORS.rst.

Example Usage:
    >>> import pingstats
    >>> for pings_real, pings_average in pingstats.get_pings('google.ca'):
    ...     pingstats.plot_pings(pings_average)
    ...
    # HIPSTERPLOT OUTPUT
"""
# For authors refer to AUTHORS.rst
# PY 2 TO 3 IMPORTS
from __future__ import print_function, with_statement

# STANDARD LIBRARY PACKAGES
from subprocess import Popen, PIPE
from shutil import get_terminal_size
from os import system, name
from argparse import ArgumentParser

import time

# NON STANDARD LIBRARY PACKAGES
from hipsterplot import plot


__version__ = "0.8.1"
PROG_NAME = 'pingstats'

# PARSER CONFIG
parser = ArgumentParser(prog=PROG_NAME)

parser.add_argument('address', help='The address to ping. This could be either '
                    'a web address (i.e, "google.ca") or an IP address.')

parser.add_argument('-V', '--version', action='version',
                    version='%(prog)s {}'.format(__version__))

X_COLUMN_SCALE = 16
Y_ROW_SCALE = 6

__all__ = ['get_pings', 'plot_pings']


def _decode_line(line):
    """ Decodes a line from internal ping call, returning the connection time.

    :line: A line returned from `get_ping.process`.
    :returns: Either the return time in milliseconds (as float), -1 on timeout,
              or None.
    """
    if line.lower().count('ttl'):
        if name != "nt":
            return float(line.split('time=')[1].split(' ')[0])
        else:
            if line.count('time<'):
                return float(line.split('time<')[1].split(' ')[0].strip('<ms'))
            else:
                return float(line.split('time=')[1].split(' ')[0].strip('ms'))

    elif line.lower().count('0 received' if name != 'nt' else '100% loss'):
        return -1


def get_pings(address, times_list=[], average_times_list=[], times_list_length=20, average_times_length=200):
    """ Runs a ``subprocess.Popen`` ping object and appends either the return time
    (in milliseconds) or -1 (for a lost packet) to *return_time*, and the average of *return_time* to
    *average_return_time*.

    :address: The address to ping
    :times_list: The list to append return times to.
    :average_times_list: The list to append average return times to.
    :times_list_length: The maximum length of times_list
    :average_times_length: The maximum length of average_times_list
    :returns: The *return_time* list, the *average_return_time* list
    """
    return_times, average_return_times = times_list[:], average_times_list[:]

    while 1:
        if name != 'nt':
            process = Popen(['ping', '-c 1', address], stdout=PIPE)
        else:
            process = Popen(['ping', '-n', '1', address], stdout=PIPE)

        process.wait()
        stdout, stderr = process.communicate()
        stdout = stdout.decode('UTF-8')

        for line in stdout.splitlines():
            if len(return_times) > times_list_length:
                return_times.pop(0)

            line_value = _decode_line(line)

            if line_value is not None:
                return_times.append(line_value)

        else:  # On end of for loop, calculate average and append it
            average_return_times.append(sum(return_times) / len(return_times if return_times != 0 else 1))
            if len(average_return_times) > average_times_length:
                average_return_times.pop(0)

        yield return_times, average_return_times


def plot_pings(pings, columns=70, rows=15):
    """ Provides high level bindings to ``hipsterplot.plot`` for use with :ref:get_pings.

    :pings: A list object containing ping return times as float values, normally from :ref:get_pings
    :columns: The number of columns to draw for the plot
    :rows: The number of rows to draw for the plot
    """
    plot(pings, num_x_chars=columns, num_y_chars=rows)


def _construct_middle_line(address, columns):
    """ Builds a separator line for visual prettiness.

    :address: The address currently being sent ping requests
    :columns: The total columns of the current terminal (from ``_get_tty_size``
    :returns: The separator line in string form
    """
    right_display = '%s %s ' % (PROG_NAME, __version__)
    right_display_string = ' ping data from %s' % address

    for i in range(columns - (len(right_display) + len(right_display_string))):
        right_display += '-'
    right_display += right_display_string

    return right_display


def _output_top_status(address, y, columns):
    """ Outputs a status line based on standard *y* collection.

    :address: The address currently being sent ping requests
    :y: The python list tracking ping data
    :columns: The total columns of the current terminal (from ``_get_tty_size``
    :returns: None. Instead, prints data to terminal
    """
    if y.count(-1) == 1:
        print('1 packet dropped of %s'.center(columns) % len(y))
    elif y.count(-1) > 1:
        print('%s packets dropped of %s'.center(columns)
              % (y.count(-1), len(y)))
    else:
        print('Displaying %s total packets from %s'.center(columns)
              % (len(y), address))


def _output_average_status(address, y_average, columns):
    """ Outputs a status line based on standard *y* collection.

    :address: The address currently being sent ping requests
    :y_average: The python list tracking average ping data
    :columns: The total columns of the current terminal (from ``_get_tty_size``
    :returns: None. Instead, prints data to terminal
    """
    if sum(y_average) / len(y_average) < 0:
        print('Connection dropped!'.center(columns))
    else:
        print('Displaying the average of %s total packets from %s'.center(columns)
              % (len(y_average), address))


def _run():
    """ Actually runs the logic. Uses ``subprocess.Popen`` to run system ``ping``
    and plots the results to ``hipsterplot.plot``.

    :address: A system ``ping`` compatible address, either web or IP.  """
    parsed = parser.parse_args()

    print('Waiting for first ping...')  # Notify user in case of high ping

    try:
        for ping_now, average_ping in get_pings(parsed.address):
            time_start = time.time()

            if time.time() - time_start < 0.5:  # Wait for time if no time elapsed
                time.sleep(0.5 - (time.time() - time_start))

            system('clear' if not name == 'nt' else 'cls')

            columns, rows = get_terminal_size()

            # Write current plot
            plot(ping_now, num_x_chars=columns - X_COLUMN_SCALE,
                 num_y_chars=int((rows - Y_ROW_SCALE) / 2))

            _output_top_status(parsed.address, ping_now, columns)

            # write middle
            print(_construct_middle_line(parsed.address, columns))

            # write average plot
            plot(average_ping, num_x_chars=columns - X_COLUMN_SCALE,
                 num_y_chars=int((rows - Y_ROW_SCALE) / 2))

            _output_average_status(parsed.address, average_ping, columns)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
        _run()
    except KeyboardInterrupt:
        pass
