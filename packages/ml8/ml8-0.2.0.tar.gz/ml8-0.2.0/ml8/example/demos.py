

def demo(name = "iris"):
    print ("Demo: " + name)

    if name == "face":
        from . import demo_face
        demo_face()
    else:
        from . import demo_iris
        demo_iris()
