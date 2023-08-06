import argparse
import random
import re
import textwrap
import webbrowser

import tortilla

DEFAULT_PAGINA = "python-ecuador"


def get_argparser():
    """
    Agregar argumentos y opciones para la interfaz de línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description="Escoge al azar uno o varios asistentes de un meetup."
    )
    parser.add_argument(
        "-n",
        "--numero",
        type=int,
        default=1,
        help="Número de asistentes a escoger.",
    )
    parser.add_argument(
        "--no-abrir-perfil",
        action="store_true",
        help="No abrir el perfil de cada ganador en el navegador",
    )
    parser.add_argument("evento", type=str, help="URL o id del evento.")
    return parser


def get_asistentes(pagina, evento):
    """
    Obtener asistenes de un evento usando la API de meetup.

    Más información en la documentación oficial de meetup:
    https://www.meetup.com/es/meetup_api/docs/:urlname/events/:id/attendance/
    """
    api = tortilla.wrap(f"https://api.meetup.com/{pagina}")
    return api.events(evento).attendance.get()


def procesar_evento(evento):
    """
    Obtener el id y nombre de la página dado el id o URL del evento.

    Si el evento es sólo un id
    la página será dada por `DEFAULT_PAGINA`.
    """
    regex_solo_id = re.compile(r"\d+")
    regex_full_url = re.compile(
        r"(https?://)?www.meetup.com/"  # puede tener el protocolo
        r"(\w+/)?"  # puede tener el lenguage
        r"(?P<pagina>.+)/events/(?P<evento>\d+)/?"
    )
    if regex_solo_id.match(evento):
        return DEFAULT_PAGINA, evento
    match = regex_full_url.match(evento)
    if match:
        match_dict = match.groupdict()
        return match_dict["pagina"], match_dict["evento"]
    else:
        raise Exception("URL no válida.")


def seleccionar_ganadores(pagina, evento, numero):
    """
    Seleccionar `numero` asistentes de un evento de manera aleatoria.

    Los asistentes deben haber respondido que si al evento.
    """
    asistentes = get_asistentes(pagina, evento)
    asistentes_presentes = {
        asistente["member"]["id"]: asistente
        for asistente in asistentes
        if asistente["rsvp"]["response"] == "yes"
    }
    print(
        "Asistentes presentes "
        f"{len(asistentes_presentes)}/{len(asistentes)}"
    )
    for _ in range(min(numero, len(asistentes_presentes))):
        seleccionado = random.choice(list(asistentes_presentes.values()))
        asistentes_presentes.pop(seleccionado["member"]["id"])
        yield seleccionado


def mostrar_ganador(miembro, abrir_perfil=False, **kwargs):
    """
    Mostrar el nombre y perfil del ganador.

    Si `abrir_perfil` es `True`,
    se abrirá el perfil del ganador en el navegador.
    """
    nombre = miembro["member"]["name"]
    id_ = miembro["member"]["id"]
    perfil = f"https://www.meetup.com/python-ecuador/members/{id_}"
    mensaje = textwrap.dedent(
        f"""
        *** Ganador(a) ***
        ¡Felicitacines {nombre}!
        {perfil}
    """
    )
    print(mensaje, **kwargs)
    if abrir_perfil:
        webbrowser.open(perfil)


def main():
    args = get_argparser().parse_args()
    try:
        pagina, evento = procesar_evento(args.evento)
    except Exception as e:
        print(e)
        exit(1)
    ganadores = seleccionar_ganadores(pagina, evento, numero=args.numero)
    for ganador in ganadores:
        mostrar_ganador(ganador, not args.no_abrir_perfil)


if __name__ == "__main__":
    main()
