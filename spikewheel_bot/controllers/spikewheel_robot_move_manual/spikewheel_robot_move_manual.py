from controller import Robot, Keyboard

robot = Robot()
timestep = int(robot.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

left_motor = robot.getDevice("left_motor")
right_motor = robot.getDevice("right_motor")

# Velocity control mode
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

SPEED = 50.0

left_motor.setVelocity(0)
# left_motor.setTorque(10)
right_motor.setVelocity(0)
# right_motor.setTorque(10)
while robot.step(timestep) != -1:
    key = keyboard.getKey()

    if key == Keyboard.UP:
        left_motor.setVelocity(SPEED)
        right_motor.setVelocity(SPEED)

    elif key == Keyboard.DOWN:
        left_motor.setVelocity(-SPEED)
        right_motor.setVelocity(-SPEED)

    else:
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
