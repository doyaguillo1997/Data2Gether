import boto3
import botocore
from botocore.exceptions import ClientError
import pandas as pd


def aws_credentials(rol="dataScience", account_id="************"):
    """
    Funcion que devuelve las credenciales de un usuario temporal con el rol definido. Es necesario
    que el usuario que llama a la función tenga permisos para obtener dicho rol.
    :param rol: rol que se desea tomar
    :param account_id: id de la cuenta de la que se desean obtener los provilegios. Se debera de tener permisos de accesos
                        en la cuenta, asi como permisos para la obtención del rol seleccionado.

    :return: credenciales del rol.
    """
    import boto3
    sts_client = boto3.client('sts')  # Para el tema de seguridad hay que crear un cliente
    # para obtener datos de bajo nivel

    # Generamos un objeto con unas credenciales temporales del rol
    assumed_role_object = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{rol}",
        RoleSessionName=rol
    )
    # Pillamos las credenciales temporales de la api
    # asi podemos hacer todas las peticiones que queramos mientras esten los permisos.
    credentials = assumed_role_object['Credentials']
    return credentials


def aws_conexion_resource(resource, credentials):
    """
    Esta función permite crear recursos de aws de forma transparente, unicamente pasandole
    el recurso que queremos. No todos estan disponibles, en caso de fallo la funcion dira
    cuales estan disponibles.
    :param resource: un string con el recurso que queremos crear
    :param credentials: las credencial del rol que necesitemos para ejecutar el recurso. Usar
                        la funcion aws_credentials para obtenerlos.
    :return:
    """
    import boto3
    # Utilizamos las credenciales para conectarnos al S3. Aqui si que podemos utilizar
    # un resource.
    aws_resource = boto3.resource(
        resource,
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    return aws_resource


def aws_validacion_bucket(bucket):
    """
    Funcion para validar la existencia de un bucket en el S3. Debido a la construcción de las
    funciones de boto3 no se valida la existencia de los buckets. Esta función lo soluciona.
    :param bucket: Recibe como argumento un objeto bucket de boto3
    :return:  Devuelve true si el objeto existe.
    """
    import botocore
    s3 = aws_conexion_resource("s3", aws_credentials())
    exists = True
    try:
        s3.Bucket(bucket)
    except botocore.exceptions.ClientError as e:
        # Si obtenemos un error comprobamos que no sea un 404.
        # En caso de que sea un 404, el bucket no existira
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False
    return exists


def aws_df_from_S3_csv(file, bucket="data2gether-playground", index_col=None):
    """
    S3 (Simple Service Storage) permite almacenar cualquier tipo de archivo, esto se debe a
    que es un almacén de objetos, no de ficheros, por lo que su acceso es un poco más
    complejo. Esta función lo simplifica un poco. Por defecto accede al playground.

    :param bucket: Es el bucket al que vamos a acceder de nuestra cuenta.
    :param file: Es el archivo que queremos leer. Es necesario poner toda la ruta con las sub carpetas
                 que estén dentro del bucket.
    :param index_col: Columna que es indice del dataframe
    :return: Devuelve un dataframe de pandas.
    """

    credentials = aws_credentials()  # Esta función solo puede usar permisos de dataScience
    if aws_validacion_bucket(bucket):
        tmp_df = pd.read_csv(
            f"s3://{bucket}/{file}",
            storage_options={
                "key": credentials['AccessKeyId'],
                "secret": credentials['SecretAccessKey'],
                "token": credentials['SessionToken'],
            },
            index_col=index_col
        )
        return tmp_df
    else:
        print("Error, bucket no encontrado")
        return -1


def aws_subir_archivo_s3(bucket, file, route):
    """
    Permite subir un archivo al bucket de S3. Abstrae al sistema de carpetas
    convencional el almacenamiento de datos. Si se especifica una "carpeta" que
    no exista la crea en el bucket.

    :param bucket: Bucket al que subir el archivo
    :param file: Archivo que queremos subir al bucket.
    :param route: Ruta a la que subir el archivo. Concatena la ruta al nombre del fichero
                  en el bucket. No hay que poner barra al final.
    :return: True si se sube con exito el archivo, False si no.
    """
    if route[-1] == "/":  # Para evitar crear carpetas con /
        route = route[:-1]

    s3 = aws_conexion_resource("s3", aws_credentials())

    if aws_validacion_bucket(bucket):
        try:
            s3.Object(bucket, f'{route}/{file.split("/")[-1]}').put(Body=open(f'{file}', 'rb'))
        except ClientError as e:
            print(f"Error: {e}")
            return False
        return True
    else:
        print("Error: no existe el bucket")
        return False
