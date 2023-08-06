
from . import models

def int_to_tuple(rgbint):
    if rgbint == -1:
        return None
    else:
        return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

def parse_special(item):
    _type = int(item["t"])
    _coordinates = (float(item["p0"]), float(item["p1"]))

    # BUILDING BLOCKS
    if _type == 3:
        # I-Beam
        width = int(item["p2"])
        height = int(item["p3"])
        rotation = float(item["p4"])
        fixed = item["p5"] == "t"
        sleeping = item["p6"] == "t"

        parsed_special = models.BuildingBlock.IBeam(_coordinates, width, height, rotation, fixed, sleeping)

    if _type == 4:
        # Log
        width = int(item["p2"])
        height = int(item["p3"])
        rotation = float(item["p4"])
        fixed = item["p5"] == "t"
        sleeping = item["p6"] == "t"

        parsed_special = models.BuildingBlock.Log(_coordinates, width, height, rotation, fixed, sleeping)

    if _type == 27:
        # Rail
        width = int(item["p2"])
        height = int(item["p3"])
        rotation = float(item["p4"])

        parsed_special = models.BuildingBlock.Rail(_coordinates, width, height, rotation)

    # HAZARDS
    if _type == 29:
        # Arrow Gun
        rotation = float(item["p2"])
        fixed = item["p3"] == "t"
        fire_rate = int(item["p4"])
        ignore_player = item["p5"] == "t"

        parsed_special = models.Hazards.ArrowGun(_coordinates, rotation, fixed, fire_rate, ignore_player)
        
    if _type == 15:
        # Harpoon Gun
        rotation = float(item["p2"])
        has_anchor = item["p3"] == "t"
        fixed_angle = item["p4"] == "t"
        firing_angle = int(item["p5"])
        trigger_firing = item["p6"] == "t"
        starts_deactivated = item["p7"] == "t"

        parsed_special = models.Hazards.HarpoonGun(_coordinates, rotation, has_anchor, fixed_angle, firing_angle, trigger_firing, starts_deactivated)

    if _type == 25:
        # Homing Mine
        movement_speed = int(item["p2"])
        explode_delay = int(item["p3"])

        parsed_special = models.Hazards.HomingMine(_coordinates, movement_speed, explode_delay)

    if _type == 2:
        # Landmine
        rotation = float(item["p2"])

        parsed_special = models.Hazards.LandMine(_coordinates, rotation)

    if _type == 6:
        # Spike Set
        rotation = float(item["p2"])
        fixed = item["p3"] == "t"
        spikes = int(item["p4"])
        sleeping = item["p5"] == "t"

        parsed_special = models.Hazards.SpikeSet(_coordinates, rotation, fixed, spikes, sleeping)

    if _type == 7:
        # Wrecking Ball
        rope_length = int(item["p2"])

        parsed_special = models.Hazards.WreckingBall(_coordinates, rope_length)

    # MOVEMENT
    if _type == 33:
        # Cannon
        rotation = float(item["p2"])
        starting_rotation = int(item["p3"])
        firing_rotation = int(item["p4"])
        cannon_type = int(item["p5"])
        fire_delay = int(item["p6"])
        muzzle_scale = int(item["p7"])
        fire_power = int(item["p8"])

        parsed_special = models.Movement.Cannon(_coordinates, rotation, starting_rotation, firing_rotation, cannon_type, fire_delay, muzzle_scale, fire_power)

    if _type == 12:
        # Boost
        rotation = float(item["p2"])
        panels_amount = int(item["p3"])
        boost_power = int(item["p4"])

        parsed_special = models.Movement.Boost(_coordinates, rotation, panels_amount, boost_power)

    if _type == 8:
        # Fan
        rotation = float(item["p2"])

        parsed_special = models.Movement.Fan(_coordinates, rotation)

    if _type == 28:
        # Jet
        rotation = float(item["p2"])
        sleeping = item["p3"] == "t"
        power = int(item["p4"])
        firing_time = int(item["p5"])
        acceleration_time = int(item["p6"])
        fixed_angle = item["p7"] == "t"

        parsed_special = models.Movement.Jet(_coordinates, rotation, sleeping, power, firing_time, acceleration_time, fixed_angle)

    if _type == 5:
        # Spring Platform
        rotation = float(item["p2"])
        delay = float(item["p3"])

        parsed_special = models.Movement.SpringPlatform(_coordinates, rotation, delay)

    if _type == 35:
        # Paddle Platform
        rotation = float(item["p2"])
        delay = float(item["p3"])
        reverse = item["p4"] == "t"
        max_angle = float(item["p5"])
        speed = float(item["p6"])

        parsed_special = models.Movement.PaddlePlatform(_coordinates, rotation, delay, reverse, max_angle, speed)

    if _type == 17:
        # NPC
        rotation = float(item["p2"])
        type = int(item["p3"])
        sleeping = item["p4"] == "t"
        reverse = item["p5"] == "t"
        holds_pose = item["p6"] == "t"
        interactive = item["p7"] == "t"
        neck_angle = int(item["p8"])
        arm1_angle = int(item["p9"])
        arm2_angle = int(item["p10"])
        elbow1_angle = int(item["p11"])
        elbow2_angle = int(item["p12"])
        leg1_angle = int(item["p13"])
        leg2_angle = int(item["p14"])
        knee1_angle = int(item["p15"])
        knee2_angle = int(item["p16"])
        try:
            releases_joints = item["p17"] == "t"
        except KeyError:
            releases_joints = False

        parsed_special = models.NPC(_coordinates, rotation, type, sleeping, reverse, holds_pose, interactive, neck_angle,
                                    arm1_angle, arm2_angle, elbow1_angle, elbow2_angle, leg1_angle, leg2_angle, knee1_angle,
                                    knee2_angle, releases_joints)

    if _type == 34:
        # Blade Weapon
        rotation = float(item["p2"])
        reverse = item["p3"] == "t"
        sleeping = item["p4"] == "t"
        interactive = item["p5"] == "t"
        type = int(item["p6"])

        parsed_special = models.Miscelleneous.BladeWeapon(_coordinates, rotation, reverse, sleeping, interactive, type)

    if _type == 32:
        # Food Item
        rotation = float(item["p2"])
        sleeping = item["p3"] == "t"
        interactive = item["p4"] == "t"
        type = item["p5"]

        parsed_special = models.Miscelleneous.FoodItem(_coordinates, rotation, sleeping, interactive, type)

    if _type == 30:
        # Chain
        rotation = float(item["p2"])
        sleeping = item["p3"] == "t"
        interactive = item["p4"] == "t"
        link_count = int(item["p5"])
        link_scale = float(item["p6"])
        chain_curve = float(item["p7"])

        parsed_special = models.Miscelleneous.Chain(_coordinates, rotation, sleeping, interactive, link_count, link_scale, chain_curve)

    if _type == 18:
        # Glass Panel
        width = int(item["p2"])
        height = int(item["p3"])
        rotation = float(item["p4"])
        sleeping = item["p5"] == "t"
        strength = int(item["p6"])
        stabs = item["p7"] == "t"

        parsed_special = models.Miscelleneous.GlassPanel(_coordinates, width, height, rotation, sleeping, strength, stabs)

    if _type == 11:
        # Meteor
        width = int(item["p2"])
        height = int(item["p3"])
        fixed = item["p4"] == "t"
        sleeping = item["p5"] == "t"

        parsed_special = models.Miscelleneous.Meteor(_coordinates, width, height, fixed, sleeping)

    if _type == 1:
        # Dinner Table
        rotation = float(item["p2"])

        try:
            sleeping = item["p3"] == "t"
        except KeyError:
            sleeping = False

        try:
            interactive = item["p4"] == "t"
        except KeyError:
            interactive = True

        parsed_special = models.Miscelleneous.DinnerTable(_coordinates, rotation, sleeping, interactive)

    if _type == 19:
        # Chair
        rotation = float(item["p2"])
        reverse = item["p3"] == "t"

        try:
            sleeping = item["p4"] == "t"
        except KeyError:
            sleeping = False

        try:
            interactive = item["p5"] == "t"
        except KeyError:
            interactive = True

        parsed_special = models.Miscelleneous.Chair(_coordinates, rotation, reverse, sleeping, interactive)

    if _type == 20:
        # Bottle
        rotation = float(item["p2"])
        type = int(item["p3"])
        sleeping = item["p4"] == "t"
        interactive = item["p5"] == "t"

        parsed_special = models.Miscelleneous.Bottle(_coordinates, rotation, type, sleeping, interactive)

    if _type == 21:
        # Television
        rotation = float(item["p2"])
        sleeping = item["p3"] == "t"
        interactive = item["p4"] == "t"

        parsed_special = models.Miscelleneous.Television(_coordinates, rotation, sleeping, interactive)

    if _type == 22:
        # Boombox
        rotation = float(item["p2"])
        sleeping = item["p3"] == "t"
        interactive = item["p4"] == "t"

        parsed_special = models.Miscelleneous.Boombox(_coordinates, rotation, sleeping, interactive)

    if _type == 10:
        # Soccer Ball

        parsed_special = models.Miscelleneous.SoccerBall(_coordinates)

    if _type == 0:
        # Van
        rotation = float(item["p2"])
        sleeping = item["p3"] == "t"
        interactive = item["p4"]

        parsed_special = models.Miscelleneous.Van(_coordinates, rotation, sleeping, interactive)

    if _type == 23:
        # Sign
        rotation = float(item["p2"])
        type = int(item["p3"])
        shows_post = item["p4"] == "t"

        parsed_special = models.Miscelleneous.Sign(_coordinates, rotation, type, shows_post)

    if _type == 26:
        # Trash Can
        rotation = float(item["p2"])
        sleeping = item["p3"] == "t"
        interactive = item["p4"] == "t"
        contains_trash = item["p5"] == "t"

        parsed_special = models.Miscelleneous.TrashCan(_coordinates, rotation, sleeping, interactive, contains_trash)

    if _type == 24:
        # Toilet
        rotation = float(item["p2"])
        reverse = item["p3"] == "t"
        sleeping = item["p4"] == "t"
        interactive = item["p5"] == "t"

        parsed_special = models.Miscelleneous.Toilet(_coordinates, rotation, reverse, sleeping, interactive)

    if _type == 31:
        # Token
        type = int(item["p2"])

        parsed_special = models.Miscelleneous.Token(_coordinates, type)

    if _type == 9:
        # Finish Line

        parsed_special = models.Miscelleneous.FinishLine(_coordinates)

    if _type == 16:
        # Text
        rotation = float(item["p2"])
        text_color = int_to_tuple(int(item["p3"]))
        font = int(item["p4"])
        font_size = int(item["p5"])
        alignment = int(item["p6"])
        text = item.p7.text

        try:
            opacity = int(item["p8"])
        except KeyError:
            opacity = 100

        parsed_special = models.Text(_coordinates, rotation, text_color, font, font_size, alignment, opacity, text)

    if _type in [13, 14]:
        # Building Block Brick & Modern
        floor_width = int(item["p2"])
        floor_amount = int(item["p3"])
        type = _type

        parsed_special = models.Building(_coordinates, floor_width, floor_amount, type)

    return parsed_special
