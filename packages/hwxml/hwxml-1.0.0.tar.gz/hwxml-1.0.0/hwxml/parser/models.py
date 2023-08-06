# -*- coding: utf-8 -*-

from collections import Iterable

class XML:
    def __init__(self, text_xml, version, character, background, shapes, joints, special_items, groups):
        self.text_xml = text_xml
        self.version = version
        self.character = character
        self.background = background
        self.shapes = shapes
        self.joints = joints
        self.special_items = special_items
        self.groups = groups

    def _flatten(self, l):
        for el in l:
            if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
                yield from self._flatten(el)
            else:
                yield el

    def get_all_shapes(self):
        shapes = []
        shapes.append(self.shapes)

        for _group in self.groups:
            for _shape in [item for item in _group.items if type(item) == Shape]:
                shapes.append(_shape)

        return list(self._flatten(shapes))

    def get_all_of_polygons(self):
        polygons = []
        polygons.append([shape.polygon for shape in self.get_all_shapes() if shape.polygon])

        for _group in self.groups:
            for _shape in [item for item in _group.items if type(item) == Shape]:
                if _shape.polygon:
                    polygons.append(_shape.polygon)

        return list(self._flatten(shapes))

class Character:
    def __init__(self, coordinates, type, forced, vehicle_hidden):
        self.coordinates = coordinates
        self.type = type
        self.forced = forced
        self.vehice_hidden = vehicle_hidden

        self.name = {1: "Wheelchair Guy",
                     2: "Segway Guy",
                     3: "Irresponsible Dad",
                     4: "Effective Shopper",
                     5: "Moped Couple",
                     6: "Lawnmower Man",
                     7: "Explorer Guy",
                     8: "Santa Claus",
                     9: "Pogostick Man",
                     10: "Irresponsible Mom",
                     11: "Helicopter Man"}[self.type]

    def __repr__(self):
        return "<Character {}>".format(self.name)

class Background:
    def __init__(self, type, color):
        self.type = type
        self.color = color

    def __repr__(self):
        return "<Background Type={}>".format(self.type)

class Shape:
    def __init__(self, 
                 coordinates, 
                 type, 
                 interactive,
                 width,
                 height,
                 rotation,
                 fixed,
                 sleeping,
                 density,
                 color,
                 outline,
                 opacity,
                 collision,
                 cutout=None,
                 polygon=None):
        self.coordinates = coordinates
        self.type = type
        self.interactive = interactive
        self.width = width
        self.height = height
        self.rotation = rotation
        self.fixed = fixed
        self.sleeping = sleeping
        self.density = density
        self.color =  color
        self.outline = outline
        self.opacity = opacity
        self.collision = collision

        self.cutout = cutout
        self.polygon = polygon

    def __repr__(self):
        return "<Shape Type={}>".format(self.type)

class Polygon:
    def __init__(self, id, number_polygons, points, original):
        self.id = id
        self.number_polygons = number_polygons
        self.points = points
        self.original = original

    def __repr__(self):
        return "<Polygon>"

class Joint:
    def __init__(self, 
                 coordinates, 
                 type, 
                 first_connection, 
                 second_connection,
                 collide_connected,
                 axis_angle=None,
                 upper_angle=None,
                 lower_angle=None,
                 upper_limit=None,
                 lower_limit=None,
                 motor_torque=None,
                 motor_force=None,
                 motor_speed=None):
        self.coordinates = coordinates
        self.type = type
        self.first_connection = first_connection
        self.second_connection = second_connection
        self.collide_connected = collide_connected

        self.axis_angle = axis_angle
        self.upper_angle = upper_angle
        self.lower_angle = lower_angle
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.motor_torque = motor_torque
        self.motor_force = motor_force
        self.motor_speed = motor_speed

    def __repr__(self):
        return "<Joint Type={}>".format(self.type)

