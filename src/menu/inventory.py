import pygame
import textwrap

from src import constants, globalvars, text, draw, game, gui

# initialize potential buttons
use_btn = gui.GuiButton(globalvars.SURFACE_MAIN, "", (0, 0), (0, 0))
drop_btn = gui.GuiButton(globalvars.SURFACE_MAIN, "", (0, 0), (0, 0))


def menu_inventory():
    """Displays the inventory menu when PLAYER accesses the inventory.

    Menu allows PLAYER to look at stored items and use or equip them.

    Returns
    -------
    None
    """
    menu_width = 809
    menu_height = 384

    first_frame_x, first_frame_y = 264, 71

    frame_x_spacing = 56
    frame_y_spacing = 52

    # (x, y) coordinates for the topleft corner of the menu
    menu_x = (constants.CAMERA_WIDTH/2) - (menu_width/2)
    menu_y = (constants.CAMERA_HEIGHT/2) - (menu_height/2)

    inventory_surface = pygame.Surface((menu_width, menu_height))

    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    menu_close = False
    globalvars.PLAYER.container.currently_displayed_item_info = None
    while not menu_close:

        draw.draw_game()

        # mouse control inside menu
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rel_x = mouse_x - menu_x
        mouse_rel_y = mouse_y - menu_y

        mouse_clicked = False
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                game.game_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # left-click is 1, right is 3, scroll up is 4 and down is 5
                if event.button == 1:
                    mouse_clicked = True

        # exit menu if mouse clicks outside its boundaries
        if mouse_clicked and (mouse_rel_y < 0 or mouse_rel_x < 0
                              or mouse_rel_x > menu_width or mouse_rel_y > menu_height):
            menu_close = True

        player_input = ((mouse_rel_x, mouse_rel_y), mouse_clicked, event_list)
        inventory_surface.blit(globalvars.ASSETS.S_INVENTORY, (0, 0))

        obj_selected = None

        # display items icons onto inventory surface
        for num, item in enumerate(globalvars.PLAYER.container.inventory):
            row = num // 5
            col = num % 5
            item_x = first_frame_x + col * frame_x_spacing
            item_y = first_frame_y + row * frame_y_spacing

            mouse_hover = (item_x < mouse_rel_x < item_x + 32
                           and item_y < mouse_rel_y < item_y + 32)

            item_clicked, item.item.hover_sound_played = gui.hovered_clickable_element(
                mouse_hover, mouse_clicked, item.item.hover_sound_played, change_cursor=False)
            if mouse_hover:
                inventory_surface.blit(globalvars.ASSETS.S_INVENTORY_SELECT,
                                       (item_x - 2, item_y - 2))

            if item_clicked:
                obj_selected = item

            # transfer equipment items to the equipment menu if equipped
            if item.equipment is not None and item.equipment.equipped:
                globalvars.PLAYER.container.equipped_inventory.append(item)
                globalvars.PLAYER.container.inventory.remove(item)
                break

            inventory_surface.blit(globalvars.ASSETS.animation_dict[item.animation_key][0],
                                   (item_x, item_y))

        # display equipment menu
        equipment_menu(inventory_surface, player_input)

        # display PLAYER stats
        display_stats(inventory_surface)

        # display PLAYER total gold
        gold_value = f"{globalvars.PLAYER.gold}"

        gold_coords = (346 - text.get_text_width(constants.FONT_BEST, gold_value), 327)
        text.draw_text(inventory_surface, gold_value, constants.FONT_BEST, gold_coords,
                       (255, 229, 26))

        # display item information in the info side menu
        if obj_selected is not None:
            globalvars.PLAYER.container.currently_displayed_item_info = obj_selected
        if globalvars.PLAYER.container.currently_displayed_item_info is not None:
            obj_state = display_item_info(
                inventory_surface, globalvars.PLAYER.container.currently_displayed_item_info,
                player_input)

            if globalvars.PLAYER.container.currently_displayed_item_info is not None \
                    and globalvars.PLAYER.container.currently_displayed_item_info.equipment is None and obj_state == "used":
                menu_close = True
        if menu_close:
            break

        globalvars.SURFACE_MAIN.blit(inventory_surface, (menu_x, menu_y))
        globalvars.CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()


