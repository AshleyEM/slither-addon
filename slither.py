bl_info = {
    "name": "Slither",
    "author": "www.github.com/AshleyEM",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Side Bar > Slither Addon",
    "category": "Animation",
}

import bpy
import math
import mathutils

# ==================== SLITHER CODE ===========================
def slither(tail, amp, flex, axis, duration, speed):

    # Selected bones (armature)
    arm = bpy.context.selected_pose_bones

    if arm == None:
        print("Slither Addon: No bones selected")
        return
    if len(arm) == 0:
        print("Slither Addon: No bones selected")
        return

    #------THINGS THE USER MODIFIES----
    # tail = slither from head or tail [True, False]
    # amp = Amplitude [0.1, 3]
    # duration = How long the animation is
    # axis = axis = Axis to slither along ['X'. 'Y', 'Z']
    # flex = Flexibility factor [0.1 , 1]
    # speed = frame jump (smaller=faster)
    #------------------------------------ 

    # Will hold be the rotation angles for each bone (x,y,z)
    rot = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
    
    # const_angle added to angle
    # num of bones scales how each bone is staggered
    total_bones = len(arm)
    const_angle = 1 /total_bones 
     
    frame = bpy.context.scene.frame_current # current frame
    angle = 0 # angle being increased each frame

    for _ in range(duration):
        
        # Bone number
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
     

# ================== ADDON PANEL UI ====================

# Execute: Apply
class ApplyOperator(bpy.types.Operator):
    bl_idname = "pose.apply"
    bl_label = "Generate Slither Animation"
    
    # Actually execute slither() -- pass Properties as args
    def execute(self, context):
        slither(
            bpy.context.scene.tail,
            bpy.context.scene.amplitude, # need to scale these down
            bpy.context.scene.flexibility,
            bpy.context.scene.axis,
            bpy.context.scene.duration,
            1/bpy.context.scene.speed # inverse relationship (smaller=faster)
        )
        return {'FINISHED'}


# The UI Panel of the whole addon
class POSE_PT_SlitherPanel(bpy.types.Panel):
    """Slither animation"""
    
    # Where SlitherPanel is located in Blender
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # 3D View -> Tab -> Panel labels
    bl_label = "Slither"
    # 3D View -> Tab label
    bl_category = "Slither Addon"
    
    def draw(self, context):
        col = self.layout.column()
        row = self.layout.row()
        
        # Panel -> buttons 
        col.prop(context.scene, 'amplitude') 
        col.prop(context.scene, 'flexibility') 
        col.prop(context.scene, 'duration')  
        col.prop(context.scene, 'speed') 
        col.prop(context.scene, 'axis')  # Axis Drop-down Menu (returns selected option)
        row.prop(context.scene, 'tail') 
        row.operator("pose.apply", text="Apply")
        
def register():
    
    # ALL PROPERTIES ARE HERE (amplitude, head/tail, axis, etc.)
    # bpy.types.Scene.amplitude = store value of 'amplitude' in the scene
    bpy.types.Scene.tail = bpy.props.BoolProperty(name="Tail", default=True)   # name=UI label text
    bpy.types.Scene.amplitude = bpy.props.FloatProperty(name="Amplitude", default=0.1, soft_max=1, soft_min=0.01)
    bpy.types.Scene.flexibility = bpy.props.FloatProperty(name="Flexibility", default=0.1, soft_max=1, soft_min=0.01)
    bpy.types.Scene.duration = bpy.props.IntProperty(name="Duration", default=10, soft_max=1000, soft_min=5)
    bpy.types.Scene.speed = bpy.props.IntProperty(name="Speed", default=1, soft_max=30, soft_min=1)
    bpy.types.Scene.axis = bpy.props.EnumProperty(
        name="Axis",
        items=( 
            ('X', 'X', 'Slither along the X-axis'),
            ('Y', 'Y', 'Slither along the Y-axis'),
            ('Z', 'Z', 'Slither along the Z-axis')
        )
    ) 

    bpy.utils.register_class(POSE_PT_SlitherPanel)
    bpy.utils.register_class(ApplyOperator)

def unregister():
    bpy.utils.unregister_class(POSE_PT_SlitherPanel)
    bpy.utils.unregister_class(ApplyOperator)

if __name__ == "__main__":
    register()
