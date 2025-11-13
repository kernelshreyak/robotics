---Robotnik Summit XL Movement Script
-- Unstabnet Research (C) 2019


---------------------Movement Functions--------------------------------------
function move_forward(vel)
    sim.setJointTargetVelocity(br,-vel)
    sim.setJointTargetVelocity(bl,vel)
    sim.setJointTargetVelocity(fr,-vel)
    sim.setJointTargetVelocity(fl,vel)
end

function move_backward(vel)
    sim.setJointTargetVelocity(br,vel)
    sim.setJointTargetVelocity(bl,-vel)
    sim.setJointTargetVelocity(fr,vel)
    sim.setJointTargetVelocity(fl,-vel)
end


function move_left(vel)
    sim.setJointTargetVelocity(br,vel)
    sim.setJointTargetVelocity(bl,-vel)
    sim.setJointTargetVelocity(fr,vel)
    sim.setJointTargetVelocity(fl,-vel)
end

function move_backward(vel)
    sim.setJointTargetVelocity(br,vel)
    sim.setJointTargetVelocity(bl,-vel)
    sim.setJointTargetVelocity(fr,vel)
    sim.setJointTargetVelocity(fl,-vel)
end

----------------------------------------------------------------------

function sysCall_init()
    -- do some initialization here:

    -- Make sure you read the section on "Accessing general-type objects programmatically"
    -- For instance, if you wish to retrieve the handle of a scene object, use following instruction:
    --
    -- handle=sim.getObjectHandle('sceneObjectName')
    -- 
    -- Above instruction retrieves the handle of 'sceneObjectName' if this script's name has no '#' in it
    --
    -- If this script's name contains a '#' (e.g. 'someName#4'), then above instruction retrieves the handle of object 'sceneObjectName#4'
    -- This mechanism of handle retrieval is very convenient, since you don't need to adjust any code when a model is duplicated!
    -- So if the script's name (or rather the name of the object associated with this script) is:
    --
    -- 'someName', then the handle of 'sceneObjectName' is retrieved
    -- 'someName#0', then the handle of 'sceneObjectName#0' is retrieved
    -- 'someName#1', then the handle of 'sceneObjectName#1' is retrieved
    -- ...
    --
    -- If you always want to retrieve the same object's handle, no matter what, specify its full name, including a '#':
    --
    -- handle=sim.getObjectHandle('sceneObjectName#') always retrieves the handle of object 'sceneObjectName' 
    -- handle=sim.getObjectHandle('sceneObjectName#0') always retrieves the handle of object 'sceneObjectName#0' 
    -- handle=sim.getObjectHandle('sceneObjectName#1') always retrieves the handle of object 'sceneObjectName#1'
    -- ...
    --
    -- Refer also to sim.getCollisionhandle, sim.getDistanceHandle, sim.getIkGroupHandle, etc.
end

function sysCall_actuation()
    -- put your actuation code here
    --
    -- For example:
    --
    -- local position=sim.getObjectPosition(handle,-1)
    -- position[1]=position[1]+0.001
    -- sim.setObjectPosition(handle,-1,position)
    
    
    bl=sim.getObjectHandle('joint_back_left_wheel')
    br=sim.getObjectHandle('joint_back_right_wheel')
    fl=sim.getObjectHandle('joint_front_left_wheel')
    fr=sim.getObjectHandle('joint_front_right_wheel')
    
    simTime=simGetSimulationTime()  
    
    -- movement logics
    T1=26
    T2=30
    if (simTime <= T1) then
       move_forward(1)
    elseif (simTime > T1) and (simTime <= T2) then 
         move_backward(1)
    end    
end

function sysCall_sensing()
    -- put your sensing code here
end

function sysCall_cleanup()
    -- do some clean-up here
end

-- You can define additional system calls here:
--[[
function sysCall_suspend()
end

function sysCall_resume()
end

function sysCall_dynCallback(inData)
end

function sysCall_jointCallback(inData)
    return outData
end
--]]
