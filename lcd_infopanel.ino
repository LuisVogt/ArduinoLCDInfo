#include <LiquidCrystal.h>
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

const int lcdColums = 16;
const int lcdLines = 2;

int nDisp0 = 0;
int nDisp1 = 1;
int nDisp2 = 12;
int nDisp3 = 13;

int backlight = 10;
int RED = 11;
int Buzzer = 3;

float vRED = 0;
float vGREEN = 0;
float vBLUE = 0;

unsigned long previousMillis = 0;

enum parsingStates
{
  initialState, //0
  ledAdjust, //1
  buzzer, //2
  pulse, //3
  bar, //4
  string, //5
  ledAdjust1,//6 
  ledAdjust2, //7
  ledAdjust3, //8
  buzzer1, //9
  pulse1, //10
  bar1, //11
  bar2, //12
  string1start, //13
  string2start, //14
  string3start, //15
  string4start, //16
  string1, //17
  string2, //18
  string3, //19
  string4, //20
  endState //21
};

byte customChar0[8] = {
  0b00000,
  0b01110,
  0b10101,
  0b10111,
  0b10001,
  0b10001,
  0b01110,
  0b00000
};

byte customChar1[8] = {
  0b00000,
  0b00000,
  0b00100,
  0b01110,
  0b10101,
  0b10001,
  0b10001,
  0b01110
};

void setup() {
  // put your setup code here, to run once:
  pinMode(nDisp0, OUTPUT);
  pinMode(nDisp1, OUTPUT);
  pinMode(nDisp2, OUTPUT);
  pinMode(nDisp3, OUTPUT);

  pinMode(RED, OUTPUT);
  pinMode(Buzzer, OUTPUT);
  pinMode(backlight, OUTPUT);

  analogWrite(backlight, 128);
  lcd.createChar(0, customChar0);
  lcd.createChar(1, customChar1);
  /*lcd.createChar(2,customChar1);
    lcd.createChar(3,customChar1);
    lcd.createChar(4,customChar1);
    lcd.createChar(5,customChar1);
    lcd.createChar(6,customChar1);
    lcd.createChar(7,customChar1);*/

  lcd.begin(lcdColums, lcdLines);
  lcd.setCursor(0, 0);
  lcd.clear();
  Serial.begin(115200);
  //Serial.setTimeout(1);
}

bool redLedPulse(int pulses, int dTime)
{
  static bool started = false;
  static int tempPulses = 0;
  static int previousValue = 0;
  static bool increase = true;
  if (started)
  {
    if (increase)
    {
      vRED += dTime * 0.255 / 0.5;
      if (vRED >= 255)
      {
        vRED = 255;
        increase = false;
      }
    }
    else
    {
      vRED -= dTime * 0.255 / 0.5;
      if (vRED <= 0)
      {
        vRED = 0;
        increase = true;
        tempPulses--;
        if (tempPulses <= 0)
        {
          vRED = previousValue;
          started = false;
          tempPulses = 0;
        }
      }
    }
  }
  else if (pulses > 0)
  {
    previousValue = vRED;
    tempPulses = pulses;
    started = true;
  }
  else
    return false;
  return true;
}

void setRGB(int r, int g, int b)
{
  Serial.println(r);
  vRED = r;
  vGREEN = g;
  vBLUE = b;
}

void binaryActivating(bool a, bool b, bool c, bool d)
{
  lcd.setCursor(2, 0);
  lcd.print(a);
  lcd.setCursor(3, 0);
  lcd.print(b);
  lcd.setCursor(4, 0);
  lcd.print(c);
  lcd.setCursor(5, 0);
  lcd.print(d);
  if (a)
    digitalWrite(nDisp3, HIGH);
  if (b)
    digitalWrite(nDisp2, HIGH);
  if (c)
    digitalWrite(nDisp1, HIGH);
  if (d)
    digitalWrite(nDisp0, HIGH);
}

void clearBinary()
{

  digitalWrite(nDisp0, LOW);
  digitalWrite(nDisp1, LOW);
  digitalWrite(nDisp2, LOW);
  digitalWrite(nDisp3, LOW);
}

