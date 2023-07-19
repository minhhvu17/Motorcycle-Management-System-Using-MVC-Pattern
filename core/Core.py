import os
import importlib
from config import APP_PATH


"""
    Class responsible for opening controllers
"""
class Core:   
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    """
        Given a controller name, return an instance of it
    
        @param controller:string Controller to be opened
    """
    @staticmethod
    def openController(controller,root):
        response = None
        # Set controller name
        controller = controller[0].upper()+controller[1:]
        controllerName = controller+"Controller"
        print(controllerName)
        # Check if file exists
        if os.path.exists(APP_PATH+"/controller/"+controllerName+".py"):
            module = importlib.import_module("controller." + controllerName)
            class_ = getattr(module, controllerName)
            response = class_(root)
        else:
            print("Error")
        return response