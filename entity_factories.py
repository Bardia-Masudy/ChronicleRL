from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.light import Light
from entity import Actor, Item

# entity = Entity(char="CHAR", colour=(R, G, B), name="STRING", blocks_movement=bool)

player = Actor(
    char="@", 
    colour=(255, 255, 255), 
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity = 26),
    level=Level(level_up_base=200),
    light=Light(radius=8)
    )

orc = Actor(
    char="O", 
    colour=(63, 127, 63), 
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity = 0),
    level=Level(xp_given=100),
    light=Light(radius=4)
    )

goblin = Actor(
    char="g", 
    colour=(0, 127, 0), 
    name="Goblin",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity = 0),
    level=Level(xp_given=35),
    light=Light(radius=0)
    )

health_potion = Item(
    char="!",
    colour=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4)
)

lighting_scroll = Item(
    char = "~",
    colour = (255, 255, 0),
    name = "Lightning Scroll",
    consumable = consumable.LightningDamageConsumable(damage=20, max_range=5)
)

confusion_scroll = Item(
    char="~",
    colour=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(duration=10)
)

fireball_scroll = Item(
    char="~",
    colour=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3)
)