void numberDisplay(int n)
{
  clearBinary();
  switch (n)
  {
    case 0:
      binaryActivating(0, 0, 0, 0);
      break;
    case 1:
      binaryActivating(0, 0, 0, 1);
      break;
    case 2:
      binaryActivating(0, 0, 1, 0);
      break;
    case 3:
      binaryActivating(0, 0, 1, 1);
      break;
    case 4:
      binaryActivating(0, 1, 0, 0);
      break;
    case 5:
      binaryActivating(0, 1, 0, 1);
      break;
    case 6:
      binaryActivating(0, 1, 1, 0);
      break;
    case 7:
      binaryActivating(0, 1, 1, 1);
      break;
    case 8:
      binaryActivating(1, 0, 0, 0);
      break;
    case 9:
      binaryActivating(1, 0, 0, 1);
      break;
  }
}

void buzz(int t)
{
  tone(Buzzer, 440, t);
}

void clearLine(int line)
{
  lcd.setCursor(0, line);
  for (int i = 0; i < lcdColums; i++)
  {
    lcd.print(" ");
  }
}

void writeArray(char* text, int n)
{
  for (int i = 0; i < n; i++)
  {
    lcd.write((int8_t)text[i]);
  }
}

void percentageBar(int percent, char symbol, char* returner)
{
  returner[0] = (int8_t)symbol;
  for (int i = 1; i < lcdColums; i++)
  {
    if ((percent * lcdColums) > (i * 100))
      returner[i] = (int8_t)255;
    else
      returner[i] = ' ';
  }
  //returner[lcdColums+1]='\0';
}

bool areTwoArraysTheSame(char* array1, char* array2, int n)
{
  for (int i = 0; i < n; i++)
  {
    if (array1[i] != array2[i])
      return false;
  }
  return true;
}

void fillArray(char* array1, int start, int finish)
{
  for (int i = start; i < finish; i++)
  {
    array1[i] = ' ';
  }
}

void copyArray(char* original, char* target, int n)
{
  for (int i = 0; i < n; i++)
    target[i] = original[i];
}

bool checkIfEmptyArray(char* str)
{
  for(int i = 0; str[i]!='\0';i++)
  {
    if(str[i]!=' ')
      return false;
  }
  return true;
}

void updateLCD(char* str1, char* str2, char* str3, char* str4)
{
  static char previousStr1[lcdColums+1];
  static char previousStr2[lcdColums+1];
  static char previousStr3[lcdColums+1];
  static char previousStr4[lcdColums+1];

  bool updateLCD = false;
/*
  if(checkIfEmptyArray(str1))
    copyArray(previousStr1, str1,lcdColums+1);
  if(checkIfEmptyArray(str2))
    copyArray(previousStr2, str2,lcdColums+1);
  if(checkIfEmptyArray(str3))
    copyArray(previousStr3, str3,lcdColums+1);
  if(checkIfEmptyArray(str4))
    copyArray(previousStr4, str4,lcdColums+1);
*/  
  if (!areTwoArraysTheSame(str1, previousStr1, lcdColums+1)){
    updateLCD = true;
    clearLine(0);
  }
  if (!areTwoArraysTheSame(str2, previousStr2, lcdColums+1)){
    updateLCD = true;
    clearLine(1);
  }
  if (!areTwoArraysTheSame(str3, previousStr3, lcdColums+1)){
    updateLCD = true;
    clearLine(2);
  }
  if (!areTwoArraysTheSame(str4, previousStr4, lcdColums+1)){
    updateLCD = true;
    clearLine(3);
  }
  
  copyArray(str1, previousStr1, lcdColums+1);
  copyArray(str2, previousStr2, lcdColums+1);
  copyArray(str3, previousStr3, lcdColums+1);
  copyArray(str4, previousStr4, lcdColums+1);

  if (updateLCD)
  {
    //lcd.clear();
    if (lcdLines >= 1)
    {
      lcd.setCursor(0,0);
      lcd.print(str1);
    }
    if (lcdLines >= 2)
    {
      lcd.setCursor(0,1);
      lcd.print(str2);
    }
    if (lcdLines >= 3)
    {
      lcd.setCursor(0,2);
      lcd.print(str3);
    }
    if (lcdLines >= 4)
    {
      lcd.setCursor(0,3);
      lcd.print(str4);
    }
  }
}

