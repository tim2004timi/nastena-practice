import customtkinter as ctk
from typing import Tuple


class Colors:
    """Цветовая палитра в HSL формате, конвертированная в RGB"""
    
    BACKGROUND = "#0A0514"
    BACKGROUND_GRADIENT_END = "#080410"
    FOREGROUND = "#F2EFF5"
    CARD = "#1A0F2E"
    CARD_GRADIENT_END = "#1F1538"
    PRIMARY = "#9D4EDD"
    SECONDARY = "#2A1F3D"
    MUTED_FOREGROUND = "#9995A0"
    BORDER = "#3A2F4D"
    INPUT = "#3A2F4D"
    RING = "#9D4EDD"
    
    GRADE_5 = "#7DD87D"
    GRADE_4 = "#2E7D32"
    GRADE_3 = "#F57C00"
    GRADE_2 = "#EF5350"
    GRADE_ABSENT = "#8B6F47"
    GRADE_EMPTY = "#4A4255"
    SUCCESS_GLOW = "#2E7D32"
    DESTRUCTIVE = "#EF5350"
    PRIMARY_LIGHT = "#27263C"


class Typography:
    """Типографика"""
    TITLE = ("Arial", 24, "bold")
    CARD_TITLE = ("Arial", 20, "bold")
    BASE = ("Arial", 16, "normal")
    SMALL = ("Arial", 14, "normal")
    XSMALL = ("Arial", 12, "normal")
    STATS = ("Arial", 30, "bold")


class Spacing:
    """Отступы и размеры"""
    SCREEN_PADDING = 24
    CARD_PADDING = 20
    ELEMENT_SPACING = 16
    SMALL_SPACING = 12
    FOOTER_HEIGHT = 64
    BUTTON_HEIGHT = 48
    INPUT_HEIGHT = 48
    TOUCH_TARGET = 48


class BorderRadius:
    """Радиусы скругления"""
    STANDARD = 16
    MEDIUM = 14
    SMALL = 12
    CARD = 16
    BUTTON = 8
    BADGE = 8
    CIRCLE = 50


class DesignSystem:
    """Основной класс дизайн-системы"""
    
    @staticmethod
    def setup_theme():
        """Настроить тему CustomTkinter"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    @staticmethod
    def get_grade_color(grade) -> str:
        """Получить цвет для оценки"""
        from models import Grade
        if grade == Grade.FIVE:
            return Colors.GRADE_5
        elif grade == Grade.FOUR:
            return Colors.GRADE_4
        elif grade == Grade.THREE:
            return Colors.GRADE_3
        elif grade == Grade.TWO:
            return Colors.GRADE_2
        elif grade == Grade.ABSENT:
            return Colors.GRADE_ABSENT
        else:
            return Colors.GRADE_EMPTY
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Конвертировать HEX в RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Конвертировать RGB в HEX"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    @staticmethod
    def blend_colors(color1: str, color2: str, ratio: float = 0.5) -> str:
        """Смешать два цвета (ratio: 0.0 = color1, 1.0 = color2)"""
        rgb1 = DesignSystem.hex_to_rgb(color1)
        rgb2 = DesignSystem.hex_to_rgb(color2)
        
        blended = tuple(
            int(rgb1[i] * (1 - ratio) + rgb2[i] * ratio)
            for i in range(3)
        )
        return DesignSystem.rgb_to_hex(blended)
    
    @staticmethod
    def with_opacity(color: str, opacity: float, background: str = None) -> str:
        """Создать цвет с прозрачностью путем смешивания с фоном"""
        if background is None:
            background = Colors.BACKGROUND
        return DesignSystem.blend_colors(background, color, opacity)

