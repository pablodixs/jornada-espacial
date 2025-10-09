import pygame
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ResourceLoader:
    """Pequeno utilitário para carregar imagens e sons com fallback.

    Uso:
        ResourceLoader.load_image(path, convert_alpha=True)
        ResourceLoader.load_sound(path)
    """

    @staticmethod
    def _resolve(path):
        p = Path(path)
        if not p.exists():
            logger.warning("Resource not found: %s", path)
        return str(p)

    @staticmethod
    def load_image(path, convert_alpha=True):
        p = ResourceLoader._resolve(path)
        try:
            surf = pygame.image.load(p)
            if convert_alpha:
                surf = surf.convert_alpha()
            else:
                surf = surf.convert()
            return surf
        except Exception as e:
            logger.exception("Failed to load image %s: %s", path, e)
            # Criar Surface vazia como fallback
            return pygame.Surface((1, 1), pygame.SRCALPHA)

    @staticmethod
    def load_sound(path):
        p = ResourceLoader._resolve(path)
        try:
            snd = pygame.mixer.Sound(p)
            return snd
        except Exception as e:
            logger.exception("Failed to load sound %s: %s", path, e)
            # Retornar um objeto com métodos compatíveis
            class SilentSound:
                def play(self, *a, **k):
                    return None

                def set_volume(self, *a, **k):
                    return None

            return SilentSound()
