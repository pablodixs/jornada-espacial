import logging
import pygame
from core.resource_loader import ResourceLoader

logger = logging.getLogger(__name__)


class SoundManager:
    _mixer_available = False

    @staticmethod
    def init():
        try:
            pygame.mixer.init()
            SoundManager._mixer_available = True
        except Exception as e:
            SoundManager._mixer_available = False
            logger.exception("pygame.mixer initialization failed: %s", e)

    @staticmethod
    def play_soundtrack(url, loop=-1, volume=0.5):
        if not SoundManager._mixer_available:
            logger.warning("Mixer not available, cannot play soundtrack: %s", url)
            return
        try:
            pygame.mixer.music.load(url)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop)
        except Exception:
            logger.exception("Failed to play soundtrack: %s", url)

    @staticmethod
    def stop_music():
        if not SoundManager._mixer_available:
            return
        try:
            pygame.mixer.music.stop()
        except Exception:
            logger.exception("Failed to stop music")

    @staticmethod
    def load_sound(path):
        # utilitário que retorna um objeto som (pode ser silencioso)
        if not SoundManager._mixer_available:
            logger.debug("Mixer not available, returning silent sound for %s", path)
            return ResourceLoader.load_sound(path)  # ResourceLoader já devolve SilentSound quando falha
        try:
            return ResourceLoader.load_sound(path)
        except Exception:
            logger.exception("Failed to load sound via ResourceLoader: %s", path)
            return ResourceLoader.load_sound(path)