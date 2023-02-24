=================================
Blender-Addon-Utils Documentation
=================================

Welcome to the blender_addon_utils documenation.

This is a utility module for blender addons to help automatically installing addon
dependencies and checking for updates.

Installation
~~~~~~~~~~~~

Add the `blender_addon_utils <https://github.com/30350n/blender_addon_utils>`_ respository to
your addon as a submodule:

.. code-block:: bash

    $ git submodule add https://github.com/30350n/blender_addon_utils my_addon/blender_addon_utils/

How it works
~~~~~~~~~~~~

You can declare required dependencies for your addon via :func:`add_dependencies`.

| When you generate your registration code via :func:`register_modules_factory`, the function
  will automatically check if all previously declared dependencies are available.
| If not, the resulting registration functions, won't register your modules, but the end-user
  will instead be presented with a panel like this, in the addon preferences:

    .. image:: ./images/addon_prefs.png
        :align: center

| The panel first offers the option to install pip and then the required dependencies.
| After dependency installation is complete, your addon will be automatically reloaded.

Usage
~~~~~

To use the :func:`add_dependencies` and :func:`register_modules_factory` functionality,
all your addon code will have to be arranged into submodules, which each submodule having its
own :func:`register` and :func:`unregister` functions.

Your :code:`__init__.py` should only contain minimal setup code, like this:

.. code-block:: python

    bl_info = {
        ...
    }

    from .blender_addon_utils import add_dependencies, register_modules_factory

    deps = {
        "pip_package_name": "module_name",
    }
    add_dependencies(deps)

    modules = ["my_submodule"]
    register, unregister = register_modules_factory(modules) 

Example :code:`my_submodule.py` file:

.. code-block:: python

    import bpy

    ...

    classes = (
        ...
    )

    def register():
        for cls in classes:
            bpy.utils.register_class(cls)

    def unregister():
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)

API Documenation
~~~~~~~~~~~~~~~~

.. automodule:: register
    :members:
    :member-order: bysource

.. automodule:: error_helper
    :members:
