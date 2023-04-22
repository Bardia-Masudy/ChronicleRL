from __future__ import annotations

from typing import TYPE_CHECKING 

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Light(BaseComponent):
    """An entity with this component will emit light onto its parent gamemap's lightmap"""
    parent: Actor

    def __init__(self, radius: int = 1) -> None:
        self.radius = radius
        # print(f"Light instance: {self} - radius: {self.radius}")
        """Lights need to be instantiated, then add themselves when they get spawned with a new entity."""

    @property
    def location(self) -> tuple[int, int]:
        return (self.parent.x, self.parent.y)
    
    def add_location(self):
        self.gamemap.lightmap.lights.add(self)
    
    def push_location(self) -> None:
        self.gamemap.lightmap.add_node(location=self.location, radius=self.radius)
