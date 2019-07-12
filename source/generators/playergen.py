

# Local project imports
from source import globalvars, actor, death
from source.components import creature, container


def gen_player(tup_coords):

    x, y = tup_coords

    container_com = container.ComContainer()
    creature_com = creature.ComCreature("Rak", max_hp=20, base_atk=3, base_def=0, death_function=death.death_player)

    globalvars.PLAYER = actor.ObjActor(x, y, "Alligator",
                                       "A_PLAYER",
                                       animation_speed=1,
                                       creature=creature_com,
                                       container=container_com)

    globalvars.GAME.current_objects.append(globalvars.PLAYER)
