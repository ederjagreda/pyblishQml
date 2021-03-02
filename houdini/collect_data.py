import os
import re
import pyblish.api
import hou


ruta = r"Z:/"           # for Mompozt
if not os.path.exists(ruta):
    ruta = r"/Volumes/Projects/"

class CollectData(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder + 0.1
    label = "Collect scene information"
    hosts = ['houdini']

    def process(self, context):
        filename = hou.hipFile.name()
        dirname, fileBase = os.path.split(filename)
        if re.findall(r"(SH\d+)", fileBase):
            type = "shot"
            project, sq, sh, task, demas =  fileBase.split("_")
        else:
            type = "asset"
            project, asset, task, demas =  fileBase.split("_")

        try:
            instance = context.create_instance(name=fileBase)
            instance.data['pjDir'] = os.path.join(ruta, project)
            instance.data['family'] = 'scene'
            instance.data['type'] = type
            instance.data['file'] = filename
            instance.data['task'] = task
            instance.data['project'] = project
            if type == "asset":
                instance.data['asset'] = asset
            elif type == "shot":
                instance.data['shot'] = sh
                instance.data['sequence'] = sq

        except Exception as e:
            raise Exception(e)
        return
