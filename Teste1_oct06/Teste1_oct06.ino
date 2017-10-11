unsigned long t;
unsigned long tmp;

unsigned long times[7];
unsigned long key[7];
unsigned long delta;
unsigned long deltaA;
unsigned long deltaTimes[6];
unsigned long deltaKey[6];
const int sensorPin=A0;
const int ledPin=13;
const int threshold=50;
int i=0;
boolean trial=false;

void setup()
{
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}
void loop()
{
  delay(2000);
  // Primeiro vamos registar a chave de abertura
  Serial.println("A registar a chave de acesso");
  register_key();
  
  Serial.println("Chave de autenticacao guardada com sucesso");
  Serial.println("A adequar a chave de autenticacao");
 
  int k;
  
   for(k=0;k<7;k++)
    {
      deltaKey[k] = key[k+1]-key[k];
    }
  //  delay(1000);
   Serial.println("Chave de autenticacao devidamente guardada...");
   Serial.println();
   //delay(1000);
  Serial.println("A tentar o acesso...");  
  int val= analogRead(sensorPin);

  i=0;
  while(i<7){
    int val= analogRead(sensorPin);
      if (val >= threshold)
      { 
          digitalWrite(13,1);
          
            times[i] = millis();
          
          delay(50);
          i++;
          digitalWrite(13,0);
          }
  }
   Serial.println("A adequar a chave introduzida");
   //deltaTimes=delta_order(times);
   for(k=0;k<7;k++)
    {
      deltaTimes[k] = times[k+1]-times[k];
    }
    //Serial.println(sizeof(deltaTimes));
    //Serial.println(sizeof(deltaKey));
   Serial.println("Chave introduzida devidamente guardada...");
   Serial.println();

   Serial.println("A comparar...");
                         //compareArrays(deltaKey,deltaTimes);
                          int flagEqual=0;
                        
                       for(i=0 ; i<6 ; i++){
                        //Serial.println("entrou");
                        Serial.println(i);
                          if(deltaTimes[i]<0.8*deltaKey[i] || deltaTimes[i]>1.2*deltaKey[i]){  // Consideramos margem de 10%, fora dessa margem considera os toques diferentes.
                            flagEqual=1;
                            Serial.println("Outside Gap");
                            delay(100);
                          }
                          
                          if(flagEqual==1){
                            break;
                            //Serial.println("break");
                            }
                        }

                        if(flagEqual==0){
                            Serial.println(" *************** WELCOME ***************** ");
                        }else
                        {
                          Serial.println(" You shall not pass!!!!!!!!!!!! ");
                          }
  
   Serial.println("_______________________________END____________________________________");

}

/*unsigned long delta_order(unsigned long vecTime[]) //vecTime ora e com a autenticação ora com a chave introduzida
{
  unsigned long vecDelta[9];    
  int k;
  for(k=0;k<sizeof(vecTime);k++)
  {
    vecDelta[k] = times[k+1]-times[k];
  }
    Serial.println(vecDelta[0]);
    Serial.println(vecDelta[1]);
    Serial.println(vecDelta[2]);
    Serial.println(vecDelta[3]);
    Serial.println(vecDelta[4]);
    Serial.println(vecDelta[5]);
    Serial.println(vecDelta[6]);
    Serial.println(vecDelta[7]);
    Serial.println(vecDelta[8]);

    return vecDelta;
}*/
/*void compareArrays(unsigned long deltaKey[], unsigned long deltaTimes[])
{
  int flagEqual=0;
  
  for(i=0 ; i<10 ; i++){
    if(deltaTimes[i]<0.99*deltaKey[i] && deltaTimes[i]>1.01*deltaKey[i]){  // Consideramos margem de 10%, fora dessa margem considera os toques diferentes.
      flagEqual=1;
    }
    
    if(flagEqual==1)
    break;
  }
  Serial.println(sizeof(deltaKey));
  Serial.println(sizeof(deltaTimes));
  if(flagEqual==0){
      Serial.println(" *************** WELCOME ***************** ");
  }else
  {
    Serial.println(" You shall not pass!!!!!!!!!!!! ");
    }
  
}
*/

void register_key()
{
   digitalWrite(13,1);
   delay(50);
   digitalWrite(13,0);
   delay(50);
   digitalWrite(13,1);
   delay(50);
   digitalWrite(13,0);
   delay(50);
   digitalWrite(13,1);
   delay(50);
   digitalWrite(13,0);
   delay(50);
  
   
  i=0;
  while(i<7){ // Estou a testar com uma chave de 6 pancadas
       
    int val = analogRead(sensorPin);
     if (val >= threshold)
     { 
        digitalWrite(13,1);
        key[i] = millis(); 
        delay(50);
        digitalWrite(13,0);
        i++;
        Serial.println(i);
     }
    
  }
}
