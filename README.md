## Dryer Monitor and Alarm
Python script that runs on a Raspberry Pi. It uses readings from an I2C accelerometer to detect when the dryer starts, and notifies the user when the dryer finishes by playing a sound through a speaker and sending an email.

The dryer monitor will notify the user if the dryer stops after having run for some minimum period of time. That minimum run period is hardcoded in dryermonitor.py.

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
Make sure /home/dairine/code/dryer/Alarm.mp3 exists.
##### Web page
The files used for the web page are in the html folder of this repo. After updating them, copy the files in there into /var/www/html (assuming that's where the web server is pointing).

#### Run the program
`./runDryer.sh`

#### Stop the program
`./killDryer.sh`

#### Check if dryer server is running and if the dryer monitor loop is running.
`./dryer -l`  
Run `./dryer --help` for more options. Alternatively:  
##### Run the program
`./runDryer.sh`

##### Stop the program
`./killDryer.sh`
