from typing import Optional, Dict, List

import pyglet
from pyglet.graphics import Batch
from pyglet.gui import Frame
from pyglet.sprite import Sprite
from pyglet.window import Window

from .grid import Grid
from .gui_elements import ToggleButton, TextEntry, Slider


class ImageWindow(Window):
    def __init__(self, image_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprite: Sprite = self._load_sprite(image_path)
        self.sprite_dx: int = 0
        self.sprite_dy: int = 0
        self._recalculate_sprite_size()
        self.batch = Batch()
        self.grid: Optional[Grid] = None

    def on_draw(self):
        self.clear()
        self.sprite.draw()
        self.batch.draw()

    def on_resize(self, width: int, height: int):
        super().on_resize(width=width, height=height)
        print('resize image window', (width, height))
        if self.grid is not None:
            self.grid.update_screen_px(width_px=width, height_px=height)

    @staticmethod
    def _load_sprite(image_path: str) -> Sprite:
        image = pyglet.image.load(image_path)
        return Sprite(image)

    def _recalculate_sprite_size(self):
        self.sprite.x = (self.width - self.sprite.width) / 2 + self.sprite_dx
        self.sprite.y = (self.height - self.sprite.height) / 2 + self.sprite_dy

    def add_grid(self, width_mm: int, height_mm: int):
        width_px, height_px = self.get_framebuffer_size()
        self.grid = Grid(
            width_px=width_px,
            height_px=height_px,
            width_mm=width_mm,
            height_mm=height_mm,
            batch=self.batch,
        )

    def remove_grid(self):
        if self.grid is not None:
            self.grid.delete()
            self.grid = None

    def image_scale(self, value: float):
        self.sprite.scale = value
        self._recalculate_sprite_size()

    def image_pan_x(self, value: float):
        self.sprite_dx = int(value)
        self._recalculate_sprite_size()

    def image_pan_y(self, value: float):
        self.sprite_dy = int(value)
        self._recalculate_sprite_size()

    def image_change(self, image_path: str):
        print('change image to', image_path)
        self.sprite.delete()
        self.sprite = self._load_sprite(image_path)
        self._recalculate_sprite_size()


class GMWindow(Window):
    def __init__(self, image_window: ImageWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_window = image_window
        self.batch = Batch()
        self.frame = Frame(window=self)
        self.text_entries: Dict[str, TextEntry] = {
            'screen_width': TextEntry(
                x=0,
                y=300,
                width=200,
                batch=self.batch,
            ),
            'screen_height': TextEntry(
                x=250,
                y=300,
                width=200,
                batch=self.batch,
            )
        }
        for widget in self.text_entries.values():
            self.frame.add_widget(widget)

        def button_callback_grid(button_value: bool) -> bool:
            if button_value:
                try:
                    width_mm = int(self.text_entries['screen_width'].value)
                    height_mm = int(self.text_entries['screen_height'].value)
                except ValueError:
                    print('Invalid input for screen size')
                    return False
                else:
                    self.image_window.add_grid(
                        width_mm=width_mm,
                        height_mm=height_mm,
                    )
                    return True
            else:
                self.image_window.remove_grid()
                return False

        self.button = ToggleButton(
            x=500,
            y=300,
            batch=self.batch,
            callback=button_callback_grid,
        )
        self.frame.add_widget(self.button)

        self.slider_scale = Slider(
            x=0,
            y=200,
            value_min=0.1,
            value_max=4,
            default=1,
            batch=self.batch,
            callback=image_window.image_scale,
        )
        self.frame.add_widget(self.slider_scale)
        self.slider_pan_x = Slider(
            x=0,
            y=100,
            value_min=-image_window.width,
            value_max=image_window.width,
            default=0,
            batch=self.batch,
            callback=image_window.image_pan_x,
        )
        self.frame.add_widget(self.slider_pan_x)
        self.slider_pan_y = Slider(
            x=0,
            y=0,
            value_min=-image_window.height,
            value_max=image_window.height,
            default=0,
            batch=self.batch,
            callback=image_window.image_pan_y,
        )
        self.frame.add_widget(self.slider_pan_y)

    def on_draw(self):
        self.batch.draw()

    def on_file_drop(self, x: int, y: int, paths: List[str]):
        self.image_window.image_change(paths[0])
        self.slider_scale.value = self.slider_scale.default_value
        self.slider_pan_x.value = self.slider_pan_x.default_value
        self.slider_pan_y.value = self.slider_pan_y.default_value
