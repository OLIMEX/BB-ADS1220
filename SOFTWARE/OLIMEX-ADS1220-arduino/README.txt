This archive contains an Arduino IDE example for Olimex BB-ADS1220. A host board is required. Jumper wires to establish proper connection are required. A 0.1" step breadboard would be of great help.

In our setup OLIMEXINO-32U4 was used. We also used Arduino IDE v1.6.2.  

The example prints the voltages that are provided to analog input pin AIN0 over the console terminal of Arduino IDE. The communication protocol between BB-ADS1220 and the host boards is SPI.

Before compiling the project proper hardware connections have to be established. This is really easy if you have a 0.1" step breadboard like BREADBOARD-1.

The hardware connections are quite easy to establish when you are looking at the board's schematic. Make sure to have the schematic in front of you when establishing the hardware connections:

AVSS - GND(-)
AIN0 - analog input pin - provide up to 2.048V (!) voltage source to be measured and displayed
AIN1 - n.c.
AIN2 - n.c.
AIN3 - n.c.
AVDD - +3.3V(+)
REFP - n.c.
REFN - n.c.

VDD	 - +3.3V
DRDY#- to D4 on Olimexino
CS#	 - CS# on UEXT.10
CLK	 - SCK on UEXT.9
DIN  - MOSI on UEXT.8
DOUT - MISO on UEXT.7
GND  - GND(-)
AVSS - GND(-)

Make sure that you have made proper hardware connection between BB-ADS1220 and your main board. Do not provide more than 2.048V to AIN0 - this can damage the board.

To use this example you would need to first close Arduino IDE. Then copy the two folders "libraries" and "examples" to the main installation folder of the Arduino IDE (the folder that contains "arduino.exe"). Select to merge the folders - the folders provided contain only additional files, no changes to your previous libraries or examples would be performed. At this point you can start Arduino IDE and go to File -> Examples -> Olimex ADS1220 -> ads1220_demo. Remember to select the proper board and port in the "Tools". Compile the project and upload to the board. Provide voltage up to 2.048V to AIN0. Open either the Arduino "Serial Monitor" from Tools -> Serial monitor or a favourite terminal program - the voltage that you provided to the board would be measured and printed.

June, 2015