def equipment_menu(surface, player_input):
    """Displays the equipment menu to the left of the inventory and monitors any actions inside.

    Parameters
    ----------
    surface : pygame Surface obj
        Surface to display the item icons on (normally inventory_surface).
    player_input : tuple
        Tuple that contains ((mouse_rel_x, mouse_rel_y), mouse_clicked, event_list)

    Returns
    -------
    None
    """

    mouse_rel_x, mouse_rel_y = player_input[0]
    mouse_clicked = player_input[1]

    equipment_selected = None

    for equipped_item in globalvars.PLAYER.container.equipped_inventory:

        if equipped_item.equipment.slot == "weapon":
            item_x, item_y = 165, 149
        elif equipped_item.equipment.slot == "shield":
            item_x, item_y = 31, 149
        elif equipped_item.equipment.slot == "head":
            item_x, item_y = 98, 71
        elif equipped_item.equipment.slot == "boots":
            item_x, item_y = 98, 214
        else:
            item_x, item_y = 0, 0

        mouse_hover = (item_x < mouse_rel_x < item_x + 32 and item_y < mouse_rel_y < item_y + 32)

        item_clicked, equipped_item.item.hover_sound_played = \
            gui.hovered_clickable_element(mouse_hover, mouse_clicked,
                                          equipped_item.item.hover_sound_played,
                                          change_cursor=False)

        if mouse_hover:
            surface.blit(globalvars.ASSETS.S_INVENTORY_SELECT, (item_x - 2, item_y - 2))

        if item_clicked:
            equipment_selected = equipped_item

        # transfer equipment item to inventory if unequipped
        if not equipped_item.equipment.equipped:
            globalvars.PLAYER.container.inventory.append(equipped_item)
            globalvars.PLAYER.container.equipped_inventory.remove(equipped_item)
            break

        surface.blit(globalvars.ASSETS.animation_dict[equipped_item.animation_key][0], (item_x, item_y))

    if equipment_selected is not None:
        globalvars.PLAYER.container.currently_displayed_item_info = equipment_selected


