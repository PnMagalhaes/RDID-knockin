#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h> 
#include <ESP8266WiFi.h>

//DEFINES######################################################################
#define SERVO_PIN       0
#define ADC             A0
#define TIMEOUT_KNOCK   3000
#define MOSFET_SELECTOR 16
#define BUZZ            4

//VARIABLES####################################################################

// WIFI
const char* ssid     = "Redmi";     // SSID
const char* password = "";          // Password
const char* host = "192.168.43.6";  // Server IP
const int   port = 8080;            // Server Port

// READER
constexpr uint8_t RST_PIN = 15;          
constexpr uint8_t SS_PIN = 2;
String hex_string ="";

// USER BUTTON
const byte interruptPin = 5;
volatile byte interruptCounter = 0;
int numberOfInterrupts = 0;

// PIEZO
String list_knock = "";
unsigned long delta_keys[7];
bool batida = false;

// BATTERY
int bat_voltage = 3300;
int i = 0;
const int threshold=40;         // limiar da ADC para o knock
unsigned long key[10];

int k = 0;
int pos = 0;
int val = 0;

Servo door;                     // create servo object to control a servo
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() //##################################################################
{ 
  Serial.begin(115200);
  Serial.setTimeout(2000);  
  
  pinMode(ADC,OUTPUT);
  pinMode(MOSFET_SELECTOR,OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  pinMode(BUZZ,OUTPUT);
  
  attachInterrupt(digitalPinToInterrupt(interruptPin), handleInterrupt, FALLING);
 
  while(!Serial) 
  {
    // Wait for serial to initialize.
  }
  close_door();
  delay(1000);

  //ADC connected to Piezo
  digitalWrite(MOSFET_SELECTOR,1);
} 
 
void loop() //###################################################################
{  
  piezo();
    
  if(batida)
  {
    reader_ID();
    wifi_connect();
    battery_read();
    server_com();    
  }  
  delay(10);
  
} 
//############################ CLOSE DOOR #######################################
void close_door()
{
  door.attach(SERVO_PIN);
  door.write(0);
  unsigned long servo_delay = millis();
  while(millis()-servo_delay < 1000)
  {
    //wait 
  }
  door.detach();
}
//########################## OPEN DOOR ###########################################
void open_door()
{
  door.attach(SERVO_PIN);
  door.write(180);
  unsigned long servo_delay = millis();
  while(millis()-servo_delay < 1000)
  {
    //wait 
  }
  door.detach();
}
//######################### WIFI CONNECT #########################################
void wifi_connect()
{
  Serial.print("Connecting to ");
  Serial.println(ssid);  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  // Print the IP address
  Serial.println(WiFi.localIP());
}
//##################################### SERVER COM #############################################################################################
void server_com()
{
  Serial.print("server_com");
  WiFiClient client;  
  if (!client.connect(host, port)) 
  {
    Serial.println("connection failed");
    return;
  }
  String tag = hex_string;
  String num = "4";
  String loc = "\"DETI\"";
  String bat = String(bat_voltage);
  String url = "{\"type\": \"validate\" , \"rfid\": "+tag+", \"knock\": ["+list_knock+ "0] , \"door\": ["+ num + " ," + loc + " ," + bat +"] , \"seq\": 1}\n\n";
  Serial.println(url);

  //client.print(url);
  unsigned long timeout = millis();
  while (client.available() == 0) 
  {
    if (millis() - timeout > 5000) 
    {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }
  while(client.available())
  {
    String line = client.readStringUntil('\n');
    Serial.print(line);
    //{"type": 'validate',"result": "True", "seq": data["seq"]}
    if (line.substring(24) == "True") 
    {
      buzzer(3);
      open_door();
      delay(10000);
      close_door();            
    }
    else
    {
      buzzer(6);
    }
  }
  list_knock = "";  
  
}
//##################### READER ID ############################################
void reader_ID()
{
	SPI.begin();			                    // Init SPI bus
	mfrc522.PCD_Init();		                // Init MFRC522
	mfrc522.PCD_DumpVersionToSerial();
  hex_string="";
  int aux = millis();
  Serial.print("Insira o Cartão");
  while(!mfrc522.PICC_IsNewCardPresent())
  {
    if(millis()-aux>3000)
    {
      Serial.print("Reader:Timeout");
      break;
    }
    delay(100);
  }
  if(mfrc522.PICC_ReadCardSerial()) 
    {
      Serial.print("RFID TAG ID:");
      for (byte i = 0; i < mfrc522.uid.size; ++i) 
      {
        //Serial.print(mfrc522.uid.uidByte[i],HEX); // print id as hex values        
        hex_string = hex_string + String(mfrc522.uid.uidByte[i],HEX);
        //Serial.print(hex_string);
      }
      //Serial.print(hex_string);
      Serial.println(); // Print out of id is complete.
    }
}
//################################# BATTERY ######################################
int battery_read()
{
  // Comutar ADC para leitura de bateria
  digitalWrite(MOSFET_SELECTOR,0);
  int b = 0;
  int temp = 0;
  for(b=0;b<4;b++)
  {
    temp = analogRead(ADC);
    bat_voltage = bat_voltage + temp;
    delay(10);
  }
  bat_voltage = bat_voltage/4;
  bat_voltage = 1.8*(bat_voltage/1024);
  Serial.print(bat_voltage);

  // Comutar ADC para ler piezo
  digitalWrite(MOSFET_SELECTOR,1);
  return bat_voltage;
}
void handleInterrupt() 
{
  open_door();
  Serial.print("User_Button -> Opendoor"); 
}
//############################################## PIEZO ############################
void piezo()
{  
  unsigned long keys[10];
  int val = analogRead(ADC);
  delay(50);
  
  int i = 0;
  if (val >= threshold) //Recebe a 1ª pancada
  { 
    keys[i]=millis();   // Aconteceu a 1ª pancada e fica a espera da segunda
    int ikey=millis();  // Regista o instante da 1ª pancada - variavel auxiliar
    i=1;
    Serial.println(i);
    while(millis()-ikey<5000)
    {  // Compara o tempo actual com o instante da ultima pancada
      val = analogRead(ADC);
      if(val>=threshold)
      { 
        //Entra aqui quando acontecem outras pancadas
        delay(50);  //delay 50
        keys[i]=millis();
        ikey=millis();  // Actualiza nesta variavel auxiliar o instante da ultima pancada
        i++;
        Serial.println(i);
      }
      delay(50);
    }
    Serial.println("PIEZO: Batida Acabada");      
    for(k=0;k<i-1;k++)
    {
      //intervalo de tempo
      delta_keys[k] = keys[k+1]-keys[k];
      list_knock = list_knock + String(delta_keys[k]) + ",";      
      Serial.println("string");
      delay(100);
    }
    Serial.print(list_knock);   
  }
  Serial.println("PIEZO:END");
  batida = true;
}
void buzzer(int loops)
{ // Loops varia, é 1 para que se passe o cartão u é 3 se o acesso foi negado
  int i;
  for(i = 0 ; i < loops ; i++)
  {
      tone(BUZZ, 1000, 300); // Send 1KHz sound signal...
      delay(200);              // ...for 200 ms
      noTone(BUZZ);          // Stop sound...
      delay(200);              // ... for 200ms
  }
}


