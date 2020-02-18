# https://github.com/adafruit/Adafruit_CircuitPython_ADXL34x
# https://www.youtube.com/watch?v=NPTK0inTldw
# sudo i2cdetect -y 1


import time
import board
import busio
import numpy as np
import adafruit_adxl34x

import smtplib
import config
from datetime import datetime

class Email:
    def __enter__(self):
        return self
    def __init__(self, address, password):
        self.address = address
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.ehlo()
        self.server.starttls()
        self.server.login(address, password)
    def send_email(self, destAddress, subject, msg):
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        print("Sending email...")
        self.server.sendmail(self.address, destAddress, message)
    def __exit__(self, type, value, traceback):
        self.server.quit()

def send_email():
    subject = "Message from Spot: " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = """The dryer has stopped."""
    try:
        with Email(config.EMAIL_ADDRESS, config.PASSWORD) as email:
            email.send_email("lwiebedembowski@gmail.com", subject, msg)
    except Exception as e:
        print("Email failed to send.")
        print(e)

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

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
RUNNING_THRESHOLD = 2 # mean deviation is about 0.5 when the dryer isn't running, and 20-25 when it is running.

# Compute initial N values and determine if the dryer is running or not.

N = 100
asquaredVals = np.fromiter((squared_length(sample_acceleration(accelerometer, 0.01)) for i in range(N)), float, N)
avg = np.average(asquaredVals)
prev_running = mean_abs_dev(asquaredVals, avg) > RUNNING_THRESHOLD

# Start main loop

startTime = time.time_ns()
while True:
    asquaredVals[N - 1] = squared_length(sample_acceleration(accelerometer, 0.1))
    avg = rolling_average(N, avg, asquaredVals[N - 1], asquaredVals[0])
    meanDev = mean_abs_dev(asquaredVals, avg)

    # print("%10f" %(meanDevVals[N-1]))
    running = meanDev > RUNNING_THRESHOLD
    
    # Reset the timer when you start the dryer.
    if running and not prev_running:
        startTime = time.time_ns()

    # To avoid potential email spam as meanDevVals[N - 1] slowly crosses RUNNING_THRESHOLD,
    # only send email if dryer was running for at least 10 seconds.
    if time.time_ns() - startTime > 10*1000000000 and not running and prev_running:
        print("Dryer has stopped.")
        send_email()

    prev_running = running
    asquaredVals = np.roll(asquaredVals, -1)
