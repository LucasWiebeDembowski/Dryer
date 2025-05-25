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
The files used for the web page in the html folder of this repo. After updating them, copy the files in there into /var/www/html (assuming that's where the web server is pointing).

#### Run the program
`./runDryer.sh`

#### Stop the program
`./killDryer.sh`

#### Check if dryer monitor is running
`./dryer -l`
