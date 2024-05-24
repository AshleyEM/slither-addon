bl_info = {
    "name": "Slither",
    "author": "www.github.com/AshleyEM",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Side Bar > Slither Addon",
    "category": "Animation",
}

import bpy
from .slither import animate_slither

# Execute: Apply
class ApplyOperator(bpy.types.Operator):
    """The Apply button that executes slither()"""
    bl_idname = "pose.apply"
    bl_label = "Generate Slither Animation"
    
    # Execute slither(), pass Properties as args
    def execute(self, context):
        animate_slither(
            bpy.context.scene.tail,
            bpy.context.scene.amplitude,
            bpy.context.scene.flexibility,
            bpy.context.scene.axis,
            bpy.context.scene.duration,
            1/bpy.context.scene.speed # inverse relationship (larger->faster)
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

       
# bpy.types.Scene.<property> = store value of <property> in scene    
def register():
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
