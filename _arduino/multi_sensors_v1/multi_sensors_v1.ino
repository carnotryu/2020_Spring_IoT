#include "Wire.h"
#include "I2Cdev.h"
#include "MPU9250.h"

MPU9250 accelgyro;
I2Cdev   I2C_M;

int mic = A0;
const int sampleTime = 3;
int micOut = 0;
int led = 0;
int touch = 0;

void getAccel_Data(void);

uint8_t buffer_m[6];

int16_t ax, ay, az;
int16_t gx, gy, gz;

float Axyz[3];
float Gxyz[3];

#define sample_num_mdate  5000

void setup()
{
    pinMode(3,INPUT);
    pinMode(4,OUTPUT);
    pinMode(5,OUTPUT);
    pinMode(13,OUTPUT);
    digitalWrite(4,led);
    digitalWrite(5,led);
    digitalWrite(13,led);
    Wire.begin();
    Serial.begin(115200);                        // 통신속도 250000 bps
    accelgyro.initialize();
}

bool data_send = true;

void loop()
{
  if (data_send)
  {
    requested();
    delay(10);
  }
}

void requested() {
  getAccel_Data();
  micOut = findPTPAmp();
  touch = digitalRead(3);
  Serial.print(abs(micOut));
  Serial.print(" ");
  Serial.print(touch);
  Serial.print(" ");
  Serial.print(Axyz[0]);
  Serial.print(" ");
  Serial.print(Axyz[1]);
  Serial.print(" ");
  Serial.print(Axyz[2]);
  Serial.print(" ");
  Serial.print(Gxyz[0]);
  Serial.print(" ");
  Serial.print(Gxyz[1]);
  Serial.print(" ");
  Serial.println(Gxyz[2]);
}

void serialEvent() {
  while (Serial.available())
  {
    char readData = (char)Serial.read();
    if (readData == '0')      digitalWrite(13, LOW);
    else if (readData == '1') digitalWrite(13, HIGH);
    else if (readData == '2') digitalWrite(4, LOW);
    else if (readData == '3') digitalWrite(4, HIGH);
    else if (readData == '4') digitalWrite(5, LOW);
    else if (readData == '5') digitalWrite(5, HIGH);
    else if (readData == 'r') data_send = true;
    else if (readData == 's') data_send = false;
  }
}


// Find the Peak-to-Peak Amplitude Function
int findPTPAmp(){
// Time variables to find the peak-to-peak amplitude
   unsigned long startTime= millis();  // Start of sample window
   unsigned int PTPAmp = 0; 

// Signal variables to find the peak-to-peak amplitude
   unsigned int maxAmp = 0;
   unsigned int minAmp = 1023;

// Find the max and min of the mic output within the 50 ms timeframe
   while(millis() - startTime < sampleTime) 
   {
      micOut = analogRead(mic);
      if( micOut < 1023) //prevent erroneous readings
      {
        if (micOut > maxAmp)
        {
          maxAmp = micOut; //save only the max reading
        }
        else if (micOut < minAmp)
        {
          minAmp = micOut; //save only the min reading
        }
      }
   }

  PTPAmp = abs(maxAmp - minAmp); // (max amp) - (min amp) = peak-to-peak amplitude
  double micOut_Volts = (PTPAmp * 3.3) / 1024; // Convert ADC into voltage

  //Uncomment this line for help debugging (be sure to also comment out the VUMeter function)
  //Serial.println(PTPAmp); 

  //Return the PTP amplitude to use in the soundLevel function. 
  // You can also return the micOut_Volts if you prefer to use the voltage level.
  return PTPAmp;   
}

void getAccel_Data(void)
{
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    Axyz[0] = (double) - ax / 16384;
    Axyz[1] = (double) - ay / 16384;
    Axyz[2] = (double) - az / 16384;
    Gxyz[0] = (double) gx * 250 / 32768;
    Gxyz[1] = (double) gy * 250 / 32768;
    Gxyz[2] = (double) gz * 250 / 32768;    
}
