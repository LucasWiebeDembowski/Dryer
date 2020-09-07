#!/usr/bin/env python

# https://github.com/adafruit/Adafruit_CircuitPython_ADXL34x
# https://www.youtube.com/watch?v=NPTK0inTldw
# sudo i2cdetect -y 1

from emailSender import *

import time
import board
import busio
import numpy as np
import adafruit_adxl34x
import logging

# Sleep for sampleTime seconds, then return an accelerometer reading (array of three values)
def sample_acceleration(accelerometer, sampleTime):
    time.sleep(sampleTime)
    return accelerometer.acceleration

# Return the squared length of a 3-vector
def squared_length(v):
    return v[0]*v[0] + v[1]*v[1] + v[2]*v[2]

# Given a set X with |X| = prev_size and a mean of prev_avg, 
# return the average of X' (the set X with new_value appended to it.)
def incremental_average(prev_size, prev_avg, new_value):
    return (1.0 / (prev_size + 1)) * (prev_size * prev_avg + new_value)

# Given a set X with |X| = prev_size and a mean of prev_avg, 
# return the average of X'' (the set X with new_value appended to it and the oldest value deleted from X)
def rolling_average(prev_size, prev_avg, new_value, oldest_value):
    return (1.0 / prev_size) * (prev_size * prev_avg + new_value - oldest_value)

# Return the mean absolute deviation from avg of the xVals numpy array
def mean_abs_dev(xVals, avg):
    return np.sum(np.fromiter((abs(x - avg) for x in xVals), float, xVals.size)) / xVals.size

####################################################################################################
def get_dryer_logger():
    logger = logging.getLogger()
    fileHandler = logging.FileHandler("dryer.log")
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger

def run_dryermonitor():
    logger = get_dryer_logger()

    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)

    # Thresholds picked by eyeballing the graph and leaving some arbitrary margin for wiggle room.
    # Mean deviation is about 0.5 when the dryer isn't running, and 20-25 when it is running.
    RUNNING_THRESHOLD_LO = 2
    RUNNING_THRESHOLD_HI = 40

    # Compute initial N values and determine if the dryer is running or not.

    N = 100
    asquaredVals = np.fromiter((squared_length(sample_acceleration(accelerometer, 0.01)) for i in range(N)), float, N)
    avg = np.average(asquaredVals)
    prev_running = mean_abs_dev(asquaredVals, avg) > RUNNING_THRESHOLD_LO

    # Start main loop

    startTime = time.time_ns()
    while True:
        asquaredVals[N - 1] = squared_length(sample_acceleration(accelerometer, 0.1))
        avg = rolling_average(N, avg, asquaredVals[N - 1], asquaredVals[0])
        meanDev = mean_abs_dev(asquaredVals, avg)
        
        if meanDev >= RUNNING_THRESHOLD_HI:
            continue # Reject outliers caused by loading/unloading laundry, opening/closing door.

        # print("%10f" %(meanDevVals[N-1]))
        running = meanDev > RUNNING_THRESHOLD_LO
        
        # Reset the timer when you start the dryer.
        if running and not prev_running:
            logger.debug("Dryer started.")
            startTime = time.time_ns()

        # To avoid potential email spam as meanDev slowly crosses RUNNING_THRESHOLD_LO,
        # only send email if dryer stopped after running for at least MIN_RUNTIME seconds.
        MIN_RUNTIME = 60
        BILLION = 1000000000
        runtime_ns = time.time_ns() - startTime
        if runtime_ns > MIN_RUNTIME*BILLION and not running and prev_running:
            msg = f"Dryer stopped afer {runtime_ns / BILLION} seconds."
            logger.debug(msg)
            send_email(msg)

        prev_running = running
        asquaredVals = np.roll(asquaredVals, -1)

run_dryermonitor()
