from src.texts.const import *

ALREADY_ON_GROUP_ERROR =f"¡Ups! Por lo que veo ya estás en un equipo. Debes hacer `{COMMAND_PREFIX}leave` antes de poder unirte a uno nuevo"
NOT_REGISTERED_ERROR = f"¡Ups! Parece que no estás conectado a tu cuenta de HackEPS. Escribe `{COMMAND_PREFIX}login` para volver a iniciar el proceso de registro."
def NOT_INGROUP_ERROR(author):
    return f"Parece que no apuntaste ningún grupo. Puedes usar los canales de reclutamiento para buscar equipo. Con el comando `{COMMAND_PREFIX}create` puedes crear un equipo o pídele a tus compañeros que te inviten mediante `{COMMAND_PREFIX}invite {author}`"