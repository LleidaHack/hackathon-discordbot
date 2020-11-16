NOT_IN_GROUP = "¿Pero si aún no estás en ningún grupo! ¿A qué esperas?"
NOT_FOUND_PEOPLE = "Oye, ¿puedes volver a repetirlo? No estoy encontrado a tus amigos D:"
TEAM_OVERFLOW = "Oye, ¿no queréis ser demasiadas personas? El límite es de 4 participantes por equipo"


def MEMBER_REGISTERED_IN(name: str, role: str):
    return f"¡{name} añadido al grupo {role}!"


def ALREADY_IN_A_GROUP(username, group_name):
    return f"{username} está ya en otro grupo: {group_name}"
