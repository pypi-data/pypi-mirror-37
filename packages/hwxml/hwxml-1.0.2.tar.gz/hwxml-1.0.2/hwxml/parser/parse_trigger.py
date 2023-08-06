# -*- coding: utf-8 -*-

from . import models

def parse_trigger(trigger):
    coordinates = (float(trigger["x"]), float(trigger["y"]))
    width = int(trigger["w"])
    height = int(trigger["h"])
    rotation = float(trigger["a"])

    triggered_by = int(trigger["b"])
    trigger_action_id = int(trigger["t"])
    repeat_type = int(trigger["r"])
    starts_disabled = trigger["sd"] == "t"

    if repeat_type in [3, 4]:
        repeat_interval = float(trigger["i"])
    else:
        repeat_interval = None

    if trigger_action_id in [1, 2]:
        delay = float(trigger["d"])
    else:
        delay = 0

    if trigger_action_id == 1:
        # Trigger action
        action_action = int(trigger["a"])

        trigger_action = models.TriggerAction.Interaction(action_action)

    if trigger_action_id == 2:
        # Plays sound
        sound_id = int(trigger["s"])
        sound_location = float(trigger["l"])
        sound_panning = float(trigger["p"])
        sound_volume = float(trigger["v"])

        trigger_action = models.TriggerAction.SoundEffect(sound_id, sound_location, sound_panning, sound_volume)

    if trigger_action_id == 3:
        trigger_action = models.TriggerAction.Victory()

    parsed_trigger = models.Trigger(coordinates, 
                                    width, 
                                    height, 
                                    rotation, 
                                    triggered_by, 
                                    trigger_action_id, 
                                    repeat_type, 
                                    starts_disabled, 
                                    repeat_interval, 
                                    delay, 
                                    trigger_action)

    return parsed_trigger

