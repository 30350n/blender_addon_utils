import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty

import subprocess, sys, requests
from subprocess import DEVNULL, CalledProcessError
from pathlib import Path
from tempfile import gettempdir
from requests.status_codes import codes as STATUS_CODE
from requests.exceptions import RequestException

from .error_helper import ErrorHelper as _ErrorHelper

GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
PIP_CMD = [sys.executable, "-m", "pip"]

def get_dependency_addon_prefs(package, deps, path, no_extra_deps):
    has_pip = subprocess.run(PIP_CMD, stdout=DEVNULL, stderr=DEVNULL).returncode == 0

    class InstallPip(Operator, _ErrorHelper):
        """Install pip"""
        bl_idname = f"{package}.install_pip"
        bl_label = f"Install pip from '{GET_PIP_URL}'"

        def execute(self, context):
            try:
                request = requests.get(GET_PIP_URL)
                if request.status_code != STATUS_CODE.OK:
                    return self.error(
                        f"received invalid status code '{request.status_code}' "
                        f"from '{GET_PIP_URL}'")

                get_pip_content = request.content

            except RequestException as e:
                return self.error(f"failed to download '{GET_PIP_URL}' with '{e}'")

            get_pip_path = Path(gettempdir()) / "get-pip.py"
            with open(get_pip_path, "wb") as file:
                file.write(get_pip_content)

            cmd = (sys.executable, get_pip_path)
            try:
                subprocess.check_call(cmd, stdout=DEVNULL, stderr=DEVNULL)
            except CalledProcessError as e:
                return self.error(f"failed to install pip with '{e}'")

            context.preferences.addons[package].preferences.install_pip = False

            return {"FINISHED"}

    class InstallDependencies(Operator, _ErrorHelper):
        """Install Dependencies"""
        bl_idname = f"{package}.install_deps"
        bl_label = f"Install {', '.join(deps)}"

        def execute(self, context):
            cmd = PIP_CMD + ["install", *deps, "-t", str(path), "--ignore-installed"]
            if no_extra_deps:
                cmd.append("--no-deps")

            try:
                subprocess.check_call(cmd, stdout=DEVNULL, stderr=DEVNULL)
            except CalledProcessError as e:
                return self.error(f"failed to install dependencies with '{e}'")

            bpy.ops.script.reload()

            return {"FINISHED"}

    class DependencyAddonPreferences(AddonPreferences):
        bl_idname = package

        install_pip: BoolProperty(options={"HIDDEN"}, default=not has_pip)

        def draw(self, context):
            layout = self.layout

            layout.label(text="Complete steps to finish addon installation:", icon="ERROR")

            row = layout.row()
            row.operator(InstallPip.bl_idname)
            row.scale_y = 2
            row.enabled = self.install_pip

            row = layout.row()
            row.operator(InstallDependencies.bl_idname)
            row.scale_y = 2
            row.enabled = not self.install_pip

    def register():
        bpy.utils.register_class(InstallPip)
        bpy.utils.register_class(InstallDependencies)
        bpy.utils.register_class(DependencyAddonPreferences)

    def unregister():
        bpy.utils.unregister_class(DependencyAddonPreferences)
        bpy.utils.unregister_class(InstallDependencies)
        bpy.utils.unregister_class(InstallPip)

    return register, unregister
