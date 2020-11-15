class Camera:
    name = "Default name"
    #instance attributes
    def __init__(self, resolution, focus):
        self.resolution = resolution
        self.focus = focus

    #instance method
    def get_camera_resolution(self):
        return "Camera resolution {}".format(self.focus)

object = Camera(1024, 8)

# Class attributes and methods
print(Camera.__dict__)
print("Object class is a {}".format(object.__class__.name))
# Instance attributes and methods
print(object.__dict__)