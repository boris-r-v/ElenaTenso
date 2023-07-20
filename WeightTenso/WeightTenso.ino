#include "KickSort.h"

#define inp_chan_1 36
#define inp_chan_2 39
#define inp_chan_3 34
#define inp_chan_4 35

void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
  
  //set the resolution to 12 bits (0-4096)
  analogReadResolution(12);
}
/*
void loop() {
  // read the analog / millivolts value for pin 2:
  int chan_1 = analogRead(inp_chan_1);
  int chan_2 = analogRead(inp_chan_2);
  int chan_3 = analogRead(inp_chan_3);
  int chan_4 = analogRead(inp_chan_4);
  
  
  Serial.printf("%d,%d,%d,%d", chan_1, chan_2, chan_3, chan_4 );
  Serial.println("");
  
  delay(1000);  
}
*/
const uint16_t window=5;
int cntr=0;
uint16_t buff[4][window];
void loop() {

  buff[0][cntr] = analogRead(inp_chan_1);
  buff[1][cntr] = analogRead(inp_chan_2);
  buff[2][cntr] = analogRead(inp_chan_3);
  buff[3][cntr] = analogRead(inp_chan_4);

  if ( ++cntr > window ){
    --cntr;
/*    int chan_1=0, chan_2=0, chan_3=0, chan_4=0;
  
    for (int i=0; i<=cntr; ++i){
      chan_1 += buff[0][cntr];
      chan_2 += buff[1][cntr];
      chan_3 += buff[2][cntr];
      chan_4 += buff[3][cntr];
      
    }
    Serial.printf("%d,%d,%d,%d\n", chan_1/cntr, chan_2/cntr, chan_3/cntr, chan_4/cntr );    
*/

    KickSort<uint16_t>::quickSort(buff[0], window);
    KickSort<uint16_t>::quickSort(buff[1], window);
    KickSort<uint16_t>::quickSort(buff[2], window);
    KickSort<uint16_t>::quickSort(buff[3], window);

    Serial.printf("%d,%d,%d,%d\n", buff[0][2], buff[1][2], buff[2][2], buff[3][2] );    

    cntr = 0;
  }
  
  delay(10);  
}
