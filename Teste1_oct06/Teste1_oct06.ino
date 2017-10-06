unsigned long t;
unsigned long tmp;
unsigned long delta[10];
unsigned long times[10];
const int sensorPin=0;
const int ledPin=13;
const int threshold=1;
int i;

void setup(){
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}
void loop(){

  int val= analogRead(sensorPin);

  if (val >= threshold)
  { 
      tmp=times[i-1];
      Serial.print("Time Elapsed: ");
      times[i] = millis();
      delta[i]=times[i]-tmp;
      Serial.println(delta[i]);
      digitalWrite(ledPin, HIGH);
      delay(2);  //delay 50
      digitalWrite(ledPin, LOW);
  }
}
