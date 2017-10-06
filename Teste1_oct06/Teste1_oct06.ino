unsigned long t;
unsigned long tmp;

unsigned long times[10];
const int sensorPin=0;
const int ledPin=13;
const int threshold=30;
int i = 0;

void setup()
{
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}
void loop()
{
  
  if(i==10)
  {
    //print array
    Serial.println(times[0]);
    Serial.println(times[1]);
    Serial.println(times[2]);
    Serial.println(times[3]);
    Serial.println(times[4]);
    Serial.println(times[5]);
    Serial.println(times[6]);
    Serial.println(times[7]);
    Serial.println(times[8]);
    Serial.println(times[9]); 
    i = 0; 
    delta_order();
     
  }
  
  int val= analogRead(sensorPin);

  if (val >= threshold)
  { 
      digitalWrite(13,1);
      times[i] = millis();
      delay(30);
      i++;
      /*
      tmp=times[i-1];
      Serial.print("Time Elapsed: ");
      times[i] = millis();
      delta[i]=times[i]-tmp;
      Serial.println(delta[i]);
      digitalWrite(ledPin, HIGH);
      delay(2);  //delay 50
      digitalWrite(ledPin, LOW);
      */
      digitalWrite(13,0);
  }
  
}
void delta_order()
{
  unsigned long delta[9];    
  int k;
  for(k=0;k<9;k++)
  {
    delta[k] = times[k+1]-times[k];
  }
    Serial.println(delta[0]);
    Serial.println(delta[1]);
    Serial.println(delta[2]);
    Serial.println(delta[3]);
    Serial.println(delta[4]);
    Serial.println(delta[5]);
    Serial.println(delta[6]);
    Serial.println(delta[7]);
    Serial.println(delta[8]);
 }
