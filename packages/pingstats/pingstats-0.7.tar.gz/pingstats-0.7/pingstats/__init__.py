# Written under the MIT license. See LICENSE for more details
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


__version__ = "0.7"
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


""" DISCUSSION:
    `get_pings` could very easily be a generator. This would bypass the need to
    pass it a both y lists. (The user could optionally provide those lists as kwargs)

    For example:
        >>> for pings_now, average_pings in pingstats.get_pings('google.ca')
        ...     pingstats.plot_pings(average_pings)
        ... # OUTPUT OF HIPSTERPLOT

    This provides a much simpler method of access, and looks much cleaner.

    This would require overhauling the source to ensure generator compatibility,
    but should be relatively simple. Maybe a V0.8 and above feature?

    Could be implemented by putting existing `get_pings` data in an infinite while
    loop with a yield instead of a return statement. Would need to add logic to use
    either generator constructed lists or user provided (at time of construction)
    lists.
"""


def get_pings(address, y, y_average):
    """ Runs a ``subprocess.Popen`` ping object and appends either the return time
    (in milliseconds) or -1 (for a lost packet) to *y*, and the average of *y* to
    *y_average*.

    :address: The address to ping
    :y: A python list object to store ping data
    :y_average: A python list object to store data on the average connections
    :returns: The *y* list, the *y_average* list
    """
    # temp_file = NamedTemporaryFile()
    # data_buffer = StringIO()
    if name != 'nt':
        process = Popen(['ping', '-c 1', address], stdout=PIPE)
    else:
        process = Popen(['ping', '-n', '1', address], stdout=PIPE)

    process.wait()
    stdout, stderr = process.communicate()
    stdout = stdout.decode('UTF-8')

    for line in stdout.splitlines():
        if len(y) > 20:
            y.pop(0)

        if line.lower().count('ttl'):
            if name != "nt":
                y.append(float(line.split('time=')[1].split(' ')[0]))
            else:
                if line.count('time<'):
                    y.append(float(line.split('time<')[1].split(' ')[0].strip('<ms')))
                else:
                    y.append(float(line.split('time=')[1].split(' ')[0].strip('ms')))

        elif line.lower().count('0 received' if name != 'nt' else '100% loss'):
                y.append(-1)

    else:
        y_average.append(sum(y) / len(y if y != 0 else 1))
        if len(y_average) > 200:
            y_average.pop(0)

    return y, y_average


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


def run():
    """ Actually runs the logic. Uses ``subprocess.Popen`` to run system ``ping``
    and plots the results to ``hipsterplot.plot``.

    :address: A system ``ping`` compatible address, either web or IP.  """
    parsed = parser.parse_args()
    y = []
    y_average = []

    print('Waiting for first ping...')  # Notify user in case of high ping

    try:
        while 1:
            time_start = time.time()

            get_pings(parsed.address, y, y_average)

            if time.time() - time_start < 0.5:  # Wait for time if no time elapsed
                time.sleep(0.5 - (time.time() - time_start))

            system('clear' if not name == 'nt' else 'cls')

            columns, rows = get_terminal_size()

            # Write current plot
            plot(y, num_x_chars=columns - X_COLUMN_SCALE,
                 num_y_chars=int((rows - Y_ROW_SCALE) / 2))

            _output_top_status(parsed.address, y, columns)

            # write middle
            print(_construct_middle_line(parsed.address, columns))

            # write average plot
            plot(y_average, num_x_chars=columns - X_COLUMN_SCALE,
                 num_y_chars=int((rows - Y_ROW_SCALE) / 2))

            _output_average_status(parsed.address, y_average, columns)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass
