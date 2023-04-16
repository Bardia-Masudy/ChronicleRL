from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import colour
import components.inventory
import components.ai
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import (
    ActionOrHandler,
    AreaRangedAttackHandler, 
    SingleRangedAttackHandler,
)

if TYPE_CHECKING:
    from entity import Actor, Item

class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """Invoke this items ability.
        'action' is the context for this activiation."""
        raise NotImplementedError()
    
    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)

class ConfusionConsumable(Consumable):
    def __init__(self, duration: int) -> None:
        self.duration = duration

    def get_action(self, consumer: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", colour.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy)
        )
    
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You cannot target an area you cannot see.")
        if not target:
            raise Impossible("You must select an enemy to target.")
        if target is consumer:
            raise Impossible("You cannot confuse yourself!") #TODO: make this possible, add confusion player status
        
        self.engine.message_log.add_message(
            f"The {target.name}'s stare grows vacant, as it starts stumbling around!",
            colour.status_effect_applied
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai, duration=self.duration
        )
        self.consume()

class FireballDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> AreaRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", colour.needs_target
        )
        return AreaRangedAttackHandler(
            self.engine,
            radius= self.radius,
            callback= lambda xy: actions.ItemAction(consumer, self.parent, xy)
        )
    
    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")
        
        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"The {actor.name} is engulfed in the firey explosion, taking {self.damage} damage!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True
        
        if not targets_hit:
            raise Impossible("There are no targets in the radius.") # TODO: change this to a better message, maybe a confirmation ask.
        self.consume()

class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount
    
    def activate(self, action: actions.ItemActions) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                colour.health_recovered
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")
    
class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, max_range: int):
        self.damage = damage
        self.max_range = max_range
    
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.max_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(f"A bolt of lightning strikes the {target.name} with a roar of thunder, dealing {self.damage} damage!")
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("Lightning crackles in the air, but there's no valid target close enough.")