def display_item_info(surface, target_item, player_input):
    """Displays all information about the `target_item` and provides options to use/drop the item.

    Parameters
    ----------
    surface : pygame Surface obj
        Surface to display the item icons on (normally inventory_surface).
    target_item : ComItem obj
        The item to have its info displayed.
    player_input : tuple
        Tuple that contains ((mouse_rel_x, mouse_rel_y), mouse_clicked, event_list)

    Returns
    -------
    None or str
        A string "used" is returned if the item was used, otherwise None is returned.
    """
    info_width, info_height = 212, 269
    info_x, info_y = 557, 73
    info_surface = pygame.Surface((info_width, info_height))
    info_center = (info_width // 2, info_height // 2)

    mouse_info_x = player_input[0][0] - info_x
    mouse_info_y = player_input[0][1] - info_y
    event_and_mouse = (player_input[2], (mouse_info_x, mouse_info_y))

    # draw item title
    title_y = 16
    title_x = info_center[0]
    text.draw_text(info_surface, target_item.display_name, constants.FONT_BEST, (title_x, title_y),
                   constants.COLOR_BLACK, center=True)

    # draw item description
    item_desc = target_item.item.item_desc

    text_height = text.get_text_height(constants.FONT_BEST)
    text_x = 10
    start_y = title_y + text_height // 2 + 16
    last_y = start_y

    new_msg_lines = textwrap.wrap(item_desc, 24)
    for i, text_line in enumerate(new_msg_lines):
        last_y = start_y + (i * text_height)
        text.draw_text(info_surface, text_line, constants.FONT_BEST, (text_x, last_y),
                       constants.COLOR_BLACK)

    # draw any bonus attributes
    if target_item.equipment is not None:
        atk_bonus = target_item.equipment.attack_bonus
        def_bonus = target_item.equipment.defence_bonus

        if target_item.equipment.equipped:
            use_btn_text = "Unequip"
        else:
            use_btn_text = "Equip"

        bonus_y = last_y + (2 * text_height)

        if atk_bonus > 0:
            text.draw_text(info_surface, f"+{atk_bonus}   Attack", constants.FONT_BEST,
                           (text_x, bonus_y), constants.COLOR_GRASS_GREEN)
            bonus_y += text_height + 10

        if def_bonus > 0:
            text.draw_text(info_surface, f"+{def_bonus}   Defence", constants.FONT_BEST,
                           (text_x, bonus_y), constants.COLOR_GRASS_GREEN)

    else:
        use_btn_text = "Use"

    # draw use/drop button equip/unequip button
    btn_width = 80
    btn_height = 32

    use_btn_x = info_center[0] - (btn_width // 2) - 8
    use_btn_y = info_height - btn_height - 10

    use_btn.surface = info_surface
    use_btn.text = use_btn_text
    use_btn.coords_center = (use_btn_x, use_btn_y)
    use_btn.size = (btn_width, btn_height)

    drop_btn_x = info_center[0] + (btn_width // 2) + 8
    drop_btn_y = info_height - btn_height - 10
    drop_btn.surface = info_surface
    drop_btn.text = "Drop"
    drop_btn.coords_center = (drop_btn_x, drop_btn_y)
    drop_btn.size = (btn_width, btn_height)

    if use_btn.update(event_and_mouse):
        target_item.item.use()
        return "used"

    if drop_btn.update(event_and_mouse):
        target_item.item.drop(globalvars.PLAYER.x, globalvars.PLAYER.y)
        globalvars.PLAYER.container.currently_displayed_item_info = None

    use_btn.draw()
    drop_btn.draw()

    surface.blit(info_surface, (info_x, info_y))


def display_stats(surface):
    stats_surface_width, stats_surface_height = 170, 90
    stats_x, stats_y = 29, 266
    stats_surface = pygame.Surface((stats_surface_width, stats_surface_height))
    stats_font = constants.FONT_BEST
    text_height = text.get_text_height(stats_font)

    atk_text = "Atk:"
    def_text = "Def:"
    atk_value = f"{globalvars.PLAYER.creature.attack_points}"
    def_value = f"{globalvars.PLAYER.creature.defence}"
    crit_chance_text = "Crit Chance:"
    crit_dmg_text = "Crit Dmg:"
    crit_chance_val = f"{globalvars.PLAYER.creature.crit_chance}%"
    crit_dmg_val = f"{int(globalvars.PLAYER.creature.crit_dmg * 100)}%"

    exp_text = "Total Exp:"
    exp_value = f"{globalvars.PLAYER.exp_total}"

    atk_text_coords = (6, 4)
    atk_value_coords = (stats_surface_width - text.get_text_width(stats_font, atk_value) - 6, 4)

    def_text_coords = (6, atk_text_coords[1] + text_height + 1)
    def_value_coords = (stats_surface_width - text.get_text_width(stats_font, def_value) - 6,
                        atk_text_coords[1] + text_height + 1)

    crit_chance_text_coords = (6, def_text_coords[1] + text_height + 1)
    crit_chance_value_coords = (stats_surface_width - text.get_text_width(stats_font,
                                                                          crit_chance_val) - 6,
                                def_text_coords[1] + text_height + 1)

    crit_dmg_text_coords = (6, crit_chance_text_coords[1] + text_height + 1)
    crit_dmg_value_coords = (stats_surface_width - text.get_text_width(stats_font,
                                                                       crit_dmg_val) - 6,
                             crit_chance_text_coords[1] + text_height + 1)

    exp_text_coords = (6, crit_dmg_text_coords[1] + text_height + 1)
    exp_value_coords = (stats_surface_width - text.get_text_width(stats_font, exp_value) - 6,
                        crit_dmg_text_coords[1] + text_height + 1)

    text.draw_text(stats_surface, atk_text, stats_font, atk_text_coords, pygame.Color("#112d4e"))
    text.draw_text(stats_surface, atk_value, stats_font, atk_value_coords, pygame.Color("#3f72af"))

    text.draw_text(stats_surface, def_text, stats_font, def_text_coords, pygame.Color("#112d4e"))
    text.draw_text(stats_surface, def_value, stats_font, def_value_coords, pygame.Color("#3f72af"))

    text.draw_text(stats_surface, crit_chance_text, stats_font, crit_chance_text_coords,
                   pygame.Color("#112d4e"))
    text.draw_text(stats_surface, crit_chance_val, stats_font, crit_chance_value_coords,
                   pygame.Color("#3f72af"))

    text.draw_text(stats_surface, crit_dmg_text, stats_font, crit_dmg_text_coords,
                   pygame.Color("#112d4e"))
    text.draw_text(stats_surface, crit_dmg_val, stats_font, crit_dmg_value_coords,
                   pygame.Color("#3f72af"))

    text.draw_text(stats_surface, exp_text, stats_font, exp_text_coords, pygame.Color("#521262"))
    text.draw_text(stats_surface, exp_value, stats_font, exp_value_coords, pygame.Color("#6639a6"))

    surface.blit(stats_surface, (stats_x, stats_y))
