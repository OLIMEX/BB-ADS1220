



#include <Protocentral_ADS1220.h>
#include <SPI.h>
#include <Wire.h>
#define OLIMEXINO_32U4


#define PGA 1
#define VREF 2.048
#define VFSR VREF/PGA
#define FSR (((long int)1<<23)-1)

volatile byte MSB;
volatile byte data;
volatile byte LSB;
volatile byte *SPI_RX_Buff_Ptr;


Protocentral_ADS1220 ADS1220;

void setup()   {

 #ifdef OLIMEXINO_32U4
    // Power Up UEXT
   pinMode(8, OUTPUT);
   digitalWrite(8, HIGH);
   delay(1000);
   digitalWrite(8, LOW);
   delay(500);
  pinMode(ADS1220_CS_PIN, OUTPUT);
  pinMode(ADS1220_DRDY_PIN, INPUT);
  
  ADS1220.begin();
 #endif   
  
  
 Serial.begin(9600);
 Serial.println("BBS-ADS1220 Demo aplication");

 }


void loop() {
    long int bit32;
  long int bit24;
  byte *config_reg;
  float Vout;
  
   SPI_RX_Buff_Ptr = ADS1220.Read_Data();
   
    if(ADS1220.NewDataAvailable = true)
  {
  ADS1220.NewDataAvailable = false;

  MSB = SPI_RX_Buff_Ptr[0];    
  data = SPI_RX_Buff_Ptr[1];
  LSB = SPI_RX_Buff_Ptr[2];

  bit24 = MSB;
  bit24 = (bit24 << 8) | data;
  bit24 = (bit24 << 8) | LSB;                                 // Converting 3 bytes to a 24 bit int
    
  /*if (MSB & 0x80)
    bit32 = (bit24 | 0xFF000000);             // Converting 24 bit two's complement to 32 bit two's complement
  else    
    bit32 = bit24;
  */
  
  bit24= ( bit24 << 8 );
  bit32 = ( bit24 >> 8 );                      // Converting 24 bit two's complement to 32 bit two's complement
  
  Vout = (float)((bit32*VFSR*1000)/FSR);     //In  mV
  }
   
Serial.print(Vout);Serial.println("mV");

  delay(500);

}


