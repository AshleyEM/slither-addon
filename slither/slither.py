import bpy
import math
import mathutils

def slither(tail, amp, flex, axis, duration, speed):

    # Selected bones (armature)
    arm = bpy.context.selected_pose_bones

    if arm == None:
        print("Slither Addon: No bones selected")
        return
    if len(arm) == 0:
        print("Slither Addon: No bones selected")
        return

    # Will hold be the rotation angles for each bone (x,y,z)
    rot = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
    
    # num of bones scales how each bone is staggered
    total_bones = len(arm)
    const_angle = 1 /total_bones 
     
    frame = bpy.context.scene.frame_current # current frame
    angle = 0 # angle being increased each frame

    for _ in range(duration):

        bn = 1
        
        # For each selected bone
        for b in arm:
 
            # Increase angle
            angle += const_angle  

            # Calculate rotation along X or Y or Z axis
            # Stagger (phase shift L/R) based on bone number (bn)
            if axis == 'X':
                if tail:
                    rot[0] = amp * bn * math.sin(angle - (bn * flex))
                else:
                    rot[0] = amp * bn * math.sin(angle + (bn * flex))
            if axis == 'Y':
                if tail:
                    rot[1] = amp * bn * math.sin(angle - (bn * flex))
                else:
                    rot[1] = amp * bn * math.sin(angle + (bn * flex))
            if axis == 'Z':
                if tail:
                    rot[2] = amp * bn * math.sin(angle - (bn * flex))
                else:
                    rot[2] = amp * bn * math.sin(angle + (bn * flex))
               
            # Rotate bone 
            b.rotation_mode = 'XYZ'
            b.rotation_euler = rot 
            
            # Insert keyframe
            b.keyframe_insert('rotation_euler', frame=frame)
            
            # Jump to next keyframe
            frame += speed * 2
            bn += 1
     
