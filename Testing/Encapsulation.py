class Camera:
    name = "Default name"

    def method(self):
        return 'instance method called', self
    #instance attributes
    def __init__(self, resolution, focus):
        self.resolution = resolution
        self.focus = focus
        self.width = 2

    def set_new_name(self, name):
        self.__class__.name = name

    #instance method
    def get_camera_resolution(self):
        return "Camera resolution {}".format(self.focus)

    def ins_width(self):
        return self.calculate_matrix_width(self.width)

    @staticmethod
    def calculate_matrix_width(size):
        return 0.0023 * size

    @classmethod
    def thermoframe_camera(cls):
        return cls(4024, 200)

    @classmethod
    def change_name(cls, res):
        cls.name = res

    @classmethod
    def class_method(cls):
        return 'class method called', cls

    @staticmethod
    def static_method():
        return 'static method called'

# STATIC METHOD EXAMPLE
cam_st = Camera(423, 234)
print(cam_st.ins_width())
print(Camera.calculate_matrix_width(123))

# INSTANCE VS CLASS METHOD
cam = Camera.thermoframe_camera()
print(cam.get_camera_resolution())

object1 = Camera(1024, 8)
object2 = Camera(2048, 13)
object3 = Camera(640, 18)

object1.set_new_name("NEW Default")

print(object1.method())
print(object2.method())
print(object3.method())

print(Camera.class_method())
print(object1.class_method())

print(object1.static_method())

# print(Camera.__dict__) # Class attributes and methods

print("Object1 class is a {}".format(object1.__class__.name))
print("Object2 class is a {}".format(object2.__class__.name))
print("Object3 class is a {}".format(object3.__class__.name))

# Instance attributes and methods
print(object1.__dict__)
print(object2.__dict__)
print(object3.__dict__)

Camera.change_name("Joke") #class method call

print("Object1 class is a {}".format(object1.__class__.name))
print("Object2 class is a {}".format(object2.__class__.name))
print("Object3 class is a {}".format(object3.__class__.name))