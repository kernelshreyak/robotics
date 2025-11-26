#include <webots/robot.h>
#include <webots/motor.h>
#include <stdio.h>

#define TIME_STEP 64

int main(int argc, char **argv) {
  wb_robot_init();

  // Get motor handles
  WbDeviceTag R_motor = wb_robot_get_device("Right_motor");
  WbDeviceTag L_motor = wb_robot_get_device("Left_motor");

  // Set infinite position (velocity control mode)
  wb_motor_set_position(R_motor, INFINITY);
  wb_motor_set_position(L_motor, INFINITY);

  // Read each motor’s maximum speed (from model)
  double R_max = wb_motor_get_max_velocity(R_motor);
  double L_max = wb_motor_get_max_velocity(L_motor);

  printf("Right motor max speed: %.2f\n", R_max);
  printf("Left motor max speed: %.2f\n", L_max);

  // Use near-maximum velocity for fast shooting
  double shoot_speed = 0.8 * R_max; // 90% of max for safety

  while (wb_robot_step(TIME_STEP) != -1) {
    // Spin in opposite directions
    wb_motor_set_velocity(R_motor, shoot_speed);
    wb_motor_set_velocity(L_motor, -shoot_speed);
  }

  wb_robot_cleanup();
  return 0;
}