void serialEvent()
{
  byte bufferBoi[Serial.available()+1];
  int bufferSize = 0;
  bufferSize = Serial.readBytes(bufferBoi, Serial.available());
  bufferBoi[bufferSize]='\n';
  int bufferIndex = 0;
  parsingStates state = initialState;
  int reader;
  //int colum = 0;
  int line = 0;

  char str1[lcdColums+1];
  char str2[lcdColums+1];
  char str3[lcdColums+1];
  char str4[lcdColums+1];

  str1[lcdColums]='\0';
  str2[lcdColums]='\0';
  str3[lcdColums]='\0';
  str4[lcdColums]='\0';

  fillArray(str1, 0, lcdColums);
  fillArray(str2, 0, lcdColums);
  fillArray(str3, 0, lcdColums);
  fillArray(str4, 0, lcdColums);

  char barString[lcdColums];
  static char previousBarString[16];
  bool barActive = false;

  int index = 0;



  int tempInt1 = 0;
  int tempInt2 = 0;
  int tempInt3 = 0;
  while (state != endState)
  {
    reader = bufferBoi[bufferIndex++];
    if (reader == '\n' || reader == -1)
    //if(reader = '\n' || bufferIndex >= bufferSize)
    {
      state = endState;
    }
    switch (state)
    {
      case initialState:
        if (reader == '*')
          state = ledAdjust;
        if (reader == '@')
          state = buzzer;
        if (reader == '!')
          state = pulse;
        if (reader == '%')
          state = bar;
        if (reader == '$')
          state = string1start;
        break;

      case ledAdjust:
        tempInt1 = reader;
        state = ledAdjust2;
        break;

      case ledAdjust2:
        tempInt2 = reader;
        state = ledAdjust3;
        break;

      case ledAdjust3:
        tempInt3 = reader;
        setRGB(tempInt1, tempInt2, tempInt3);
        state = initialState;
        break;

      case buzzer:
        tempInt1 = reader;
        buzz(tempInt1);
        state = initialState;
        break;

      case pulse:
        tempInt1 = reader;
        redLedPulse(tempInt1, 0);
        state = initialState;
        break;

      case bar:
        tempInt1 = reader;
        state = bar1;
        break;

      case bar1:
        tempInt2 = reader;
        percentageBar(tempInt1, tempInt2, barString);
        barActive = true;
        state = initialState;

      case string1start:
        if(reader=='~')
        {
          state = string2start;
          break;
        }
        index = 0;
        str1[index++] = reader;
        state = string1;
        break;

      case string1:
        if(reader=='~')
        {
          state = string2start;
          break;
        }
        str1[index++] = reader;
        break;
        
      case string2start:
        if(reader=='~')
        {
          state = string3start;
          break;
        }
        index = 0;
        str2[index++] = reader;
        state = string2;
        break;

      case string2:
        if(reader=='~')
        {
          state = string3start;
          break;
        }
        str2[index++] = reader;
        break;
        
      case string3start:
        if(reader=='~')
        {
          state = string4start;
          break;
        }
        index = 0;
        str3[index++] = reader;
        state = string3;
        break;

      case string3:
        if(reader=='~')
        {
          state = string4start;
          break;
        }
        str3[index++] = reader;
        break;
        
      case string4start:
        if(reader=='~')
        {
          state = endState;
          break;
        }
        index = 0;
        str4[index++] = reader;
        state = string4;
        break;

      case string4:
        if(reader=='~')
        {
          state = endState;
          break;
        }
        str4[index++] = reader;
        break;
    }
  }
  if (barActive)
  {
    copyArray(barString, str1, lcdColums);
  }
  updateLCD(str1, str2, str3, str4);
  Serial.write('!');
}

void sendButton(int b)
{
  static int teste = 0;
  if (b < 100) {
    Serial.write(1);
    delay(200);
    //Direita
  }
  else if (b < 200) {
    Serial.write(2);
    delay(200);
    //Cima
  }
  else if (b < 400) {
    Serial.write(3);
    delay(200);
    //Baixo
  }
  else if (b < 600) {
    Serial.write(4);
    //updateLCD("1234567890123456","                ","                ","                ");
    delay(200);
    //Esquerda
  }
  else if (b < 800) {
    //Select
    Serial.write(5);
    delay(200);
  }
  else
  {
    //Serial.write(0);
    //delay(200);
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  unsigned long deltaTime = currentMillis - previousMillis;
  previousMillis = currentMillis;

  int botao = analogRead(0);
  sendButton(botao);
  redLedPulse(0, deltaTime);
  analogWrite(RED, vRED);
  delay(50);
}
