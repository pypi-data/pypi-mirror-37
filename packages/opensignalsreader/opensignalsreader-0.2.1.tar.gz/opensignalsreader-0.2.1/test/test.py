"""
OpenSignalsReader TEST
---------------------

This skript test calls the most important functions of the OpenSignalsReader class for testing purposes.

Notes
-----
..	This skript ist not intended to be shared!
..  This skript is part of the master thesis
	"Development of an Open-Source Python Toolbox for Heart Rate Variability (HRV)".

Author
------
..  Pedro Gomes, Master Student, University of Applied Sciences Hamburg

Thesis Supervisors
------------------
..  Hugo Silva, PhD, Instituto de Telecomunicacoes, PLUX wireless biosignals S.A.
..  Prof. Dr. Petra Margaritoff, University of Applied Sciences Hamburg

Last Update
-----------
13-10-2018

"""
# Compatibility
from __future__ import print_function

# Imports
import sys
from opensignalsreader import OpenSignalsReader

# Input file data
# NOTE: In some cases, for example when not running this script within an IDE's project, it might be required change
# the relative file paths to absolute file paths in order for the files to be found.
# Example: 'SampleECG.txt' -> '/Users/sampleuser/SampleECG.txt'
BIT_DATA1 = 'SampleECG.txt'
BIT_DATA2 = 'SampleEMGECG.txt'
BIO_DATA = 'SampleBVP.txt'


# Next test function
def next_test(i):
	msg = "\n*** Press 'enter' key to proceed with the next test #%i" % i
	if sys.version_info.major < 3:
		raw_input(msg)
	else:
		input(msg)


#
# TESTS
#
print("OPENSIGNALSREADER TEST SCRIPT")
i = 1

# TEST 1: Create OpenSignals object and read file with automatic signal conversion and plot results
next_test(i)
acq = OpenSignalsReader(BIT_DATA1)
print('\nTEST %i: Loading OpenSignals file' % i)
print('Available Channels', acq.channels)
print('Available Sensors', acq.sensors)
i += 1

# TEST 2
next_test(i)
print("\nTEST %i: Accessing converted signal using sensor label:" % i)
print(acq.signal('ECG'))
i += 1

# TEST 3
next_test(i)
print("\nTEST %i: Accessing converted signal using sensor channel:" % i)
print(acq.signal(2))
i += 1

# TEST 4
next_test(i)
print("\nTEST %i: Accessing raw signal using sensor label:" % i)
print(acq.raw('ECG'))
i += 1

# TEST 5
next_test(i)
print("\nTEST %i: Accessing raw signal using sensor channel" % i)
print(acq.raw(2))
i += 1

# TEST 6
next_test(i)
print("\nTEST %i: Accessing non-existing signal using sensor channel (should raise exception)" % i)
try:
	print(acq.raw(100))
except ValueError, emsg:
	print(' --> ValueError occurred as expected. Error Message: \n%s' % emsg)

# TEST 7
next_test(i)
print("\nTEST %i: Accessing non-existing signal using sensor label (should raise exception)" % i)
try:
	print(acq.raw('EMG'))
except ValueError, emsg:
	print(' --> ValueError occurred as expected. Error Message: \n%s' % emsg)

# TEST 8
acq = OpenSignalsReader(BIT_DATA2)
print('New File:')
print('Available Channels', acq.channels)
print('Available Sensors', acq.sensors)
next_test(i)
print("\nTEST %i: Accessing multiple converted signal using sensor label:" % i)
print(acq.signal(['ECG', 'EMG']))
i += 1

# TEST 9
next_test(i)
print("\nTEST %i: Accessing multiple converted signal using sensor channel:" % i)
print(acq.signal([1, 2]))
i += 1

# TEST 10
next_test(i)
print("\nTEST %i: Accessing multiple raw signal using sensor label:" % i)
print(acq.raw(['ECG', 'EMG']))
i += 1

# TEST 11
next_test(i)
print("\nTEST %i: Accessing multiple raw signal using sensor channel" % i)
print(acq.raw([1, 2]))
i += 1

# TEST 12
next_test(i)
print("TEST %i: Load and plot converted data directly" % i)
OpenSignalsReader(BIT_DATA2, show=True)
i += 1

# TEST 13
next_test(i)
print("TEST %i: Load and plot raw data directly" % i)
OpenSignalsReader(BIT_DATA2, show=True, raw=True)
i += 1

# TEST 14
next_test(i)
print("\nTEST %i: Try to load biosignalsplux sensor data should raise an exception" % i)
try:
	OpenSignalsReader(BIO_DATA)
except ValueError, emsg:
	print(' --> ValueError occurred as expected. Error Message: \n%s' % emsg)
