import pygame
import numpy as np
import wave


class MusicVisualizer:
    def __init__(self, song_path, color_base=(100, 100, 255)):
        """
        Initializes the MusicVisualizer with the given song path.

        :param song_path: Path to the song file (.wav needed for feature extraction).
        :param color_base: Base RGB values for the visualizer's colors.
        """
        self.color_base = color_base
        self.song_path = song_path

        # Fallback: Variable for simulated music progression
        self.start_ticks = pygame.time.get_ticks()
        self.duration = self.get_song_duration(song_path)  # Approximate song duration in ms

        # Preprocess song features (assuming .wav format for raw audio data)
        self.amplitude_data = self.preprocess_audio(song_path)

        # Visualization parameters
        self.bar_count = 64  # Number of bars in the waveform
        self.color = (0, 128, 255)  # Default color for waveform
        self.amplitude = 150  # Maximum amplitude of the waveform

    def get_song_duration(self, song_path):
        """
        Fallback for retrieving song duration from pygame mixer.
        Pygame mixer doesn't support detailed song information, so estimates must be used from external tools.

        :param song_path: Path to the song file.
        :return: Duration in milliseconds or default to 3 minutes.
        """
        try:
            return int(pygame.mixer.Sound(song_path).get_length() * 1000)  # seconds to ms
        except Exception as e:
            print(f"Warning: Could not retrieve song duration ({e}). Defaulting to 3 minutes.")
            return 180000  # Default to 3 minutes = 180,000 ms

    def preprocess_audio(self, song_path):
        """
        Extracts amplitude (RMS) values from the song for visualization.

        :param song_path: Path to the .wav audio file.
        :return: List of amplitude values normalized to the 0-255 range.
        """
        try:
            # Open the song as a .wav file
            with wave.open(song_path, "r") as wav_file:
                # Get audio parameters
                n_frames = wav_file.getnframes()
                framerate = wav_file.getframerate()
                duration = n_frames / float(framerate)

                # Read frames and convert to numpy array
                raw_audio = np.frombuffer(wav_file.readframes(n_frames), dtype=np.int16)

                # Compute RMS over small chunks
                chunk_size = framerate // 20  # 50ms chunks
                amplitude_data = [
                    np.sqrt(np.mean(raw_audio[i: i + chunk_size] ** 2))
                    for i in range(0, len(raw_audio), chunk_size)
                ]

                # Normalize amplitude values to range 0-255
                max_amplitude = max(amplitude_data) if amplitude_data else 1
                amplitude_data = [
                    int((amplitude / max_amplitude) * 255) for amplitude in amplitude_data
                ]

                return amplitude_data
        except Exception as e:
            print(f"Error during audio preprocessing: {e}")
            return []

    def calculate_amplitude(self):
        """
        Simulates amplitude values over time. Replace this logic with audio data when available.

        :return: Normalized amplitude value (0-255).
        """
        current_time = pygame.time.get_ticks() - self.start_ticks  # Time since music started (ms)

        # Simulate amplitude progression (e.g., oscillating effect based on time)
        if current_time < self.duration:
            amplitude = abs(np.sin(current_time * 0.005)) * 255
        else:
            amplitude = 0  # If time exceeds duration, amplitude drops to 0

        return int(amplitude)

    def get_visual_color(self):
        """
        Returns a color tuple based on the calculated amplitude.

        :return: (R, G, B) color tuple.
        """
        amplitude = self.calculate_amplitude()
        color = (
            amplitude,              # Amplitude affects red intensity
            self.color_base[1],     # Base green intensity stays static
            255 - amplitude         # Complementary blue
        )
        return color

    def get_frequency_bars(self):
        """
        Returns a frequency spectrum for visualization based on FFT.
        """
        # Take a chunk of the waveform
        chunk = np.random.randint(-32768, 32767, size=1024)

        # Apply FFT to chunk
        fourier = np.fft.fft(chunk)
        magnitude = np.abs(fourier[:len(fourier) // 2])  # Take positive frequencies only
        magnitudes = magnitude[:self.bar_count]  # Limit to bar_count

        # Scale magnitudes for visualization
        scaled = (magnitudes / np.max(magnitudes)) * self.amplitude if np.max(magnitudes) > 0 else magnitudes
        return scaled

    def draw_waveform(self, screen, width, height):
        """
        Draws a waveform visualization on the screen.
        """
        bar_width = width // self.bar_count
        frequencies = self.get_frequency_bars()

        for i, freq in enumerate(frequencies):
            x = i * bar_width
            bar_height = freq
            bar_rect = pygame.Rect(x, height // 2 - bar_height // 2, bar_width - 2, bar_height)
            pygame.draw.rect(screen, self.color, bar_rect)

    def draw_ripples(self, screen, width, height):
        frequencies = self.get_frequency_bars()
        center_x, center_y = width // 2, height // 2

        for i, freq in enumerate(frequencies):
            radius = int(freq)  # Circle radius based on frequency magnitude
            color = (i * 4 % 255, 128, 255 - i * 4 % 255)  # Slightly dynamic colors
            pygame.draw.circle(screen, color, (center_x, center_y), radius, 2)  # Draw circles

    def draw_spiral(self, screen, width, height, angle_offset):
        frequencies = self.get_frequency_bars()
        center_x, center_y = width // 2, height // 2

        for i, freq in enumerate(frequencies):
            angle = i * (360 / len(frequencies)) + angle_offset
            radius = int(freq) * 3
            x = int(center_x + radius * np.cos(np.radians(angle)))
            y = int(center_y + radius * np.sin(np.radians(angle)))
            color = (255 - i * 4 % 255, i * 8 % 255, 128)  # Color dynamic
            pygame.draw.circle(screen, color, (x, y), 4)  # Small circle at each point

    def draw_radial_bars(self, screen, width, height):
        frequencies = self.get_frequency_bars()
        center_x, center_y = width // 2, height // 2
        num_bars = len(frequencies)
        angle_step = 360 / num_bars

        for i, freq in enumerate(frequencies):
            length = int(freq) * 4
            angle = i * angle_step
            end_x = int(center_x + length * np.cos(np.radians(angle)))
            end_y = int(center_y + length * np.sin(np.radians(angle)))

            color = (255, i * 4 % 255, i * 8 % 255)  # Dynamic color
            pygame.draw.line(screen, color, (center_x, center_y), (end_x, end_y), 2)  # Thin bars

    def draw_wave_grid(self, screen, width, height, frame_count):
        frequencies = self.get_frequency_bars()
        rows, cols = 10, 10  # Adjust rows and columns for resolution
        grid_width, grid_height = width // cols, height // rows

        for row in range(rows):
            for col in range(cols):
                x = col * grid_width + grid_width // 2
                y = row * grid_height + grid_height // 2
                freq = frequencies[(row * cols + col) % len(frequencies)]
                offset = int(50 * np.sin(frame_count / 10.0 + freq / 10.0))  # Oscillation
                pygame.draw.circle(screen, (255 - freq % 255, 128, freq % 255), (x, y + offset), 5)


