from src import globalvars, actor, death
from src.components import creature, container


def gen_player(coord):
    """Generates the PLAYER at the map-grid `coord`.

    Parameters
    ----------
    coord : tuple
        The map tile coordinates to place the PLAYER.

    Returns
    -------
    None

    """
    container_com = container.ComContainer()
    creature_com = creature.ComCreature("Rak", max_hp=25, base_atk=1, base_def=3, death_function=death.death_player)

    globalvars.PLAYER = actor.ObjActor(*coord, "PLAYER", "A_PLAYER_LEFT", animation_speed=0.8,
                                       creature=creature_com,
                                       container=container_com)

    globalvars.GAME.current_objects.append(globalvars.PLAYER)
