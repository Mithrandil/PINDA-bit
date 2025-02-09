# Mesh Bed Leveling
#
# Copyright (C) 2018  Kevin O'Connor <kevin@koconnor.net>
# Copyright (C) 2018-2019 Eric Callahan <arksine.code@gmail.com>
# Copyright (C) 2023 Christian Lorandi
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging, collections
#from bed_mesh import *
from . import bed_mesh


class ProfileManagerTilt(bed_mesh.ProfileManager):
    def __init__(self, config, bedmesh):
        self.name = config.get_name()
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.bedmesh = bedmesh
        self.profiles = {}
        self.current_profile = ""
        self.incompatible_profiles = []
        # Fetch stored profiles from Config
        stored_profs = config.get_prefix_sections(self.name)
        stored_profs = [s for s in stored_profs
                        if s.get_name() != self.name]
        for profile in stored_profs:
            name = profile.get_name().split(' ', 1)[1]
            version = profile.getint('version', 0)
            if version != PROFILE_VERSION:
                logging.info(
                    "bed_mesh: Profile [%s] not compatible with this version\n"
                    "of bed_mesh.  Profile Version: %d Current Version: %d "
                    % (name, version, PROFILE_VERSION))
                self.incompatible_profiles.append(name)
                continue
            self.profiles[name] = {}
            zvals = profile.getlists('points', seps=(',', '\n'), parser=float)
            self.profiles[name]['points'] = zvals
            self.profiles[name]['mesh_params'] = params = \
                collections.OrderedDict()
            for key, t in PROFILE_OPTIONS.items():
                if t is int:
                    params[key] = profile.getint(key)
                elif t is float:
                    params[key] = profile.getfloat(key)
                elif t is str:
                    params[key] = profile.get(key)
        # Register GCode
        self.gcode.register_command(
            'BED_TILT_CORRECTION', self.cmd_BED_TILT_CORRECTION,
            desc=self.cmd_BED_TILT_CORRECTION_help)
            
    def compute_tilt(self, mesh, axis):
        """
        Compute the average tilt of the given mesh along the specified axis.

        Parameters:
        mesh (list of lists): the mesh to compute the tilt from.
        axis (int): 0 for X-axis, 1 for Y-axis.

        Returns:
        float: the average tilt along the specified axis.
        """
        first_line_z_sum = 0.0
        last_line_z_sum = 0.0
        
        points_on_the_axis = 0
        
        if axis == 0:        
            points_on_the_axis = len(mesh)
            for i in range(points_on_the_axis):
                first_line_z_sum += mesh[i][0]
                last_line_z_sum += mesh[i][-1]
        elif axis == 1:
            points_on_the_axis = len(mesh[0])
            for i in range(points_on_the_axis):
                first_line_z_sum += mesh[0][i]
                last_line_z_sum += mesh[-1][i]
        else:
            raise ValueError("Axis must be 0 or 1")

        return (last_line_z_sum - first_line_z_sum) / points_on_the_axis
            
    def edit_profile(self, prof_name):
        self.profiles = self.printer.lookup_object("bed_mesh").pmgr.get_profiles()
        
        # load the previously saved "prof_name" bed mesh profile from the config
        profile = self.profiles.get(prof_name, None)
        if profile is None:
            raise self.gcode.error(
                "bed_mesh_edit: Unknown profile [%s]" % prof_name)
                
        # move the the profile['points'] in a list to allow editing (tuples are read only)
        loaded_mesh = [list(line) for line in profile['points']]
        
        # load the data points from the current bed mash (usually probed points)
        probed_mesh = self.bedmesh.z_mesh.get_probed_matrix()
        
        probed_tilt_x = self.compute_tilt(probed_mesh, axis=0)
        loaded_tilt_x = self.compute_tilt(loaded_mesh, axis=0)
        z_correction_per_point_along_x = (probed_tilt_x - loaded_tilt_x) / (len(loaded_mesh[0]) - 1)

        probed_tilt_y = self.compute_tilt(probed_mesh, axis=1)
        loaded_tilt_y = self.compute_tilt(loaded_mesh, axis=1)
        z_correction_per_point_along_y = (probed_tilt_y - loaded_tilt_y) / (len(loaded_mesh) - 1)
        
        # apply z_correction to each point of the loaded_mesh
        for i in range(len(loaded_mesh)):
                for j in range(len(loaded_mesh[i])):
                        loaded_mesh[i][j] = loaded_mesh[i][j] + (z_correction_per_point_along_y * i) + (z_correction_per_point_along_x * j)

        
        # return the tilted mesh (loaded_mesh) to a tuple
        probed_matrix = tuple(tuple(line) for line in loaded_mesh)
        
        # some values should be recalculated with the new values
        mesh_params = profile['mesh_params']
        
        z_mesh = bed_mesh.ZMesh(mesh_params, prof_name)
        try:
            # create a z_mesh using the points of the tilted mesh
            z_mesh.build_mesh(probed_matrix)
        except BedMeshError as e:
            raise self.gcode.error(str(e))
        self.current_profile = prof_name
        self.bedmesh.set_mesh(z_mesh)
  
    cmd_BED_TILT_CORRECTION_help = "Saved Bed Mesh Tilt Correction using a freshly probed mesh"
    def cmd_BED_TILT_CORRECTION(self, gcmd):
        options = collections.OrderedDict({
            'SAVEDMESH': self.edit_profile,
        })
        for key in options:
            name = gcmd.get(key, None)
            if name is not None:
                if not name.strip():
                    raise gcmd.error(
                        "Value for parameter '%s' must be specified" % (key)
                    )
                else:
                    options[key](name)
                return
        gcmd.respond_info("Invalid syntax '%s'" % (gcmd.get_commandline(),))


def load_config(config):
    return ProfileManagerTilt(config, config.get_printer().lookup_object("bed_mesh"))
    