class BuildingBlock:
    class IBeam:
        def __init__(self, coordinates, width, height, rotation, fixed, sleeping):
            self.coordinates = coordinates
            self.width = width
            self.height = height
            self.rotation = rotation
            self.fixed = fixed
            self.sleeping = sleeping

        def __repr__(self):
            return "<IBeam>"

    class Log:
        def __init__(self, coordinates, width, height, rotation, fixed, sleeping):
            self.coordinates = coordinates
            self.width = width
            self.height = height
            self.rotation = rotation
            self.fixed = fixed
            self.sleeping = sleeping

        def __repr__(self):
            return "<Log>"

    class Rail:
        def __init__(self, coordinates, width, height, rotation):
            self.coordinates = coordinates
            self.width = width
            self.height = height
            self.rotation = rotation

        def __repr__(self):
            return "<Rail>"

class Hazards:
    class ArrowGun:
        def __init__(self, coordinates, rotation, fixed, fire_rate, ignore_player):
            self.coordinates = coordinates
            self.rotation = rotation
            self.fixed = fixed
            self.fire_rate = fire_rate
            self.ignore_player = ignore_player

        def __repr__(self):
            return "<ArrowGun>"

    class HarpoonGun:
        def __init__(self, coordinates, rotation, has_anchor, is_fixed_angle, firing_angle, trigger_firing, starts_deactivated):
            self.coordinates = coordinates
            self.rotation = rotation
            self.has_anchor = has_anchor
            self.is_fixed_angle = is_fixed_angle
            self.firing_angle = firing_angle
            self.trigger_firing = trigger_firing
            self.starts_deactivated = starts_deactivated

        def __repr__(self):
            return "<HarpoonGun>"

    class HomingMine:
        def __init__(self, coordinates, movement_speed, explode_delay):
            self.coordinates = coordinates
            self.movement_speed = movement_speed
            self.explode_delay = explode_delay

        def __repr__(self):
            return "<HomingMine>"

    class LandMine:
        def __init__(self, coordinates, rotation):
            self.coordinates = coordinates
            self.rotation = rotation

        def __repr__(self):
            return "<Landmine>"

    class SpikeSet:
        def __init__(self, coordinates, rotation, fixed, spikes, sleeping):
            self.coordinates = coordinates
            self.rotation = rotation
            self.fixed = fixed
            self.sleeping = sleeping
            self.spikes = spikes

        def __repr__(self):
            return "<Spikeset>"

    class WreckingBall:
        def __init__(self, coordinates, rope_length):
            self.coordinates = coordinates
            self.rope_length = rope_length

        def __repr__(self):
            return "<WreckingBall>"

class Movement:
    class Cannon:
        def __init__(self, 
                     coordinates, 
                     rotation, 
                     starting_rotation, 
                     firing_rotation, 
                     cannon_type, 
                     fire_delay, 
                     muzzle_scale, 
                     fire_power):
            self.coordinates = coordinates
            self.rotation = rotation
            self.starting_rotation = starting_rotation
            self.firing_rotation = firing_rotation
            self.cannon_type = cannon_type
            self.fire_delay = fire_delay
            self.muzzle_scale = muzzle_scale
            self.fire_power = fire_power

        def __repr__(self):
            return "<Cannon Type={}>".format(self.cannon_type)

    class Boost:
        def __init__(self, coordinates, rotation, panels_amount, boost_power):
            self.coordinates = coordinates
            self.rotation = rotation
            self.panels_amount = panels_amount
            self.boost_power = boost_power

        def __repr__(self):
            return "<Boost>"

    class Fan:
        def __init__(self, coordinates, rotation):
            self.coordinates = coordinates
            self.rotation = rotation

        def __repr__(self):
            return "<Fan>"

    class Jet:
        def __init__(self, coordinates, rotation, sleeping, power, firing_time, acceleration_time, fixed_angle):
            self.coordinates = coordinates
            self.rotation = rotation
            self.sleeping = sleeping
            self.power = power
            self.firing_time = firing_time
            self.acceleration_time = acceleration_time
            self.fixed_angle = fixed_angle

        def __repr__(self):
            return "<Jet>"

    class SpringPlatform:
        def __init__(self, coordinates, rotation, delay):
            self.coordinates = coordinates
            self.rotation = rotation
            self.delay = delay

        def __repr__(self):
            return "<SpringPlatform>"

    class PaddlePlatform:
        def __init__(self, coordinates, rotation, delay, reverse, max_angle, speed):
            self.coordinates = coordinates
            self.rotation = rotation
            self.delay = delay
            self.reverse = reverse
            self.max_angle = max_angle
            self.speed = speed

        def __repr__(self):
            return "<PaddlePlatform>"

