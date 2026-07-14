// --- Motor Connections ---
#define ENCA 2 // Encoder A (Must be an interrupt pin on Arduino)
#define ENCB 3 // Encoder B
#define PWM 9  // L298N ENA (Must be a PWM pin)
#define IN1 8  // L298N IN1
#define IN2 7  // L298N IN2

// --- Globals ---
volatile long encoderCount = 0;
long previousTime = 0;
long previousCount = 0;
float eIntegral = 0;
float ePrevious = 0;

// --- PID Constants (TUNE THESE) ---
float kp = 2.0; 
float ki = 5.0; 
float kd = 1.0; 

// Target Speed (Counts per time interval)
float targetSpeed = 100.0; 

void setup() {
  Serial.begin(9600);
  
  pinMode(ENCA, INPUT_PULLUP);
  pinMode(ENCB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCA), readEncoder, RISING);
  
  pinMode(PWM, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void loop() {
  // 1. Set time interval for the loop (e.g., 50ms)
  long currentTime = millis();
  float deltaTime = ((float)(currentTime - previousTime)) / 1000.0; 
  
  if (deltaTime >= 0.05) { // Run PID at 20Hz
    
    // 2. Calculate current speed (counts per interval)
    long currentCount = encoderCount;
    float currentSpeed = (currentCount - previousCount) / deltaTime;
    
    previousCount = currentCount;
    previousTime = currentTime;

    // 3. Calculate Error
    float error = targetSpeed - currentSpeed;

    // 4. Calculate PID Terms
    float pTerm = kp * error;
    eIntegral = eIntegral + (error * deltaTime);
    float iTerm = ki * eIntegral;
    float dTerm = kd * ((error - ePrevious) / deltaTime);
    
    ePrevious = error;

    // 5. Compute Output and constrain to PWM limits (0-255)
    float controlSignal = pTerm + iTerm + dTerm;
    
    int pwr = (int)fabs(controlSignal);
    if (pwr > 255) pwr = 255;
    if (pwr < 0) pwr = 0;

    // 6. Set Motor Direction and Power
    int dir = 1;
    if (controlSignal < 0) {
      dir = -1;
    }
    setMotor(dir, pwr, PWM, IN1, IN2);

    // 7. Print to Serial Plotter (Format: Target, Actual)
    Serial.print(targetSpeed);
    Serial.print(" ");
    Serial.println(currentSpeed);
  }
}

// Function to drive the motor via L298N
void setMotor(int dir, int pwmVal, int pwmPin, int in1Pin, int in2Pin) {
  analogWrite(pwmPin, pwmVal);
  if (dir == 1) {
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
  } else if (dir == -1) {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
  } else {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, LOW);
  }
}

// Interrupt Service Routine to count encoder pulses
void readEncoder() {
  int b = digitalRead(ENCB);
  if (b > 0) {
    encoderCount++;
  } else {
    encoderCount--;
  }
}
