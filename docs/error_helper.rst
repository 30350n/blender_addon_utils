============
error_helper
============

.. autoclass:: error_helper.ErrorHelper
    :members:

Example:

.. code-block:: python

    class MY_ADDON_OT_my_operator(bpy.types.Operator, ErrorHelper):
        bl_idname = "my_addon.my_operator"
        bl_label = "My Operator"

        def execute(self, context):
            if context.mode == "EDIT_MESH":
                self.warning("we are in edit mode")
            elif context.mode == "POSE":
                return self.error("operator doesn't work in pose mode")
            return {"FINISHED"}
