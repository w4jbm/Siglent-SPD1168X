# Siglent-SPD1168X

This Python code is to support operation of the Siglent SPD1168X power supply over the Ethernet interface. It is largely based on previous work for the three channel model of the supply developed by [Saulius Lukse](https://github.com/Kurokesu/siglent_psu_api).

I have only performed limited testing, but things seem to work as expected. For reliable operation, there should be a pause between commands that change the status of the supply (such as setting voltage or enabling the output).

```
$ python3 example.py 
Fetching system identification...
{'manufacturer': 'Siglent Technologies', 'model': 'SPD1168X', 'sn': 'SPD13DCC5R0279', 'firmware_ver': '2.1.1.8', 'hadrware_ver': 'V1.0'}

Fetching system status...
{'status': '0x10', 'mode': 'CV', 'output': 'on', 'wire_mode': '2W', 'timer': 'off', 'display': 'digital'}

Voltage: 5.001 volts, Current: 0.032 amps.
```
