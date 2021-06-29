from src.texts.const import *

NOT_REGISTERED_ERROR = f"¡Ups! Parece que no estás conectado a tu cuenta de {EVENT_NAME}. Escribe {COMMAND_PREFIX}register para volver a iniciar el proceso de registro."
SINTAXIS_ERROR = f"El comando para crear el equipo debe incluír el nombre del equipo. Vuelve a intentarlo con la sintaxis ```{COMMAND_PREFIX}create <Nombre del equipo``` o utiliza ```{COMMAND_PREFIX}help``` para más información."
ALREADY_ON_GROUP_ERROR = f"¡Más tranqulo hacker! Parece que ya estás en un grupo. Si necesitas cambiar de equipo, utiliza ```{COMMAND_PREFIX}leave``` para abandonar el equipo primero."
GROUP_ALREADY_EXISTS_ERROR = "Parece que algún Hackepsito ya ha registrado este nombre de grupo... Prueba con otro :)"
CREATED_GROUP = f"¡EPSelente! ¡Grupo creado! Ya puedes invitar a tus compañeros de equipo con ```{COMMAND_PREFIX}invite <correo o discordTag>```. También te he preparado un cómodo canal de chat y voz para que compartas con tus compañeros."
STARTING_CREATE_GROUP = "Ajá. Parece que todo está en orden, dame unos segundos que realizo el ritual de creación de grupo."