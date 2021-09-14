import os.path


def modelsDirectory(path="./models"):
    """
    Genera las rutas necesarias para guardar los archivos de los modelos
    :param path: Ruta base a validar. Las carpetas intermedias no se pueden modificar
    :return:  None
    """
    if os.path.isdir(path):
        if not os.path.isdir(path+"/random"):
            os.mkdir(path+"/random")
        if not os.path.isdir(path+"/centered"):
            os.mkdir(path+"/centered")
    else:
        os.makedirs(path+"/random")
        os.makedirs(path+"/centered")


