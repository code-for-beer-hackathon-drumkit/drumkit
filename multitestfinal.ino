int sensorPin0 = A0;      // input pin (+ve of piezo) 
int sensorPin1 = A1;
int sensorPin2 = A2;
int sensorValue0 = 0;     // variable to store the value coming from the sensor
int sensorValue1 = 0;
int sensorValue2 = 0;

void setup()
{
	Serial.begin(9600);     // start serial port at 9600 bps:
}

void loop()
{
	sensorValue0 = analogRead(sensorPin0);  // read the value from the sensor:
	sensorValue1 = analogRead(sensorPin1);  
	sensorValue2 = analogRead(sensorPin2); 
	
	sensorValue0= sensorValue0+1000;        // append a constant to analog value to differentiate between the sensors
	sensorValue1= sensorValue1+2000;
	sensorValue2= sensorValue2+3000;
	
	Serial.print(sensorValue0);            //print value
	//Serial.print("\n");                    //newline  
	Serial.print(sensorValue1); 
	//Serial.print("\n");
	Serial.print(sensorValue2); 
	//Serial.print("\n");
	//Serial.print("\n");  
	delay(300);                          //read from the sensors every 300 milliseconds               
}
