#include <webots/robot.h>
#include <webots/supervisor.h>
#include <stdio.h>
#include <string.h> // Required for sprintf

#define TIME_STEP 32
#define BELT_SPEED 0.5   // Target speed in m/s
#define GAIN 2       

// Adjust these to match the ACTUAL size of your grey belt in the world
// If these are wrong, the force cuts off early, causing the package to stop.
#define BELT_MIN_X -1.0
#define BELT_MAX_X  1.0 
#define BELT_MIN_Z -0.25
#define BELT_MAX_Z  0.25

#define MAX_PACKAGES 10  // How many possible packages to look for (PACKAGE1 to PACKAGE10)

int main(int argc, char **argv) {
  wb_robot_init();

  // Array to store references to all found packages
  WbNodeRef packages[MAX_PACKAGES];
  int found_count = 0;

  // 1. Initialization Loop: Find PACKAGE1, PACKAGE2, etc.
  for (int i = 1; i <= MAX_PACKAGES; i++) {
    char def_name[32];
    sprintf(def_name, "PACKAGE%d", i); // Generates string "PACKAGE1", "PACKAGE2"...

    WbNodeRef node = wb_supervisor_node_get_from_def(def_name);
    
    if (node != NULL) {
      packages[found_count] = node;
      found_count++;
      printf("Conveyor Controller: Connected to %s\n", def_name);
    }
  }

  if (found_count == 0) {
    printf("Warning: No nodes found with DEF name 'PACKAGE1', 'PACKAGE2', etc.\n");
  }

  // Main Simulation Loop
  while (wb_robot_step(TIME_STEP) != -1) {
    
    // Loop through all the packages we found earlier
    for (int i = 0; i < found_count; i++) {
      WbNodeRef current_package = packages[i];

      // 2. Get current position and velocity
      const double *pos = wb_supervisor_node_get_position(current_package);
      const double *vel = wb_supervisor_node_get_velocity(current_package);
      
      // Safety check in case a package was deleted during simulation
      if (pos == NULL || vel == NULL) continue;

      // 3. Check bounds: Is THIS package currently on the belt?
      if (pos[0] > BELT_MIN_X && pos[0] < BELT_MAX_X &&
          pos[2] > BELT_MIN_Z && pos[2] < BELT_MAX_Z) {
        
        // 4. Calculate Force
        double diff = BELT_SPEED - vel[0];
        
        // Apply force in X direction
        // Higher GAIN ensures the box doesn't get stuck due to friction
        double force[3] = { diff * GAIN, 0, 0 };
        
        wb_supervisor_node_add_force(current_package, force, false);
      }
    }
  }

  wb_robot_cleanup();
  return 0;
}