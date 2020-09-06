##### Permissions
Make sure your user has permissions to read the i2c device. You shouldn't need to run this as root.

##### Configuring the program
You need to create a file in the same working directory, called 'config.py' with the following contents:  
```python
SENDER_EMAIL_ADDRESS = "example@example.com"
SENDER_EMAIL_PASSWORD = "examplePassword"
RECEIVER_EMAIL_ADDRESS = "example2@example2.com"
```
Recommend using some burner account you don't care about as the sender, and your real email as the receiver.

##### Run the program
`./runDryer.sh`

##### Stop the program
`./killDryer.sh`

##### Check if dryer monitor is running
`pgrep -f "python3 dryer"`
