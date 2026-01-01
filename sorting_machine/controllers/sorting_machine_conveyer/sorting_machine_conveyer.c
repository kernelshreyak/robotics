#include <webots/robot.h>
#include <webots/motor.h>
#include <stdio.h>

#define TIME_STEP 32
#define NUM_MOTORS 25 // Change this to match your total motor count

int main() {
  wb_robot_init();

  // 1. Initialize an array of device tags
  WbDeviceTag roller_motors[NUM_MOTORS];
  char motor_name[20];

  for (int i = 0; i < NUM_MOTORS; i++) {
    // Construct the name dynamically (roller_motor1, roller_motor2, ...)
    sprintf(motor_name, "roller_motor%d", i + 1);
    
    // Get the device tag from Webots
    roller_motors[i] = wb_robot_get_device(motor_name);

    if (roller_motors[i]) {
      // 2. Set to Velocity Mode by setting position to INFINITY
      wb_motor_set_position(roller_motors[i], INFINITY);
      
      // 3. Set initial velocity to 0.0
      wb_motor_set_velocity(roller_motors[i], 0.0);
    } else {
      printf("Error: Could not find motor named %s\n", motor_name);
    }
  }

  // Simulation loop
  while (wb_robot_step(TIME_STEP) != -1) {
    // 4. Update motor velocities (example: rotate all at 2.0 rad/s)
    for (int i = 0; i < NUM_MOTORS; i++) {
      if (roller_motors[i]) {
        wb_motor_set_velocity(roller_motors[i], 2.0);
      }
    }
  }

  wb_robot_cleanup();
  return 0;
}