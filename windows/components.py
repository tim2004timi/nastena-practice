import customtkinter as ctk
from typing import Optional, Callable
from models import Grade
from design_system import Colors, Typography, Spacing, BorderRadius, DesignSystem


class GradeBadge(ctk.CTkButton):
    """Бейдж оценки"""
    
    def __init__(self, parent, grade: Optional[Grade] = None, 
                 command: Optional[Callable] = None, width=40, height=40):
        self.grade = grade
        if grade and grade != Grade.EMPTY:
            text = str(grade)
        else:
            text = "—"
        color = DesignSystem.get_grade_color(grade) if grade else Colors.GRADE_EMPTY
        
        super().__init__(
            parent,
            text=text,
            width=width,
            height=height,
            corner_radius=BorderRadius.BADGE,
            fg_color=color,
            text_color="white" if grade and grade != Grade.EMPTY else Colors.FOREGROUND,
            font=Typography.SMALL,
            command=command,
            hover_color=self._darken_color(color)
        )
    
    def _darken_color(self, color: str) -> str:
        """Затемнить цвет для hover эффекта"""
        rgb = DesignSystem.hex_to_rgb(color)
        return DesignSystem.rgb_to_hex((
            max(0, rgb[0] - 20),
            max(0, rgb[1] - 20),
            max(0, rgb[2] - 20)
        ))
    
    def set_grade(self, grade: Optional[Grade]):
        """Обновить оценку"""
        self.grade = grade
        text = str(grade) if grade else "—"
        color = DesignSystem.get_grade_color(grade) if grade else Colors.GRADE_EMPTY
        self.configure(
            text=text,
            fg_color=color,
            hover_color=self._darken_color(color)
        )


class GradeSelectorDialog(ctk.CTkToplevel):
    """Диалог выбора оценки"""
    
    def __init__(self, parent, on_select: Callable[[Optional[Grade]], None]):
        super().__init__(parent)
        self.on_select = on_select
        self.selected_grade: Optional[Grade] = None
        
        self.title("Выберите оценку")
        self.geometry("400x280")
        self.configure(fg_color=Colors.BACKGROUND)
        
        title_label = ctk.CTkLabel(
            self,
            text="Выберите оценку",
            font=Typography.CARD_TITLE,
            text_color=Colors.FOREGROUND
        )
        title_label.pack(pady=Spacing.ELEMENT_SPACING)
        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=Spacing.ELEMENT_SPACING, padx=Spacing.SCREEN_PADDING)
        
        grades = [
            (Grade.FIVE, "5"),
            (Grade.FOUR, "4"),
            (Grade.THREE, "3"),
            (Grade.TWO, "2"),
            (Grade.ABSENT, "н"),
            (Grade.EMPTY, "Очистить")
        ]
        
        for i, (grade, text) in enumerate(grades):
            row = i // 3
            col = i % 3
            
            color = DesignSystem.get_grade_color(grade)
            
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                width=100,
                height=70,
                corner_radius=BorderRadius.BUTTON,
                fg_color=color,
                text_color="white" if grade and grade != Grade.EMPTY else Colors.FOREGROUND,
                font=Typography.CARD_TITLE,
                command=lambda g=grade: self._select_grade(g)
            )
            btn.grid(row=row, column=col, padx=8, pady=8)
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.grab_set()
        self.focus()
    
    def _select_grade(self, grade: Grade):
        """Выбрать оценку"""
        self.selected_grade = grade if grade != Grade.EMPTY else None
        self.on_select(None if grade == Grade.EMPTY else grade)
        self.destroy()


class FooterNav(ctk.CTkFrame):
    """Футер-навигация"""
    
    def __init__(self, parent, on_navigate: Callable[[str], None], current_route: str = "/"):
        super().__init__(parent, fg_color=Colors.CARD, corner_radius=0, height=Spacing.FOOTER_HEIGHT)
        self.on_navigate = on_navigate
        self.current_route = current_route
        
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=Spacing.SCREEN_PADDING, pady=8)
        
        nav_items = [
            ("/", "Профиль", "👤"),
            ("/students", "Студенты", "👥"),
            ("/groups", "Группы", "📁")
        ]
        
        for route, label, icon in nav_items:
            is_active = route == current_route
            
            btn = ctk.CTkButton(
                nav_frame,
                text=f"{icon}\n{label}",
                width=100,
                height=Spacing.FOOTER_HEIGHT - 16,
                corner_radius=BorderRadius.BUTTON,
                fg_color=Colors.PRIMARY if is_active else "transparent",
                text_color=Colors.FOREGROUND if is_active else Colors.MUTED_FOREGROUND,
                font=Typography.XSMALL,
                command=lambda r=route: self._navigate(r),
                hover_color=Colors.PRIMARY if not is_active else None
            )
            btn.pack(side="left", expand=True, fill="both", padx=4)
    
    def _navigate(self, route: str):
        """Перейти на маршрут"""
        self.on_navigate(route)
    
    def set_active_route(self, route: str):
        """Установить активный маршрут"""
        self.current_route = route
        for widget in self.winfo_children():
            widget.destroy()
        self.__init__(self.master, self.on_navigate, route)


