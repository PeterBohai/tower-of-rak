from source import globalvars, actor, death
from source.components import creature, container


def gen_player(tup_coords):

    x, y = tup_coords

    container_com = container.ComContainer()
    creature_com = creature.ComCreature("Rak", max_hp=25, base_atk=1, base_def=10, death_function=death.death_player)

    globalvars.PLAYER = actor.ObjActor(x, y, "PLAYER",
                                       "A_PLAYER_LEFT",
                                       animation_speed=0.8,
                                       creature=creature_com,
                                       container=container_com)

    globalvars.GAME.current_objects.append(globalvars.PLAYER)
