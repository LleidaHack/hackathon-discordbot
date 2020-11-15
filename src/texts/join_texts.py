USER_NOT_REGISTERED="¡Aún no te has registrado! Hazlo con el comando eps!login"


def USER_ALREADY_IN_TEAM(group_name):
    return f"¡Ya estás en el grupo {group_name}!"


def NOT_ALLOWED_TEAM(team_name):
    return f"No veo que te hayan invitado al grupo {team_name}"


ERROR_SERVER="¡Uy! Tengo problemas con Lo Servidor..."


def MEMBER_REGISTERED_IN(username, team_name):
    return f"¡Genial, {username}! Ya estas en el grupo {team_name}"