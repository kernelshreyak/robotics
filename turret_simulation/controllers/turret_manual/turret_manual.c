#include <webots/robot.h>
#include <webots/motor.h>
#include <webots/keyboard.h>
#include <webots/position_sensor.h>
#include <stdio.h>

int main() {
  wb_robot_init();

  int time_step = wb_robot_get_basic_time_step();
  if (time_step <= 0)
    time_step = 32; // fallback

  // ---- Devices ----
  WbDeviceTag yaw_motor = wb_robot_get_device("yaw_motor");
  WbDeviceTag yaw_sensor = wb_robot_get_device("yaw_sensor");

  WbDeviceTag pitch_motor = wb_robot_get_device("pitch_motor");
  WbDeviceTag pitch_sensor = wb_robot_get_device("pitch_sensor");

  // ---- Enable sensors ----
  wb_position_sensor_enable(yaw_sensor, time_step);
  wb_position_sensor_enable(pitch_sensor, time_step);

  // ---- Enable keyboard ----
  wb_keyboard_enable(time_step);

  // ---- Configure motors for velocity control ----
  wb_motor_set_position(yaw_motor, INFINITY);
  wb_motor_set_position(pitch_motor, INFINITY);

  // Optionally give them torque capability
  wb_motor_set_force(yaw_motor, 10.0);
  wb_motor_set_force(pitch_motor, 10.0);

  double yaw_speed = 0.0;
  double pitch_speed = 0.0;
  const double speed_step = 1.0;  // radians/sec

  printf("Turret manual control started.\n");
  printf("A/D = Yaw left/right | W/S = Pitch up/down\n");

  // ---- Main control loop ----
  while (wb_robot_step(time_step) != -1) {
    int key = wb_keyboard_get_key();

    // Reset speeds
    yaw_speed = 0.0;
    pitch_speed = 0.0;

    // Handle yaw (A/D)
    if (key == 'A') {
      yaw_speed = speed_step;
    } else if (key == 'D') {
      yaw_speed = -speed_step;
    }

    // Handle pitch (W/S)
    if (key == 'W') {
      pitch_speed = speed_step;
    } else if (key == 'S') {
      pitch_speed = -speed_step;
    }

    // Apply velocities
    wb_motor_set_velocity(yaw_motor, yaw_speed);
    wb_motor_set_velocity(pitch_motor, pitch_speed);

    // Optional debug info
    double yaw_angle = wb_position_sensor_get_value(yaw_sensor);
    double pitch_angle = wb_position_sensor_get_value(pitch_sensor);
    printf("\rYaw: %.2f rad | Pitch: %.2f rad  ", yaw_angle, pitch_angle);
    fflush(stdout);
  }

  wb_robot_cleanup();
  return 0;
}
