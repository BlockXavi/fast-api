# Importo las bibliotecas que contienen las clases FastAPI y de Bases de Datos
# EJER.3 - Añadimos el import de HTTPException
from fastapi import FastAPI, HTTPException
# EJER.3 - Añadimos las importaciones de constr y EmailStr para la validación
from pydantic import BaseModel, constr, EmailStr

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Simulamos una base de datos en memoria
database = {}

# Define modelos de datos utilizando la clase BaseModel de Pydantic para una entidad "Usuario"
# EJER.3 - Añade validaciones a los modelos de datos existentes. Por ejemplo, especifica que
# EJER.3 - el campo "name" debe tener una longitud mínima y máxima, o que el campo "email" debe
# EJER.3 - tener un formato de correo electrónico válido
class User(BaseModel):
  id: int
  name: constr(min_length=1, max_length=50)
  email: EmailStr
  age: int
  
# Añade rutas y funciones de controlador para cada operación CRUD
  
# Crear usuario
# EJER.3 - Implementa validaciones en las rutas de la API. Asegúrate
# EJER.3 - de que los datos proporcionados en una solicitud de
# EJER.3 - creación de usuario son válidos antes de insertarlos en la
# EJER.3 - base de datos.
# EJER.3 - Modificamos la ruta create user añadiendo las respuestas de error usando HTTPException
@app.post("/users")
def create_user(user: User):
   # Comprovamos si el el id introducido esta ya en uso
   if user.id in database:
      # Si el usuario con el id introducido ya existe, devolvemos un error
      raise HTTPException(
            status_code=400, detail="El Usuario con el id introducido ya existe")
   # Comprovamos si el el email introducido esta ya en uso
   if user.email in database:
      # Si el usuario con el email introducido ya existe, devolvemos un error
      raise HTTPException(
            status_code=400, detail="El Usuario con el email introducido ya existe")
   # Simulamos la creacion del usuario en la base de datos
   database[user.id] = user
   # Devolvemos un mensaje para hacer saber que el usuario se ha creado correctamente
   return {"message": "Usuario creado correctamente"}
    
# Obtener todos los usuarios
# EJER.2 - Modificar la función get_all_users para permitir la recuperación de usuarios utilizando
# EJER.2 - parámetros de consulta (query params) para filtrar por nombre y/o correo electrónico
# EJER.2 - y/o edad.
@app.get("/users")
def get_all_users(name: str = None, email: str = None, age: int = None):
    # Lista para almacenar los usuarios filtrados
    filtered_users = []

    # Iterar sobre todos los usuarios en la base de datos
    for user in database.values():
        # Verificar si se proporcionan tanto el nombre, el correo electrónico y la edad
        if name and email and age:
            # Si el nombre, el correo electrónico y la edad coinciden con los proporcionados, se agrega el usuario a la lista filtrada
            if user.name == name and user.email == email and user.age == age:
                filtered_users.append(user)
        # Verificar si se proporciona solo el nombre y la edad
        elif name and age:
            # Si el nombre y la edad coinciden con los proporcionados, se agrega el usuario a la lista filtrada
            if user.name == name and user.age == age:
                filtered_users.append(user)
        # Verificar si se proporciona solo el correo electrónico y la edad
        elif email and age:
            # Si el correo electrónico y la edad coinciden con los proporcionados, se agrega el usuario a la lista filtrada
            if user.email == email and user.age == age:
                filtered_users.append(user)
        # Verificar si se proporciona solo el nombre
        elif name:
            # Si el nombre coincide con el proporcionado, se agrega el usuario a la lista filtrada
            if user.name == name:
                filtered_users.append(user)
        # Verificar si se proporciona solo el correo electrónico
        elif email:
            # Si el correo electrónico coincide con el proporcionado, se agrega el usuario a la lista filtrada
            if user.email == email:
                filtered_users.append(user)
        # Verificar si se proporciona solo la edad
        elif age:
            # Si la edad coincide con la proporcionada, se agrega el usuario a la lista filtrada
            if user.age == age:
                filtered_users.append(user)
        # Si no se proporcionan ni el nombre, el correo electrónico ni la edad, se agrega el usuario a la lista filtrada
        else:
            filtered_users.append(user)
    # Devolver la lista de usuarios filtrados
    return filtered_users

# Obtener un usuario por ID
# EJER.3 - Modificamos la ruta get user añadiendo las respuestas de error usando HTTPException
@app.get("/users/{user_id}")
def get_user(user_id: int = None):
   # Recuperamos el usuario de nuestra base de datos en memoria
   user = database.get(user_id)
   # Si hemos encontrado el usuario, lo develolvemos como respuesta
   if user:
      return user
   # En caso de no encontrarlo, devolvemos un error con codio 404
   raise HTTPException(
      status_code=404, detail="Usuario no encontrado")

# Actualizar un usuario
# EJER.3 - Modificamos la ruta update user añadiendo las respuestas de error usando HTTPException
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
   # Comprovamos si el usuario con el id pasado existe.
   if user_id in database:
      # En caso de existir actualizamos el usuaro con los nuevos datos.
      database[user_id] = user
      # Devolvemos un mensaje para informar de que se ha actualizado correctamente.
      return {"message": "Usuario actualizado correctamente"}
   # En caso de no encontrarlo, devolvemos un error con codio 404
   raise HTTPException(
      status_code=404, detail="Usuario no encontrado")

# Eliminar un usuario
# EJER.3 - Modificamos la ruta delete user añadiendo las respuestas de error usando HTTPException
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
   # Comprovamos si el usuario con el id pasado existe.
   if user_id in database:
      # Elimina el usuario de la base de datos simulada
      del database[user_id]
      # Devolvemos un mensaje para informar de que se ha borrado correctamente.
      return {"message": "Usuario eliminado correctamente"}
   # En caso de no encontrarlo, devolvemos un error con codio 404
   raise HTTPException(
      status_code=404, detail="Usuario no encontrado")

