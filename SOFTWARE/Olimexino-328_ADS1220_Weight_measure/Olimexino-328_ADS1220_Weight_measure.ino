/*********************************************************************************************************
 Sample demo software for Olimexino-328 rev.C with weight sensor (SNS-WS50KG)
 and BB-ADS1220 module connected to the SPI pins of the UEXT.
 In order to work properly the pins must be connected as shown below.
 The project is tested with Arduino IDE 1.6.5.

 Note: On this illustration:
 - the asterisk sign (*) means there is a junction between the crossed lines.
 - the plus sign (+) means the crossed lines ARE NOT CONNECTED!


Weight sensor               BB-ADS1220                          Olimexino-328     
SNS-WS50KG                                                         (UEXT)         
                                                              pin   UEXT   arduino
                                                              fun    pin     pin  
white ----*---------*----------------------------------|                          
          |         |                                  |                          
          |         |  |------------------|            |                          
          |     |---+--|AVSS           VDD|------------*----  3.3V    1           
        1Kohm   |   |  |                  |                                       
          |     |   *--|IN0          ~DRDY|                                       
          |     |   |  |                  |                                       
          *-----+---+--|IN 1           ~CS|-----------------  ~CS    10     (D7)  
          |     |   |  |                  |                                       
red   ----+-----+---+--|IN 2           CLK|-----------------  SCK     9     (D13) 
          |     |   |  |                  |                                       
        1Kohm   *---+--|IN 3           DIN|-----------------  MOSI    8     (D11) 
          |     |   |  |                  |                                       
black ----*-----|   |--|AVDD          DOUT|-----------------  MISO    7     (D12) 
          |            |                  |                                       
          |            |REFP0          GND|-----------------  GND     2           
         GND           |                  |                                       
                       |REFN0         AVSS|                                       
                       |------------------|                                        


If connected properly when you program the Olimexino board with this software,
on the Serial monitor you will see received data from the ADS1220 with interval
determined by the macro INTERVAL (in milliseconds).
The three bytes of data will be shown on different lines.

You can find detailed information about the ADS1220 module on the datasheet provided on our website:
https://www.olimex.com/Products/Breadboarding/BB-ADS1220/resources/ads1220.pdf

Date:  2015/12/10
*********************************************************************************************************/

#include <SPI.h>
#include <String.h>

const int chipSelectPin = 7;

#define CS_OUT()  pinMode(chipSelectPin, OUTPUT)
#define CS(Val)   digitalWrite (chipSelectPin, Val)

#define INTERVAL  1000  // ms
#define RECEIVED_BYTES  3
unsigned char Data[RECEIVED_BYTES], i;
char Buff[20];

void setup()
{
  Serial.begin(9600);

  // start the SPI library:
  SPI.begin();
  // configure the SPI - ADS1220 module works ONLY in SPI_MODE1! (datasheet page 33)
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE1));

  // initalize the chip select pins:
  CS_OUT();
  CS(HIGH);

  // initialize the module in resistive bridge management mode
  CS(LOW);
  SPI.transfer(0x43); // trigger write to registers command, from address 0, 4 (3+1) bytes - datasheet page 35, table 14
  // Resistive bridge management mode - datasheet page 57, table 26 (values and description of the values)
  // set the four registers (pages 38-42)
  SPI.transfer(0x3E); // register 0x00
  SPI.transfer(0x04); // register 0x01
  SPI.transfer(0x98); // register 0x02
  SPI.transfer(0x00); // register 0x03
  CS(HIGH);
}

void loop()
{
  // start conversion
  CS(LOW);
  SPI.transfer(0x08); // trigger start conversion, datasheet page 35
  CS(HIGH);

  // read data
  CS(LOW);
  SPI.transfer(0x10); // trigger read data command, datasheet page 35
  for (i=0; i<RECEIVED_BYTES; i++)
    Data[i] = SPI.transfer(0);
  CS(HIGH);

  // print data
  for (i=0; i<RECEIVED_BYTES; i++)
  {
    sprintf (Buff, "Byte[%d] = %d\n", i, Data[i]);
    Serial.print (Buff);
  }
  Serial.println ();

  // few milliseconds delay before next reading
  delay (INTERVAL);
}

