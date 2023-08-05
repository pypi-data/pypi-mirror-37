from ribosome.data.plugin_state import PluginState

from proteome.data.env import Env
from proteome.config.component import ProteomeComponent

ProteomeState = PluginState[Env, ProteomeComponent]

__all__ = ('ProteomeState',)
