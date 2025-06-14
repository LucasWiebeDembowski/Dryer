## Dryer Monitor and Alarm
Python script that runs on a Raspberry Pi. It uses a 3rd party library to read an ADXL345 I2C accelerometer, and then detect when the dryer starts, and it notifies the user when the dryer finishes by playing a sound through a speaker and sending an email.

The dryer monitor will notify the user if the dryer stops after having run for some minimum period of time. That minimum run period is hardcoded in dryermonitor.py.

There's also a web page running on the Raspberry Pi which you can access in a web browser on another machine in your local network that displays the status of the dryer monitor, whether the dryer is on, and how long it has been on for. It also has buttons to enable and disable the dryer monitor.

#### Dependencies
`sudo apt install python3 mpg123 apache2 php`  
Follow installation instructions at https://github.com/adafruit/Adafruit_CircuitPython_ADXL34x

#### Permissions
Make sure your user has permissions to read the i2c device. You shouldn't need to run this as root.

#### Configuring the program
##### Email
You need to create a file in the same working directory, called 'config.py' with the following contents:  
```python
SENDER_EMAIL_ADDRESS = "example@example.com"
SENDER_EMAIL_PASSWORD = "examplePassword"
RECEIVER_EMAIL_ADDRESS = "example2@example2.com"
```
Obviously storing your email password in plaintext is insecure. Recommend using some burner account you don't care about as the sender, and your real email as the receiver. TODO store secrets securely.  
##### Alarm sound
Make sure /usr/local/share/dryer/Alarm.mp3 exists.
##### Web page
The files used for the web page are in the html folder of this repo. After updating them, copy the files in there into  
/var/www/html (assuming that's where the web server is pointing).

#### How to check if dryer server is running and if the dryer monitor loop is running:
`./dryer -l`  

Run `./dryer --help` for more options. For example:  
##### Run the program
`./dryer --run`

##### Stop the program
`./dryer --kill`
