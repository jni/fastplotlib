from typing import *

from pygfx import WorldObject
from pygfx.linalg import Vector3

from .features import GraphicFeature, PresentFeature


class BaseGraphic:
    def __init_subclass__(cls, **kwargs):
        """set the type of the graphic in lower case like "image", "line_collection", etc."""
        cls.type = cls.__name__.lower().replace("graphic", "").replace("collection", "_collection")
        super().__init_subclass__(**kwargs)


class Graphic(BaseGraphic):
    def __init__(
            self,
            name: str = None
    ):
        """

        Parameters
        ----------
        name: str, optional
            name this graphic, makes it indexable within plots

        """

        self.name = name
        self.present = PresentFeature(parent=self)

        valid_features = ["visible"]
        for attr_name in self.__dict__.keys():
            attr = getattr(self, attr_name)
            if isinstance(attr, GraphicFeature):
                valid_features.append(attr_name)

        self._valid_features = tuple(valid_features)

    @property
    def world_object(self) -> WorldObject:
        return self._world_object

    @property
    def position(self) -> Vector3:
        """The position of the graphic"""
        return self.world_object.position

    @property
    def interact_features(self) -> Tuple[str]:
        """The features for this ``Graphic`` that support interaction."""
        return self._valid_features

    @property
    def visible(self) -> bool:
        return self.world_object.visible

    @visible.setter
    def visible(self, v):
        """Toggle the visibility of this Graphic"""
        self.world_object.visible = v

    @property
    def children(self) -> WorldObject:
        return self.world_object.children

    def __setattr__(self, key, value):
        if hasattr(self, key):
            attr = getattr(self, key)
            if isinstance(attr, GraphicFeature):
                attr._set(value)
                return

        super().__setattr__(key, value)

    def __repr__(self):
        if self.name is not None:
            return f"'{self.name}' fastplotlib.{self.__class__.__name__} @ {hex(id(self))}"
        else:
            return f"fastplotlib.{self.__class__.__name__} @ {hex(id(self))}"