class Card(ctk.CTkFrame):
    """Карточка с градиентом"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=Colors.CARD,
            corner_radius=BorderRadius.CARD,
            **kwargs
        )


class PrimaryButton(ctk.CTkButton):
    """Основная кнопка"""
    
    def __init__(self, parent, text: str, command: Optional[Callable] = None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=Colors.PRIMARY,
            text_color="white",
            height=Spacing.BUTTON_HEIGHT,
            corner_radius=BorderRadius.BUTTON,
            font=Typography.BASE,
            hover_color=self._darken_color(Colors.PRIMARY),
            **kwargs
        )
    
    def _darken_color(self, color: str) -> str:
        """Затемнить цвет"""
        rgb = DesignSystem.hex_to_rgb(color)
        return DesignSystem.rgb_to_hex((
            max(0, rgb[0] - 20),
            max(0, rgb[1] - 20),
            max(0, rgb[2] - 20)
        ))


class OutlineButton(ctk.CTkButton):
    """Кнопка с обводкой"""
    
    def __init__(self, parent, text: str, command: Optional[Callable] = None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color="transparent",
            border_color=Colors.BORDER,
            border_width=2,
            text_color=Colors.FOREGROUND,
            height=Spacing.BUTTON_HEIGHT,
            corner_radius=BorderRadius.BUTTON,
            font=Typography.BASE,
            hover_color=Colors.SECONDARY,
            **kwargs
        )


class Input(ctk.CTkEntry):
    """Поле ввода"""
    
    def __init__(self, parent, placeholder: str = "", height: int = Spacing.INPUT_HEIGHT, **kwargs):
        super().__init__(
            parent,
            placeholder_text=placeholder,
            height=height,
            corner_radius=BorderRadius.BUTTON,
            border_color=Colors.BORDER,
            fg_color=Colors.INPUT,
            text_color=Colors.FOREGROUND,
            placeholder_text_color=Colors.MUTED_FOREGROUND,
            font=Typography.BASE,
            **kwargs
        )


class Label(ctk.CTkLabel):
    """Метка"""
    
    def __init__(self, parent, text: str, font=None, **kwargs):
        if font is None:
            font = Typography.BASE
        if 'text_color' not in kwargs:
            kwargs['text_color'] = Colors.FOREGROUND
        super().__init__(
            parent,
            text=text,
            font=font,
            **kwargs
        )


class ConfirmDialog(ctk.CTkToplevel):
    """Диалог подтверждения"""
    
    def __init__(self, parent, title: str, message: str, on_confirm: Callable[[], None]):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.result = False
        
        self.title(title)
        self.geometry("400x200")
        self.configure(fg_color=Colors.BACKGROUND)
        
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=Typography.CARD_TITLE,
            text_color=Colors.FOREGROUND
        )
        title_label.pack(pady=Spacing.ELEMENT_SPACING)
        
        message_label = ctk.CTkLabel(
            self,
            text=message,
            font=Typography.BASE,
            text_color=Colors.FOREGROUND,
            wraplength=350
        )
        message_label.pack(pady=Spacing.ELEMENT_SPACING, padx=Spacing.SCREEN_PADDING)
        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=Spacing.ELEMENT_SPACING, padx=Spacing.SCREEN_PADDING)
        
        no_btn = OutlineButton(buttons_frame, text="Нет", command=self._on_no)
        no_btn.pack(side="left", fill="x", expand=True, padx=(0, Spacing.SMALL_SPACING))
        
        yes_btn = PrimaryButton(buttons_frame, text="Да", command=self._on_yes)
        yes_btn.pack(side="left", fill="x", expand=True)
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.grab_set()
        self.focus()
    
    def _on_yes(self):
        """Подтвердить"""
        self.result = True
        if self.on_confirm:
            self.on_confirm()
        self.destroy()
    
    def _on_no(self):
        """Отменить"""
        self.result = False
        self.destroy()

