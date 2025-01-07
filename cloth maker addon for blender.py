# -*- coding: utf-8 -*-
bl_info = {
    "name": "Cloth Maker",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > Cloth Maker",
    "description": "Create and convert cloth objects",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy

class ClothMakerPanel(bpy.types.Panel):
    bl_label = "Cloth Maker"
    bl_idname = "VIEW3D_PT_cloth_maker"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ClothMaker'
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "plane_size")
        layout.prop(context.scene, "subdivisions")
        layout.operator("object.create_cloth_plane", text="Create Cloth Plane")
        layout.operator("object.convert_to_cloth", text="Convert to Cloth")

class ClothMakerTool(bpy.types.Operator):
    bl_idname = "wm.cloth_maker_tool"
    bl_label = "Cloth Maker"
    bl_description = "Open the Cloth Maker panel"
    
    def execute(self, context):
        return {'FINISHED'}

class CreateClothPlaneOperator(bpy.types.Operator):
    bl_idname = "object.create_cloth_plane"
    bl_label = "Create Cloth Plane"
    
    def execute(self, context):
        plane_size = context.scene.plane_size
        subdivisions = context.scene.subdivisions
        
        # Create a new plane at the center position (0, 0, 0)
        bpy.ops.mesh.primitive_plane_add(size=plane_size, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        obj = bpy.context.active_object
        
        if obj is not None:
            # Subdivide the plane
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=subdivisions)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Apply Cloth Modifier to the plane
            bpy.ops.object.modifier_add(type='CLOTH')
            cloth_modifier = obj.modifiers[-1]
            cloth_modifier.settings.quality = 5
            cloth_modifier.settings.mass = 0.3
                    
            self.report({'INFO'}, "Cloth plane created at center")
        else:
            self.report({'WARNING'}, "Failed to create plane")
        
        return {'FINISHED'}

class ConvertToClothOperator(bpy.types.Operator):
    bl_idname = "object.convert_to_cloth"
    bl_label = "Convert to Cloth"
    
    def execute(self, context):
        obj = context.object
        subdivisions = context.scene.subdivisions
        
        if obj is not None and obj.type == 'MESH':
            # Subdivide the plane
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=subdivisions)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Apply Cloth Modifier to the selected object
            bpy.ops.object.modifier_add(type='CLOTH')
            cloth_modifier = obj.modifiers[-1]
            cloth_modifier.settings.quality = 5
            cloth_modifier.settings.mass = 0.3
                    
            self.report({'INFO'}, "Selected plane converted to cloth")
        else:
            self.report({'WARNING'}, "No valid object selected")
        
        return {'FINISHED'}

def draw_cloth_maker_button(self, context):
    layout = self.layout
    layout.operator("wm.cloth_maker_tool", text="Cloth Maker", icon='MOD_CLOTH')

def register():
    bpy.types.Scene.plane_size = bpy.props.FloatProperty(
        name="Plane Size",
        description="Size of the plane",
        default=2.0,
        min=0.1,
        max=1000.0
    )
    bpy.types.Scene.subdivisions = bpy.props.IntProperty(
        name="Subdivisions",
        description="Number of subdivisions for the plane",
        default=2,
        min=1,
        max=1000000  # Setting a very high max value to act as infinite
    )
    bpy.utils.register_class(ClothMakerPanel)
    bpy.utils.register_class(ClothMakerTool)
    bpy.utils.register_class(CreateClothPlaneOperator)
    bpy.utils.register_class(ConvertToClothOperator)
    bpy.types.VIEW3D_HT_tool_header.append(draw_cloth_maker_button)

def unregister():
    bpy.utils.unregister_class(ClothMakerPanel)
    bpy.utils.unregister_class(ClothMakerTool)
    bpy.utils.unregister_class(CreateClothPlaneOperator)
    bpy.utils.unregister_class(ConvertToClothOperator)
    bpy.types.VIEW3D_HT_tool_header.remove(draw_cloth_maker_button)
    del bpy.types.Scene.plane_size
    del bpy.types.Scene.subdivisions

if __name__ == "__main__":
    register()
