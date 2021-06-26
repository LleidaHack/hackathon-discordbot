USER_NOT_REGISTERED="¡Aún no te has registrado! Hazlo con el comando eps!login"


def USER_ALREADY_IN_TEAM(group_name):
    return f"¡Ya estás en el grupo {group_name}!"


def NOT_ALLOWED_TEAM(team_name):
    return f"No veo que te hayan invitado al grupo {team_name}"


def MEMBER_REGISTERED_IN(username, team_name):
    return f"¡Genial, {username}! Ya estas en el grupo {team_name}"

def MANY_INVITES(team_names):
    names = "# " + '\n# '.join(team_names)
    print(names)
    return f"""¡Ups! Veo que tienes más de una invitación, así que necesito que me especifiques a que equipo quieres unirte. Utiliza `eps!join <nombre del equipo>`.
    Actualmente tienes invitaciones pendientes para los siguientes equipos:
```cs
{names}
```
    """
def ANY_INVITE(username, discriminator):
    return f"No veo que tengas ninguna invitación... dile a tus compañeros que te inviten mediante el comando `eps!invite {username}#{discriminator}`"

def GROUP_LOST(group_name):
    return f"¡Qué desastre! Creo que se me ha perdido el equipo {group_name}. Puedes pedir que te vuelvan a invitar o crear tu propio equipo con `eps!create`."


ERROR_SERVER="¡Uy! Tengo problemas con Lo Servidor..."