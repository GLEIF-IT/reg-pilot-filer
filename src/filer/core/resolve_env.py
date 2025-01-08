import os
from dataclasses import dataclass, field
from typing import List, Tuple

from keri.app import configing


@dataclass(frozen=True)
class FilerEnvironment:
    configuration: configing.Configer = None
    mode: str = "production"
    verifier_base_url: str = "localhost:7676"
    admin_role_name: str = "EBA Data Admin"
    admin_lei: str = ""


    _instance: "FilerEnvironment" = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FilerEnvironment, cls).__new__(cls)
            object.__setattr__(cls._instance, '_initialized', False)
        return cls._instance

    def __post_init__(self):
        if getattr(self, '_initialized', False):
            raise RuntimeError("FilerEnvironment is a singleton and cannot be re-initialized.")
        object.__setattr__(self, '_initialized', True)

    @classmethod
    def initialize(cls, **kwargs):
        """
        Initialize the singleton instance with custom arguments. Can only be called once.
        """
        if cls._instance is None:
            instance = cls(**kwargs)
            cls._instance = instance
            return instance
        else:
            return cls._instance

    @classmethod
    def resolve_env(cls):
        """
        Get the existing instance of FilerEnvironment. If not initialized, create with defaults.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
