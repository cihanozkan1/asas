"""Blender (bpy) explosion with Mantaflow: renders a transparent PNG sequence (our own VFX, zero licence risk).

  ./bv/bin/python tools/vfx/explosion.py <out_dir> [--res 64] [--size 512] [--samples 24] [--frames 48] [--preset blast|muzzle|volcano]
"""
import bpy, sys, math, os, argparse
ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--res', type=int, default=64); ap.add_argument('--size', type=int, default=512)
ap.add_argument('--samples', type=int, default=24); ap.add_argument('--frames', type=int, default=48); ap.add_argument('--preset', default='blast')
a = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
os.makedirs(a.out, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = a.samples
sc.cycles.use_denoising = False
sc.render.film_transparent = True
sc.render.resolution_x = a.size; sc.render.resolution_y = a.size; sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.frame_start = 1; sc.frame_end = a.frames; sc.render.fps = 24
sc.view_settings.view_transform = 'Standard'

P = {'blast': dict(fuel=1.6, vel=2.4, flow_end=5, dens=6.0, rad=0.45, temp_k=1.0),
     'muzzle': dict(fuel=1.2, vel=4.0, flow_end=3, dens=3.0, rad=0.25, temp_k=1.0),
     'volcano': dict(fuel=0.9, vel=3.2, flow_end=40, dens=9.0, rad=0.5, temp_k=0.8)}[a.preset]

# --- domain
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.2))
dom = bpy.context.object; dom.name = 'Domain'; dom.scale = (2.6, 2.6, 4.4)
bpy.ops.object.modifier_add(type='FLUID')
dom.modifiers['Fluid'].fluid_type = 'DOMAIN'
ds = dom.modifiers['Fluid'].domain_settings
ds.domain_type = 'GAS'; ds.resolution_max = a.res
ds.use_noise = False
ds.cache_type = 'ALL'; ds.cache_directory = os.path.join(a.out, '_cache')
ds.use_adaptive_timesteps = True
ds.vorticity = 0.6
ds.beta = 1.5                       # buoyancy by temperature (heat)
ds.alpha = 0.6                      # buoyancy by density
ds.burning_rate = 0.9
ds.flame_smoke = 1.0
ds.flame_vorticity = 0.5
ds.use_dissolve_smoke = True; ds.dissolve_speed = 40
ds.use_collision_border_front = ds.use_collision_border_back = ds.use_collision_border_left = ds.use_collision_border_right = False
ds.use_collision_border_top = False; ds.use_collision_border_bottom = False

# --- flow source (a sphere at the bottom)
bpy.ops.mesh.primitive_ico_sphere_add(radius=P['rad'], location=(0, 0, 0.55), subdivisions=3)
fl = bpy.context.object; fl.name = 'Flow'
bpy.ops.object.modifier_add(type='FLUID')
fl.modifiers['Fluid'].fluid_type = 'FLOW'
fs = fl.modifiers['Fluid'].flow_settings
fs.flow_type = 'BOTH'; fs.flow_behavior = 'INFLOW'; fs.flow_source = 'MESH'
fs.fuel_amount = P['fuel']; fs.density = 1.0; fs.temperature = 2.0 * P['temp_k']
fs.use_initial_velocity = True; fs.velocity_normal = P['vel']; fs.surface_distance = 0.6
fs.use_inflow = True
fs.keyframe_insert('use_inflow', frame=1)
fs.use_inflow = False
fs.keyframe_insert('use_inflow', frame=P['flow_end'])
fl.hide_render = True

# --- volume material on the domain
mat = bpy.data.materials.new('Fire'); mat.use_nodes = True
nt = mat.node_tree; nt.nodes.clear()
out = nt.nodes.new('ShaderNodeOutputMaterial'); pv = nt.nodes.new('ShaderNodeVolumePrincipled')
ad = nt.nodes.new('ShaderNodeAttribute'); ad.attribute_name = 'density'
af = nt.nodes.new('ShaderNodeAttribute'); af.attribute_name = 'flame'
at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = 'temperature'
mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = P['dens']
nt.links.new(ad.outputs['Fac'], mul.inputs[0]); nt.links.new(mul.outputs[0], pv.inputs['Density'])
pv.inputs['Color'].default_value = (0.05, 0.045, 0.04, 1)
pv.inputs['Absorption Color'].default_value = (0.02, 0.018, 0.016, 1) if 'Absorption Color' in pv.inputs else None
pv.inputs['Blackbody Intensity'].default_value = 1.0
nt.links.new(af.outputs['Fac'], pv.inputs['Emission Strength']) if 'Emission Strength' in pv.inputs else None
pv.inputs['Emission Strength'].default_value = 6.0
nt.links.new(at.outputs['Fac'], pv.inputs['Temperature'])
nt.links.new(pv.outputs['Volume'], out.inputs['Volume'])
dom.data.materials.append(mat)

# --- light + camera
bpy.ops.object.light_add(type='SUN', location=(3, -4, 6)); bpy.context.object.data.energy = 3.0
bpy.context.object.rotation_euler = (math.radians(55), 0, math.radians(35))
bpy.ops.object.camera_add(location=(0, -9, 2.4), rotation=(math.radians(90), 0, 0)); cam = bpy.context.object
cam.data.lens = 50; sc.camera = cam

# --- bake + render
sc.frame_set(1)
bpy.ops.fluid.bake_data({'scene': sc, 'active_object': dom}) if False else None
with bpy.context.temp_override(scene=sc, active_object=dom, object=dom):
    bpy.ops.fluid.bake_data()
for f in range(1, a.frames + 1):
    sc.frame_set(f)
    sc.render.filepath = os.path.join(a.out, f'f{f:03d}.png')
    bpy.ops.render.render(write_still=True)
print('DONE', a.out)