class NPC:
    def __init__(self, coordinates, rotation, type, sleeping, reverse, holds_pose, interactive, neck_angle, arm1_angle,
                 arm2_angle, elbow1_angle, elbow2_angle, leg1_angle, leg2_angle, knee1_angle, knee2_angle, releases_joints):
        self.coordinates = coordinates
        self.rotation = rotation
        self.type = type
        self.sleeping = sleeping
        self.reverse = reverse
        self.holds_pose = holds_pose
        self.interactive = interactive
        self.neck_angle = neck_angle
        self.arm1_angle = arm1_angle
        self.arm2_angle = arm2_angle
        self.elbow1_angle = elbow1_angle
        self.elbow2_angle = elbow2_angle
        self.leg1_angle = leg1_angle
        self.leg2_angle = leg2_angle
        self.knee1_angle = knee1_angle
        self.knee2_angle = knee2_angle
        self.releases_joints = releases_joints

        self.character_name = {1: "Wheelchair Guy",
                               2: "Segway Guy",
                               3: "Irresponsible Dad",
                               4: "Effective Shopper",
                               5: "Moped Couple",
                               6: "Lawnmower Man",
                               7: "Explorer Guy",
                               8: "Santa Claus",
                               9: "Pogostick Man",
                               10: "Irresponsible Mom",
                               11: "Helicopter Man"}[self.type]

    def __repr__(self):
        return "<NPC {}>".format(self.character_name)


class Building:
    def __init__(self, coordinates, floor_width, floor_amount, type):
        self.coordinates = coordinates
        self.floor_width = floor_width
        self.floor_amount = floor_amount
        self.type = type

    def __repr__(self):
        return "<Building Type={}>".format(self.type)

