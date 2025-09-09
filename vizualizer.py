import pygame
import numpy as np

class MusicVisualizer:
    def __init__(self, color_base=(100, 100, 255)):
        self.color_base = color_base

    def calculate_amplitude(self):
        """
        Simulates an amplitude value. Replace this with actual audio signal processing.
        """
        amplitude = (abs(np.sin(pygame.time.get_ticks() * 0.005)) ** 0.5) * 255
        return amplitude

    def get_visual_color(self):
        """
        Returns a color tuple based on the calculated amplitude.
        """
        amplitude = self.calculate_amplitude()
        color = (
            int(amplitude),
            self.color_base[1],  # Keep base green unchanged
            int(255 - amplitude)
        )
        return color