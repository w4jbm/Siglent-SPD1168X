# Siglent-SPD1168X

This code is to support operation of the Siglent SPD1168X power supply over the Ethernet interface. It is largely based on previous work for the three channel model of supply by [Saulius Lukse](https://github.com/Kurokesu/siglent_psu_api).

I have only performed limited testing, but things seem to work as expected. For reliable operation, there should be a pause between commands that change the status of the supply (such as setting voltage or enabling the output).