class Miscelleneous:
    class BladeWeapon:
        def __init__(self, coordinates, rotation, reverse, sleeping, interactive, type):
            self.coordinates = coordinates
            self.rotation = rotation
            self.reverse = reverse
            self.sleeping = sleeping
            self.interactive = interactive
            self.type = type

        def __repr__(self):
            return "<BladeWeapon Type={}>".format(self.type)

    class FoodItem:
        def __init__(self, coordinates, rotation, sleeping, interactive, type):
            self.coordinates = coordinates
            self.rotation = rotation
            self.sleeping = sleeping
            self.interactive = interactive
            self.type = type

        def __repr__(self):
            return "<FoodItem Type={}>".format(self.type)

    class Chain:
        def __init__(self, coordinates, rotation, sleeping, interactive, link_count, link_scale, chain_curve):
            self.rotation = rotation
            self.sleeping = sleeping
            self.interactive = interactive
            self.link_count = link_count
            self.link_scale = link_scale
            self.chain_curve = chain_curve

        def __repr__(self):
            return "<Chain>"

    class GlassPanel:
        def __init__(self, coordinates, width, height, rotation, sleeping, strength, stabs):
            self.coordinates = coordinates
            self.width = width
            self.height = height
            self.rotation = rotation
            self.sleeping = sleeping
            self.strength = strength
            self.stabs = stabs

        def __repr__(self):
            return "<GlassPanel>"

    class Meteor:
        def __init__(self, coordinates, width, height, fixed, sleeping):
            self.coordinates = coordinates
            self.width = width
            self.height = height
            self.fixed = fixed
            self.sleeping = sleeping

        def __repr__(self):
            return "<Meteor>"

    class DinnerTable:
        def __init__(self, coordinates, rotation, sleeping, interactive):
            self.coordinates = coordinates
            self.rotation = rotation
            self.sleeping = sleeping
            self.interactive = interactive

        def __repr__(self):
            return "<DinnerTable>"

    class Chair:
        def __init__(self, coordinates, rotation, reverse, sleeping, interactive):
            self.coordinates = coordinates
            self.rotation = rotation
            self.reverse = reverse
            self.sleeping = sleeping
            self.interactive = interactive

        def __repr__(self):
            return "<Chair>"

    class Bottle:
        def __init__(self, coordinates, rotation, type, sleeping, interactive):
            self.coordinates = coordinates
            self.rotation = rotation
            self.type = type
            self.sleeping = sleeping
            self.interactive = interactive

        def __repr__(self):
            return "<Bottle Type={}>".format(self.type)

    class Television:
        def __init__(self, coordinates, rotation, sleeping, interactive):
            self.coordinates = coordinates
            self.rotation = rotation
            self.sleeping = sleeping
            self.interactive = interactive

        def __repr__(self):
            return "<Television>"

    class Boombox:
        def __init__(self, coordinates, rotation, sleeping, interactive):
            self.coordinates = coordinates
            self.rotation = rotation
            self.sleeping = sleeping
            self.interactive = interactive

        def __repr__(self):
            return "<Boombox>"

    class SoccerBall:
        def __init__(self, coordinates):
            self.coordinates = coordinates

        def __repr__(self):
            return "<SoccerBall>"

    class Van:
        def __init__(self, coordinates, rotation, sleeping, interactive):
            self.coordinates = coordinates
            self.rotation = rotation
            self.sleeping = sleeping
            self.interactive = interactive

        def __repr__(self):
            return "<Van>"

    class Sign:
        def __init__(self, coordinates, rotation, type, shows_post):
            self.coordinates = coordinates
            self.rotation = rotation
            self.type = type
            self.shows_post = shows_post

        def __repr__(self):
            return "<Sign Type={}>".format(self.type)

    class TrashCan:
        def __init__(self, coordinates, rotation, sleeping, interactive, contains_trash):
            self.coordinates = coordinates
            self.rotation = rotation
            self.sleeping = sleeping
            self.interactive = interactive
            self.contains_trash = contains_trash

        def __repr__(self):
            return "<TrashCan>"

    class Toilet:
        def __init__(self, coordinates, rotation, reverse, sleeping, interactive):
            self.coordinates = coordinates
            self.rotation = rotation
            self.reverse = reverse
            self.sleeping = sleeping
            self.interactive = interactive

        def __repr__(self):
            return "<Toilet>"

    class Token:
        def __init__(self, coordinates, type):
            self.coordinates = coordinates
            self.type = type

        def __repr__(self):
            return "<Token Type={}>".format(self.type)

    class FinishLine:
        def __init__(self, coordinates):
            self.coordinates = coordinates

        def __repr__(self):
            return "<FinishLine>"

class Text:
    def __init__(self, coordinates, rotation, color, font, font_size, alignment, opacity, content):
        self.coordinates = coordinates
        self.rotation = rotation
        self.color = color
        self.font = font
        self.font_size = font_size
        self.alignment = alignment
        self.opacity = opacity
        self.content = content

    def __repr__(self):
        return "<Text Content='{}'>".format(self.content)

class Group:
    def __init__(self, coordinates, rotation, origin_coordinates, sleeping, foreground, opacity, fixed, fixed_angle, items):
        self.coordinates = coordinates
        self.rotation = rotation
        self.origin_coordinates = origin_coordinates
        self.sleeping = sleeping
        self.foreground = foreground
        self.opacity = opacity
        self.fixed = fixed
        self.fixed_angle = fixed_angle
        self.items = items

    def __repr__(self):
        return "<Group>"

class Trigger:
    def __init__(self, coordinates, width, height, rotation, triggered_by, trigger_action, repeat_type, starts_disabled, repeat_interval, delay):
        self.coordinates = coordinates
        self.width = width
        self.height = height
        self.rotation = rotation
        self.triggered_by = triggered_by
        self.trigger_action = trigger_action
        self.repeat_type = repeat_type
        self.starts_disabled
        self.repeat_interval = repeat_interval
        self.delay = delay

    def __repr__(self):
        return "<Trigger>"
