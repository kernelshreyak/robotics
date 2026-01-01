#include <webots/robot.h>
#include <webots/supervisor.h>
#include <stdio.h>
#include <stdlib.h> 
#include <time.h>   
#include <string.h> 

#define TIME_STEP 32 
#define SPAWN_INTERVAL_SECONDS 2.0
#define MAX_STRING_LENGTH 256
#define BOX_HEIGHT 0.06
#define HALF_BOX_HEIGHT (BOX_HEIGHT / 2.0)

// Define the fixed spawn location coordinates
#define FIXED_SPAWN_X 1.0
#define FIXED_SPAWN_Z 0.0
// Y is fixed based on half the box height to sit on the ground (assuming ground Y is 0.0)
#define FIXED_SPAWN_Y HALF_BOX_HEIGHT


int main(int argc, char **argv) {
    wb_robot_init();
    srand(time(NULL));

    WbNodeRef root_node = wb_supervisor_node_get_root();
    WbFieldRef children_field = wb_supervisor_node_get_field(root_node, "children");

    if (root_node == NULL || children_field == NULL) {
        fprintf(stderr, "Error accessing scene tree.\n");
        wb_robot_cleanup();
        return 1;
    }

    double time_elapsed = 0.0;
    double next_spawn_time = 0.0;
    int box_count = 0;

    printf("Supervisor starting. Spawning boxes at fixed location (%.1f, %.3f, %.1f) every %.1f seconds.\n", 
           FIXED_SPAWN_X, FIXED_SPAWN_Y, FIXED_SPAWN_Z, SPAWN_INTERVAL_SECONDS);

    while (wb_robot_step(TIME_STEP) != -1) {
        time_elapsed += (double)TIME_STEP / 1000.0;

        if (time_elapsed >= next_spawn_time) {
            
            // The coordinates are now hardcoded constants
            double x_pos = FIXED_SPAWN_X;
            double y_pos = FIXED_SPAWN_Y; 
            double z_pos = FIXED_SPAWN_Z;

            // Create a unique DEF name for each box
            char box_def_name;
            sprintf(box_def_name, "FIXED_BOX_%d", box_count);

            // Create the full node string, using the fixed location and size constants
            char box_string[MAX_STRING_LENGTH];
            sprintf(box_string, "DEF %s CardboardBox { translation %f %f %f size %f %f %f }", 
                    box_def_name, x_pos, y_pos, z_pos, BOX_HEIGHT, BOX_HEIGHT, BOX_HEIGHT);

            // Import the node
            wb_supervisor_field_import_mf_node_from_string(children_field, -1, box_string);

            printf("Spawned %s at (%.2f, %.2f, %.2f) at time %.2fs\n", 
                   box_def_name, x_pos, y_pos, z_pos, time_elapsed);

            // Update counters for the next interval
            next_spawn_time += SPAWN_INTERVAL_SECONDS;
            box_count++;
        }
    }

    wb_robot_cleanup();
    return 0;
}
