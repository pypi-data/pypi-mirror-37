# -*- coding: utf-8 -*-

import pprint
import copy

from bs4 import BeautifulSoup

from . import models
from . import parse_special
from . import parse_trigger


class parser:
    def __init__(self, xml):
        self.xml = xml

        self.xml_parser = "xml"

        self._polygons = []

    def _prepare(self):
        self.soup = BeautifulSoup(self.xml, self.xml_parser)

    def int_to_tuple(self, rgbint):
        if rgbint == -1:
            return None
        else:
            return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

    def _parse_polygon(self, polygon):
        id = polygon["id"]

        try:
            number_polygons = int(polygon["n"])
            is_original = True
        except KeyError:
            number_polygons = 0
            is_original = False

        if is_original:
            point_list = []
            exists = True
            index = 0
            while exists == True: # TODO: rewrite to `while key in polygon`
                try:
                    point = polygon["v{}".format(index)]

                    if (len(point.split("_")) > 2):
                        # Bezier curve
                        x_point, y_point, dx0, dy0, dx1, dy1 = [float(e) for e in point.split("_")]
                        data_tuple = (x_point, y_point, dx0, dy0, dx1, dy1)
                    else:
                        # Regular polygon
                        try:
                            x_point, y_point = point.split("_")
                        except ValueError as e:
                            # Old XML Support
                            x_point, y_point = point.split(".")

                        data_tuple = (float(x_point), float(y_point))

                    point_list.append(data_tuple)

                    index += 1
                except KeyError:
                    exists = False
        else:
            point_list = []

        parsed_polygon = models.Polygon(id, number_polygons, point_list, is_original)

        self._polygons.append(parsed_polygon)
        return parsed_polygon

    def _parse_shape(self, shape):
        type = int(shape["t"])
        interactive = False

        shape_coordinates = (float(shape["p0"]), float(shape["p1"]))

        width = float(shape["p2"])
        height = float(shape["p3"])

        rotation = float(shape["p4"])
        fixed = shape["p5"] == "t"
        sleeping = shape["p6"] == "t"
        density = float(shape["p7"])
        fill_color = self.int_to_tuple(int(shape["p8"]))
        outline_color = self.int_to_tuple(int(shape["p9"]))
        opacity = float(shape["p10"])
        collision = int(shape["p11"])

        if type == 1:
            cutout = int(shape["p12"])
        else:
            cutout = None

        if shape.v:
            polygon = self._parse_polygon(shape.v)
        else:
            polygon = None

        parsed_shape = models.Shape(shape_coordinates,
                                    type, 
                                    interactive, 
                                    width, 
                                    height, 
                                    rotation, 
                                    fixed, 
                                    sleeping, 
                                    density, 
                                    fill_color, 
                                    outline_color, 
                                    opacity, 
                                    collision, 
                                    cutout=cutout,
                                    polygon=polygon)

        return parsed_shape

    def _parse_joint(self, joint):
        type = joint["t"]
        coordinates = (float(joint["x"]), float(joint["y"]))

        first_connection = joint["b1"]
        second_connection = joint["b2"]

        if "a" in joint:
            axis_angle = int(joint["a"])
        else:
            axis_angle = None

        limit_enabled = joint["l"] == "t"
        try:
            upper_angle = int(joint["ua"])
        except KeyError:
            upper_angle = None

        try:
            lower_angle = int(joint["la"])
        except KeyError:
            lower_angle = None

        try:
            upper_limit = int(joint["ul"])
        except KeyError:
            upper_limit = None

        try:
            lower_limit = int(joint["ll"])
        except KeyError:
            lower_limit = None

        motor_enabled = joint["m"] == "t"
        try:
            motor_torque = float(joint["tq"])
        except KeyError:
            motor_torque = None

        try:
            motor_force = float(joint["fo"])
        except KeyError:
            motor_force = None

        try:
            motor_speed = float(joint["sp"])
        except KeyError:
            motor_speed = None

        collide_connected = joint["c"] == "t"

        parsed_joint = models.Joint(coordinates, 
                                    type,
                                    first_connection,
                                    second_connection,
                                    collide_connected,
                                    axis_angle=axis_angle,
                                    upper_angle=upper_angle,
                                    lower_angle=lower_angle,
                                    upper_limit=upper_limit,
                                    lower_limit=lower_limit,
                                    motor_torque=motor_torque,
                                    motor_force=motor_force,
                                    motor_speed=motor_speed)

        return parsed_joint

    def _parse_group(self, group):
        coordinates = (float(group["x"]), float(group["y"]))
        rotation = float(group["r"])
        origin_coordinates = (float(group["ox"]), float(group["oy"]))
        sleeping = group["s"] == "t"
        foreground = group["f"] == "t"

        try:
            opacity = int(group["o"])
        except KeyError:
            opacity = 100

        try:
            fixed = group["im"] == "t"
        except KeyError:
            fixed = False

        try:
            fixed_angle = group["fr"] == "t"
        except KeyError:
            fixed_angle = False

        parsed_items = []
        for item in group.find_all(recursive=False):
            if item.name == "sh":
                parsed_shape = self._parse_shape(item)
                parsed_items.append(parsed_shape)

            if item.name == "j":
                parsed_joint = self._parse_joint(item)
                parsed_items.append(parsed_joint)

            if item.name == "sp":
                parsed_item = parse_special.parse_special(item)
                parsed_items.append(parsed_item)

        parsed_group = models.Group(coordinates, rotation, origin_coordinates, sleeping, foreground, opacity, fixed, fixed_angle, parsed_items)
        return parsed_group

    def parse(self):
        self._prepare()

        # LEVEL XML
        version = float(self.soup.info["v"])

        # CHARACTER
        character_type = int(self.soup.info["c"])
        character_forced = self.soup.info["f"] == "t"
        character_coordinates = (float(self.soup.info["x"]), float(self.soup.info["y"]))

        try:
            character_vehicle_hidden = self.soup.info["h"] == "t"
        except KeyError:
            character_vehicle_hidden = True

        character = models.Character(character_coordinates, character_type, character_forced, character_vehicle_hidden)

        # BACKGROUND
        background_type = int(self.soup.info["bg"])
        background_color = self.int_to_tuple(int(self.soup.info["bgc"]))

        background = models.Background(background_type, background_color)

        # SHAPES
        shapes = []
        if self.soup.shapes:
            for shape in self.soup.shapes.find_all("sh", recursive=False):
                parsed_shape = self._parse_shape(shape)
                shapes.append(parsed_shape)

        # Patch polygons
        patched_shapes = []
        for shape in shapes:
            if (shape.polygon and not shape.polygon.original):
                potential_originals = [polygon for polygon in self._polygons if polygon.id == shape.polygon.id]
                original = [polygon for polygon in potential_originals if polygon.points != []][0]

                shape.polygon.points = original.points
                patched_shapes.append(shape)
            else:
                patched_shapes.append(shape)

        shapes = patched_shapes

        # JOINTS
        joints = []
        if self.soup.joints:
            for joint in self.soup.joints.find_all("j", recursive=False):
                parsed_joint = self._parse_joint(joint)
                joints.append(parsed_joint)

        # SPECIAL ITEMS
        special_items = []
        if self.soup.specials:
            for item in self.soup.specials.find_all("sp", recursive=False):
                parsed_item = parse_special.parse_special(item)
                special_items.append(parsed_item)

        # TRIGGERS
        triggers = []
        if self.soup.triggers:
            for trigger in self.soup.triggers.find_all("t", recursive=False):
                parsed_trigger = parse_trigger.parse_trigger(trigger)
                triggers.append(parsed_trigger)

        # GROUPS
        groups = []
        if self.soup.groups:
            for group in self.soup.groups.find_all("g", recursive=False):
                parsed_group = self._parse_group(group) 
                groups.append(parsed_group)

        patched_groups = []
        for group in groups:
            group_copy = copy.deepcopy(group)

            index = 0
            for item in group.items:
                if type(item) == models.Shape:
                    if (item.polygon and not item.polygon.original):
                        potential_originals = [polygon for polygon in self._polygons if polygon.id == item.polygon.id]
                        original = [polygon for polygon in potential_originals if polygon.points != []][0]

                        group_copy.items[index].polygon.points = original.points

                index += 1

            patched_groups.append(group_copy)

        groups = patched_groups

        final_xml = models.XML(self.xml, version, character, background, shapes, joints, special_items, triggers, groups)
        return final_xml

