import customtkinter as ctk
from typing import Callable, Optional
from models import User, Group, Student, Grade
from design_system import Colors, Typography, Spacing, BorderRadius, DesignSystem
from components import (
    Card, PrimaryButton, OutlineButton, Input, Label,
    GradeBadge, GradeSelectorDialog, FooterNav, ConfirmDialog
)
from api_service import ApiService


class BaseScreen(ctk.CTkFrame):
    """Базовый экран"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None]):
        super().__init__(parent, fg_color=Colors.BACKGROUND, corner_radius=0)
        self.api = api
        self.on_navigate = on_navigate
    
    def show(self):
        """Показать экран"""
        self.pack(fill="both", expand=True)
        self.refresh()
    
    def hide(self):
        """Скрыть экран"""
        self.pack_forget()
    
    def refresh(self):
        """Обновить данные экрана (переопределить в дочерних классах)"""
        pass


class LoginScreen(BaseScreen):
    """Экран входа"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None], 
                 on_login_success: Callable[[User], None]):
        super().__init__(parent, api, on_navigate)
        self.on_login_success = on_login_success
        self._build_ui()
    
    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=Spacing.SCREEN_PADDING, pady=Spacing.SCREEN_PADDING)
        
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(pady=(0, Spacing.ELEMENT_SPACING * 2))
        
        icon_frame = ctk.CTkFrame(
            header_frame,
            width=64,
            height=64,
            corner_radius=32,
            fg_color="transparent"
        )
        icon_frame.pack(pady=(0, Spacing.ELEMENT_SPACING))
        icon_label = Label(icon_frame, text="🎓", font=("Arial", 32))
        icon_label.pack(expand=True)
        
        title = Label(header_frame, text="Добро пожаловать", font=Typography.TITLE)
        title.pack()
        
        subtitle = Label(header_frame, text="Успеваемость студентов", 
                        font=Typography.SMALL, text_color=Colors.MUTED_FOREGROUND)
        subtitle.pack()
        
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(fill="x", pady=Spacing.ELEMENT_SPACING)
        
        Label(form_frame, text="Логин", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.login_input = Input(form_frame, placeholder="Введите логин")
        self.login_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        Label(form_frame, text="Пароль", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.password_input = Input(form_frame, placeholder="Введите пароль", show="*")
        self.password_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.error_label = Label(form_frame, text="", font=Typography.SMALL, 
                                text_color=Colors.DESTRUCTIVE)
        self.error_label.pack(pady=(0, Spacing.ELEMENT_SPACING))
        
        login_btn = PrimaryButton(form_frame, text="Войти", command=self._handle_login)
        login_btn.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        register_link = ctk.CTkLabel(
            form_frame,
            text="Нет аккаунта? Зарегистрироваться",
            font=Typography.SMALL,
            text_color=Colors.PRIMARY,
            cursor="hand2"
        )
        register_link.pack()
        register_link.bind("<Button-1>", lambda e: self.on_navigate("/register"))
    
    def _handle_login(self):
        """Обработка входа"""
        login = self.login_input.get().strip()
        password = self.password_input.get().strip()
        
        if not login or not password:
            self.error_label.configure(text="Заполните все поля")
            return
        
        result = self.api.login(login, password)
        if result:
            user = User.from_dict(result["user"])
            self.on_login_success(user)
            self.on_navigate("/")
        else:
            self.error_label.configure(text="Неверный логин или пароль")


class RegisterScreen(BaseScreen):
    """Экран регистрации"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None],
                 on_register_success: Callable[[User], None]):
        super().__init__(parent, api, on_navigate)
        self.on_register_success = on_register_success
        self._build_ui()
    
    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=Spacing.SCREEN_PADDING, pady=Spacing.SCREEN_PADDING)
        
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(pady=(0, Spacing.ELEMENT_SPACING * 2))
        
        icon_frame = ctk.CTkFrame(
            header_frame,
            width=64,
            height=64,
            corner_radius=32,
            fg_color="transparent"
        )
        icon_frame.pack(pady=(0, Spacing.ELEMENT_SPACING))
        icon_label = Label(icon_frame, text="🎓", font=("Arial", 32))
        icon_label.pack(expand=True)
        
        title = Label(header_frame, text="Регистрация", font=Typography.TITLE)
        title.pack()
        
        subtitle = Label(header_frame, text="Создайте новый аккаунт",
                        font=Typography.SMALL, text_color=Colors.MUTED_FOREGROUND)
        subtitle.pack()
        
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(fill="x", pady=Spacing.ELEMENT_SPACING)
        
        Label(form_frame, text="ФИО", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.full_name_input = Input(form_frame, placeholder="Иванов Иван Иванович")
        self.full_name_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        Label(form_frame, text="Логин", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.login_input = Input(form_frame, placeholder="Введите логин")
        self.login_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        Label(form_frame, text="Пароль", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.password_input = Input(form_frame, placeholder="Введите пароль", show="*")
        self.password_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        Label(form_frame, text="Повторите пароль", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.password_confirm_input = Input(form_frame, placeholder="Повторите пароль", show="*")
        self.password_confirm_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.error_label = Label(form_frame, text="", font=Typography.SMALL,
                                text_color=Colors.DESTRUCTIVE)
        self.error_label.pack(pady=(0, Spacing.ELEMENT_SPACING))
        
        register_btn = PrimaryButton(form_frame, text="Зарегистрироваться", command=self._handle_register)
        register_btn.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        login_link = ctk.CTkLabel(
            form_frame,
            text="Уже есть аккаунт? Войти",
            font=Typography.SMALL,
            text_color=Colors.PRIMARY,
            cursor="hand2"
        )
        login_link.pack()
        login_link.bind("<Button-1>", lambda e: self.on_navigate("/login"))
    
    def _handle_register(self):
        """Обработка регистрации"""
        full_name = self.full_name_input.get().strip()
        login = self.login_input.get().strip()
        password = self.password_input.get().strip()
        password_confirm = self.password_confirm_input.get().strip()
        
        if not all([full_name, login, password, password_confirm]):
            self.error_label.configure(text="Заполните все поля")
            return
        
        if password != password_confirm:
            self.error_label.configure(text="Пароли не совпадают")
            return
        
        result = self.api.register(full_name, login, password)
        if result:
            user = User.from_dict(result["user"])
            self.on_register_success(user)
            self.on_navigate("/")
        else:
            self.error_label.configure(text="Ошибка регистрации. Возможно, логин уже занят")


class ProfileScreen(BaseScreen):
    """Главная страница / Профиль"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None], 
                 current_user: User, on_logout: Optional[Callable[[], None]] = None):
        super().__init__(parent, api, on_navigate)
        self.current_user = current_user
        self.is_editing = False
        self.on_logout = on_logout
        self._build_ui()
        self._load_statistics()
    
    def _build_ui(self):
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=Spacing.SCREEN_PADDING, 
                       pady=Spacing.SCREEN_PADDING)
        
        profile_card = Card(main_frame)
        profile_card.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        profile_content = ctk.CTkFrame(profile_card, fg_color="transparent")
        profile_content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
        
        header = ctk.CTkFrame(profile_content, fg_color="transparent")
        header.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.profile_info_frame = ctk.CTkFrame(profile_content, fg_color="transparent")
        self.profile_info_frame.pack(side="left", fill="x", expand=True)
        
        logout_btn = ctk.CTkButton(
            header,
            text="🚪",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent",
            hover_color=DesignSystem.with_opacity(Colors.DESTRUCTIVE, 0.2),  
            command=self._handle_logout
        )
        logout_btn.pack(side="right", padx=(0, Spacing.SMALL_SPACING))
        
        self.settings_btn = ctk.CTkButton(
            header,
            text="⚙️",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent",
            hover_color=Colors.SECONDARY,
            command=self._toggle_edit
        )
        self.settings_btn.pack(side="right")
        
        self._update_profile_display()
        
        stats_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        groups_card = Card(stats_frame)
        groups_card.pack(side="left", fill="both", expand=True, padx=(0, Spacing.SMALL_SPACING))
        
        groups_content = ctk.CTkFrame(groups_card, fg_color="transparent")
        groups_content.pack(fill="both", expand=True, padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
        
        icon_frame = ctk.CTkFrame(
            groups_content,
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent"
        )
        icon_frame.pack(anchor="w", pady=(0, Spacing.SMALL_SPACING))
        Label(icon_frame, text="📁", font=("Arial", 20)).pack(expand=True)
        
        self.groups_count_label = Label(groups_content, text="0", font=Typography.STATS)
        self.groups_count_label.pack(anchor="w")
        
        Label(groups_content, text="Групп", font=Typography.SMALL,
             text_color=Colors.MUTED_FOREGROUND).pack(anchor="w")
        
        students_card = Card(stats_frame)
        students_card.pack(side="left", fill="both", expand=True, padx=(Spacing.SMALL_SPACING, 0))
        
        students_content = ctk.CTkFrame(students_card, fg_color="transparent")
        students_content.pack(fill="both", expand=True, padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
        
        icon_frame2 = ctk.CTkFrame(
            students_content,
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent"
        )
        icon_frame2.pack(anchor="w", pady=(0, Spacing.SMALL_SPACING))
        Label(icon_frame2, text="👥", font=("Arial", 20)).pack(expand=True)
        
        self.students_count_label = Label(students_content, text="0", font=Typography.STATS)
        self.students_count_label.pack(anchor="w")
        
        Label(students_content, text="Студентов", font=Typography.SMALL,
             text_color=Colors.MUTED_FOREGROUND).pack(anchor="w")
    
    def _update_profile_display(self):
        """Обновить отображение профиля"""
        for widget in self.profile_info_frame.winfo_children():
            widget.destroy()
        
        if self.is_editing:
            Label(self.profile_info_frame, text="ФИО", font=Typography.XSMALL).pack(anchor="w", pady=(0, 4))
            self.full_name_edit = Input(self.profile_info_frame, height=40, 
                                       placeholder=self.current_user.full_name)
            self.full_name_edit.insert(0, self.current_user.full_name)
            self.full_name_edit.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
            
            Label(self.profile_info_frame, text="Логин", font=Typography.XSMALL).pack(anchor="w", pady=(0, 4))
            self.login_edit = Input(self.profile_info_frame, height=40,
                                   placeholder=self.current_user.login)
            self.login_edit.insert(0, self.current_user.login)
            self.login_edit.pack(fill="x")
        else:
            Label(self.profile_info_frame, text=self.current_user.full_name,
                 font=Typography.TITLE).pack(anchor="w")
            Label(self.profile_info_frame, text=f"@{self.current_user.login}",
                 font=Typography.SMALL, text_color=Colors.MUTED_FOREGROUND).pack(anchor="w")
    
    def _toggle_edit(self):
        """Переключить режим редактирования"""
        if self.is_editing:
            full_name = self.full_name_edit.get().strip()
            login = self.login_edit.get().strip()
            
            if full_name and login:
                updated_user = self.api.update_user(full_name, login)
                if updated_user:
                    self.current_user = updated_user
            
            self.is_editing = False
            self.settings_btn.configure(text="⚙️")
        else:
            self.is_editing = True
            self.settings_btn.configure(text="✓")
        
        self._update_profile_display()
    
    def _handle_logout(self):
        """Обработка выхода"""
        if self.on_logout:
            self.on_logout()
    
    def refresh(self):
        """Обновить данные экрана"""
        updated_user = self.api.get_current_user()
        if updated_user:
            self.current_user = updated_user
            self._update_profile_display()
        self._load_statistics()
    
    def _load_statistics(self):
        """Загрузить статистику"""
        groups = self.api.get_groups()
        students = self.api.get_students()
        
        self.groups_count_label.configure(text=str(len(groups)))
        self.students_count_label.configure(text=str(len(students)))


class GroupsScreen(BaseScreen):
    """Список групп"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None]):
        super().__init__(parent, api, on_navigate)
        self.groups = []
        self._build_ui()
        self._load_groups()
    
    def _build_ui(self):
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=Spacing.SCREEN_PADDING, 
                       pady=Spacing.SCREEN_PADDING)
        
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.search_input = Input(search_frame, placeholder="Поиск группы...")
        self.search_input.pack(side="left", fill="x", expand=True, padx=(0, Spacing.SMALL_SPACING))
        self.search_input.bind("<KeyRelease>", lambda e: self._filter_groups())
        
        add_btn = ctk.CTkButton(
            search_frame,
            text="+",
            width=Spacing.BUTTON_HEIGHT,
            height=Spacing.BUTTON_HEIGHT,
            corner_radius=BorderRadius.BUTTON,
            fg_color=Colors.PRIMARY,
            command=lambda: self.on_navigate("/groups/add")
        )
        add_btn.pack(side="right")
        
        self.groups_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.groups_frame.pack(fill="both", expand=True)
    
    def refresh(self):
        """Обновить данные экрана"""
        self._load_groups()
    
    def _load_groups(self):
        """Загрузить группы"""
        self.groups = self.api.get_groups()
        self._render_groups()
    
    def _delete_group(self, group_id: int):
        """Удалить группу"""
        def on_confirm():
            if self.api.delete_group(group_id):
                self._load_groups()
        
        dialog = ConfirmDialog(
            self,
            "Удаление группы",
            "Вы точно хотите удалить группу и всех студентов в ней?",
            on_confirm
        )
    
    def _filter_groups(self):
        """Фильтровать группы по поисковому запросу"""
        self._render_groups()
    
    def _render_groups(self):
        """Отобразить группы"""
        for widget in self.groups_frame.winfo_children():
            widget.destroy()
        
        search_query = self.search_input.get().strip().lower()
        filtered_groups = [
            g for g in self.groups
            if search_query in g.name.lower()
        ]
        
        if not filtered_groups:
            empty_label = Label(
                self.groups_frame,
                text="Группы не найдены" if search_query else "Нет групп",
                font=Typography.SMALL,
                text_color=Colors.MUTED_FOREGROUND
            )
            empty_label.pack(pady=Spacing.ELEMENT_SPACING * 3)
            return
        
        all_students = self.api.get_students()
        
        for group in filtered_groups:
            group_students = [s for s in all_students if s.group_id == group.id]
            not_allowed_count = sum(1 for s in group_students if not s.is_allowed(group.control_sum))
            
            card = Card(self.groups_frame)
            card.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
            
            header = ctk.CTkFrame(content, fg_color="transparent")
            header.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
            
            name_label = Label(header, text=group.name, font=Typography.CARD_TITLE)
            name_label.pack(side="left", anchor="w")
            
            delete_btn = ctk.CTkButton(
                header,
                text="✕",
                width=24,
                height=24,
                corner_radius=12,
                fg_color=Colors.DESTRUCTIVE,
                hover_color=Colors.DESTRUCTIVE,
                command=lambda gid=group.id: self._delete_group(gid)
            )
            delete_btn.pack(side="right")
            
            stats_frame = ctk.CTkFrame(content, fg_color="transparent")
            stats_frame.pack(fill="x")
            
            Label(stats_frame, text=f"Студентов: {len(group_students)}",
                 font=Typography.SMALL).pack(side="left", anchor="w")
            Label(stats_frame, text=f"Недопущены: {not_allowed_count}",
                 font=Typography.SMALL, text_color=Colors.DESTRUCTIVE).pack(side="left", anchor="w", padx=(Spacing.ELEMENT_SPACING, 0))
            
            def on_card_click(e, gid=group.id):
                widget = e.widget
                while widget:
                    if widget == delete_btn:
                        return  
                    widget = widget.master if hasattr(widget, 'master') else None
                self.on_navigate(f"/groups/{gid}")
            
            def on_enter(e):
                card.configure(cursor="hand2")
            
            def on_leave(e):
                card.configure(cursor="")
            
            card.bind("<Button-1>", on_card_click)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            content.bind("<Button-1>", on_card_click)
            name_label.bind("<Button-1>", on_card_click)
            stats_frame.bind("<Button-1>", on_card_click)
            
            delete_btn.bind("<Button-1>", lambda e: None)


class AddGroupScreen(BaseScreen):
    """Добавление группы"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None]):
        super().__init__(parent, api, on_navigate)
        self.students_to_add = []
        self.show_add_form = False
        self._build_ui()
    
    def _build_ui(self):
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=Spacing.SCREEN_PADDING, 
                       pady=Spacing.SCREEN_PADDING)
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Назад",
            width=100,
            height=40,
            corner_radius=BorderRadius.BUTTON,
            fg_color="transparent",
            hover_color=Colors.SECONDARY,
            command=lambda: self.on_navigate("/groups")
        )
        back_btn.pack(anchor="w", pady=(0, Spacing.ELEMENT_SPACING))
        
        Label(main_frame, text="Новая группа", font=Typography.TITLE).pack(anchor="w", pady=(0, Spacing.ELEMENT_SPACING))
        
        form_card = Card(main_frame)
        form_card.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
        
        Label(form_content, text="Название группы", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.name_input = Input(form_content, placeholder="А12")
        self.name_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        Label(form_content, text="Контрольная сумма", font=Typography.SMALL).pack(anchor="w", pady=(0, 4))
        self.control_sum_input = Input(form_content, placeholder="12")
        self.control_sum_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        add_group_btn = PrimaryButton(form_content, text="Добавить группу", command=self._create_group)
        add_group_btn.pack(fill="x")
        
        students_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        students_section.pack(fill="x", pady=(Spacing.ELEMENT_SPACING, 0))
        
        students_header = ctk.CTkFrame(students_section, fg_color="transparent")
        students_header.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        Label(students_header, text="Студенты", font=Typography.CARD_TITLE).pack(side="left")
        
        add_student_btn = ctk.CTkButton(
            students_header,
            text="+",
            width=32,
            height=32,
            corner_radius=BorderRadius.BUTTON,
            fg_color=Colors.PRIMARY,
            command=self._toggle_add_form
        )
        add_student_btn.pack(side="right")
        
        self.add_form_frame = ctk.CTkFrame(students_section, fg_color="transparent")
        
        self.students_list_frame = ctk.CTkFrame(students_section, fg_color="transparent")
        self.students_list_frame.pack(fill="x")
        self._render_students_list()
    
    def _toggle_add_form(self):
        """Показать/скрыть форму добавления студента"""
        if self.show_add_form:
            self.add_form_frame.pack_forget()
            self.show_add_form = False
        else:
            self._build_add_form()
            self.add_form_frame.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
            self.show_add_form = True
    
    def _build_add_form(self):
        """Построить форму добавления студента"""
        for widget in self.add_form_frame.winfo_children():
            widget.destroy()
        
        form_card = Card(self.add_form_frame)
        form_card.pack(fill="x")
        
        form_content = ctk.CTkFrame(form_card, fg_color="transparent")
        form_content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
        
        self.student_name_input = Input(form_content, height=40, placeholder="Иванов И. И.")
        self.student_name_input.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
        
        buttons_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        add_btn = PrimaryButton(buttons_frame, text="Добавить", command=self._add_student)
        add_btn.pack(side="left", fill="x", expand=True, padx=(0, Spacing.SMALL_SPACING))
        
        cancel_btn = OutlineButton(buttons_frame, text="Отмена", command=self._toggle_add_form)
        cancel_btn.pack(side="left", fill="x", expand=True)
    
    def _add_student(self):
        """Добавить студента в список"""
        name = self.student_name_input.get().strip()
        if name:
            self.students_to_add.append(name)
            self.student_name_input.delete(0, "end")
            self._render_students_list()
            self._toggle_add_form()
    
    def _remove_student(self, index: int):
        """Удалить студента из списка"""
        self.students_to_add.pop(index)
        self._render_students_list()
    
    def _render_students_list(self):
        """Отобразить список студентов"""
        for widget in self.students_list_frame.winfo_children():
            widget.destroy()
        
        if not self.students_to_add:
            empty_label = Label(
                self.students_list_frame,
                text="Нажмите +, чтобы добавить студентов",
                font=Typography.SMALL,
                text_color=Colors.MUTED_FOREGROUND
            )
            empty_label.pack(pady=Spacing.ELEMENT_SPACING * 2)
            return
        
        for i, name in enumerate(self.students_to_add):
            card = Card(self.students_list_frame)
            card.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
            
            Label(content, text=name, font=Typography.BASE).pack(side="left", fill="x", expand=True)
            
            delete_btn = ctk.CTkButton(
                content,
                text="✕",
                width=24,
                height=24,
                corner_radius=12,
                fg_color=Colors.DESTRUCTIVE,
                command=lambda idx=i: self._remove_student(idx)
            )
            delete_btn.pack(side="right")
    
    def _create_group(self):
        """Создать группу"""
        name = self.name_input.get().strip()
        try:
            control_sum = int(self.control_sum_input.get().strip())
        except ValueError:
            return
        
        if not name:
            return
        
        group = self.api.create_group(name, control_sum)
        if group:
            for student_name in self.students_to_add:
                self.api.create_student(student_name, group.id)
            
            self.on_navigate("/groups")


class GroupDetailScreen(BaseScreen):
    """Детали группы"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None], group_id: int):
        super().__init__(parent, api, on_navigate)
        self.group_id = group_id
        self.group: Optional[Group] = None
        self.students = []
        self.is_editing = False
        self.filter_type = "all"  # all, allowed, notAllowed
        self.search_query = ""
        self.show_add_form = False
        self._load_data()
        self._build_ui()
    
    def refresh(self):
        """Обновить данные экрана"""
        self._load_data()
        if hasattr(self, 'students_frame'):
            self._update_students_list()
        if hasattr(self, 'info_frame') and self.group:
            self._update_info_display()
    
    def _load_data(self):
        """Загрузить данные группы"""
        self.group, self.students = self.api.get_group_with_students(self.group_id)
    
    def _build_ui(self):
        if not self.group:
            Label(self, text="Группа не найдена", font=Typography.TITLE).pack(expand=True)
            return
        
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=Spacing.SCREEN_PADDING, 
                       pady=Spacing.SCREEN_PADDING)
        
        back_btn = ctk.CTkButton(
            main_frame,
            text="← Назад",
            width=100,
            height=40,
            corner_radius=BorderRadius.BUTTON,
            fg_color="transparent",
            hover_color=Colors.SECONDARY,
            command=lambda: self.on_navigate("/groups")
        )
        back_btn.pack(anchor="w", pady=(0, Spacing.ELEMENT_SPACING))
        
        info_card = Card(main_frame)
        info_card.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        info_content = ctk.CTkFrame(info_card, fg_color="transparent")
        info_content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
        
        header = ctk.CTkFrame(info_content, fg_color="transparent")
        header.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.info_frame = ctk.CTkFrame(info_content, fg_color="transparent")
        self.info_frame.pack(side="left", fill="x", expand=True)
        
        self.settings_btn = ctk.CTkButton(
            header,
            text="⚙️",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent",
            hover_color=Colors.SECONDARY,
            command=self._toggle_edit
        )
        self.settings_btn.pack(side="right")
        
        self._update_info_display()
        
        self.search_input = Input(main_frame, placeholder="Поиск студента...")
        self.search_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        self.search_input.bind("<KeyRelease>", lambda e: self._update_students_list())
        
        filters_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filters_frame.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.filter_buttons = {}
        filter_buttons = [
            ("all", "Все"),
            ("allowed", "Допущенные"),
            ("notAllowed", "Недопущенные")
        ]
        
        for filter_type, label in filter_buttons:
            btn = ctk.CTkButton(
                filters_frame,
                text=label,
                height=36,
                corner_radius=BorderRadius.BUTTON,
                fg_color=Colors.PRIMARY if self.filter_type == filter_type else "transparent",
                border_color=Colors.BORDER if self.filter_type != filter_type else Colors.PRIMARY,
                border_width=2 if self.filter_type != filter_type else 0,
                text_color=Colors.FOREGROUND,
                command=lambda ft=filter_type: self._set_filter(ft)
            )
            btn.pack(side="left", fill="x", expand=True, padx=(0, Spacing.SMALL_SPACING))
            self.filter_buttons[filter_type] = btn
        
        self.add_student_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        self._update_add_student_section()
        
        self.students_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.students_frame.pack(fill="both", expand=True)
        self._update_students_list()
    
    def _update_info_display(self):
        """Обновить отображение информации о группе"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        if self.is_editing:
            Label(self.info_frame, text="Название", font=Typography.XSMALL).pack(anchor="w", pady=(0, 4))
            self.name_edit = Input(self.info_frame, height=40, placeholder=self.group.name)
            self.name_edit.insert(0, self.group.name)
            self.name_edit.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
            
            Label(self.info_frame, text="Контрольная сумма", font=Typography.XSMALL).pack(anchor="w", pady=(0, 4))
            self.control_sum_edit = Input(self.info_frame, height=40, placeholder=str(self.group.control_sum))
            self.control_sum_edit.insert(0, str(self.group.control_sum))
            self.control_sum_edit.pack(fill="x")
        else:
            Label(self.info_frame, text=self.group.name, font=Typography.TITLE).pack(anchor="w")
            Label(self.info_frame, text=f"Контрольная сумма: {self.group.control_sum}",
                 font=Typography.SMALL, text_color=Colors.MUTED_FOREGROUND).pack(anchor="w")
    
    def _toggle_edit(self):
        """Переключить режим редактирования"""
        if self.is_editing:
            name = self.name_edit.get().strip()
            try:
                control_sum = int(self.control_sum_edit.get().strip())
            except ValueError:
                return
            
            if name:
                updated_group = self.api.update_group(self.group_id, name, control_sum)
                if updated_group:
                    self.group = updated_group
            
            self.is_editing = False
            self.settings_btn.configure(text="⚙️")
        else:
            self.is_editing = True
            self.settings_btn.configure(text="✓")
        
        self._update_info_display()
        self._update_add_student_section()
        self._update_students_list()
    
    def _set_filter(self, filter_type: str):
        """Установить фильтр"""
        self.filter_type = filter_type
        if hasattr(self, 'filter_buttons'):
            for ft, btn in self.filter_buttons.items():
                is_active = ft == filter_type
                btn.configure(
                    fg_color=Colors.PRIMARY if is_active else "transparent",
                    border_color=Colors.PRIMARY if is_active else Colors.BORDER,
                    border_width=0 if is_active else 2
                )
        self._update_students_list()
    
    def _update_add_student_section(self):
        """Обновить секцию добавления студента"""
        for widget in self.add_student_section.winfo_children():
            widget.destroy()
        
        if not self.is_editing:
            return
        
        self.add_student_section.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        header = ctk.CTkFrame(self.add_student_section, fg_color="transparent")
        header.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
        
        Label(header, text="Добавить студента", font=Typography.SMALL,
             text_color=Colors.MUTED_FOREGROUND).pack(side="left")
        
        add_btn = ctk.CTkButton(
            header,
            text="+",
            width=32,
            height=32,
            corner_radius=BorderRadius.BUTTON,
            fg_color=Colors.PRIMARY,
            command=self._toggle_add_form
        )
        add_btn.pack(side="right")
        
        self.add_form_frame = ctk.CTkFrame(self.add_student_section, fg_color="transparent")
    
    def _toggle_add_form(self):
        """Показать/скрыть форму добавления студента"""
        for widget in self.add_form_frame.winfo_children():
            widget.destroy()
        
        if self.show_add_form:
            self.add_form_frame.pack_forget()
            self.show_add_form = False
        else:
            form_card = Card(self.add_form_frame)
            form_card.pack(fill="x")
            
            form_content = ctk.CTkFrame(form_card, fg_color="transparent")
            form_content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
            
            self.student_name_input = Input(form_content, height=40, placeholder="Иванов И. И.")
            self.student_name_input.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
            
            buttons_frame = ctk.CTkFrame(form_content, fg_color="transparent")
            buttons_frame.pack(fill="x")
            
            add_btn = PrimaryButton(buttons_frame, text="Добавить", command=self._add_student)
            add_btn.pack(side="left", fill="x", expand=True, padx=(0, Spacing.SMALL_SPACING))
            
            cancel_btn = OutlineButton(buttons_frame, text="Отмена", command=self._toggle_add_form)
            cancel_btn.pack(side="left", fill="x", expand=True)
            
            self.add_form_frame.pack(fill="x")
            self.show_add_form = True
    
    def _add_student(self):
        """Добавить студента"""
        name = self.student_name_input.get().strip()
        if name:
            student = self.api.create_student(name, self.group_id)
            if student:
                self._load_data()
                self._update_students_list()
                self._toggle_add_form()
    
    def _update_students_list(self):
        """Обновить список студентов"""
        for widget in self.students_frame.winfo_children():
            widget.destroy()
        
        if not self.group:
            return
        
        self.search_query = self.search_input.get().strip().lower()
        
        filtered_students = self.students.copy()
        
        if self.search_query:
            filtered_students = [
                s for s in filtered_students
                if self.search_query in s.full_name.lower()
            ]
        
        if self.filter_type == "allowed":
            filtered_students = [
                s for s in filtered_students
                if s.is_allowed(self.group.control_sum)
            ]
        elif self.filter_type == "notAllowed":
            filtered_students = [
                s for s in filtered_students
                if not s.is_allowed(self.group.control_sum)
            ]
        
        filtered_students.sort(key=lambda s: s.full_name)
        
        if not filtered_students:
            empty_label = Label(
                self.students_frame,
                text="Студенты не найдены" if self.search_query else "Нет студентов",
                font=Typography.SMALL,
                text_color=Colors.MUTED_FOREGROUND
            )
            empty_label.pack(pady=Spacing.ELEMENT_SPACING * 3)
            return
        
        for student in filtered_students:
            is_allowed = student.is_allowed(self.group.control_sum)
            
            card = Card(self.students_frame)
            if is_allowed:
                card.configure(border_color=Colors.SUCCESS_GLOW, border_width=2)
            card.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
            
            header = ctk.CTkFrame(content, fg_color="transparent")
            header.pack(fill="x", pady=(0, Spacing.SMALL_SPACING))
            
            Label(header, text=student.format_name(), font=Typography.BASE).pack(side="left", fill="x", expand=True)
            
            if self.is_editing:
                delete_btn = ctk.CTkButton(
                    header,
                    text="✕",
                    width=24,
                    height=24,
                    corner_radius=12,
                    fg_color=Colors.DESTRUCTIVE,
                    command=lambda sid=student.id: self._delete_student(sid)
                )
                delete_btn.pack(side="right")
            
            grades_frame = ctk.CTkFrame(content, fg_color="transparent")
            grades_frame.pack(fill="x")
            
            for i, grade in enumerate(student.grades):
                badge = GradeBadge(
                    grades_frame,
                    grade,
                    command=lambda idx=i, sid=student.id: self._open_grade_selector(sid, idx)
                )
                badge.pack(side="left", padx=(0, Spacing.SMALL_SPACING))
    
    def _open_grade_selector(self, student_id: int, grade_index: int):
        """Открыть диалог выбора оценки"""
        student = next((s for s in self.students if s.id == student_id), None)
        if not student:
            return
        
        current_grade = student.grades[grade_index] if grade_index < len(student.grades) else Grade.EMPTY
        
        def on_select(grade: Optional[Grade]):
            self.api.update_student_grade(student_id, grade_index, grade)
            self._load_data()
            self._update_students_list()
        
        dialog = GradeSelectorDialog(self, on_select)
    
    def _delete_student(self, student_id: int):
        """Удалить студента"""
        if self.api.delete_student(student_id):
            self._load_data()
            self._update_students_list()


class StudentsScreen(BaseScreen):
    """Список студентов"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None]):
        super().__init__(parent, api, on_navigate)
        self.students = []
        self.groups = []
        self.filter_type = "all"
        self.search_query = ""
        self._load_data()
        self._build_ui()
    
    def refresh(self):
        """Обновить данные экрана"""
        self._load_data()
        self._update_students_list()
    
    def _load_data(self):
        """Загрузить данные"""
        self.students = self.api.get_students()
        self.groups = self.api.get_groups()
    
    def _build_ui(self):
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=Spacing.SCREEN_PADDING, 
                       pady=Spacing.SCREEN_PADDING)
        
        Label(main_frame, text="Студенты", font=Typography.TITLE).pack(anchor="w", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.search_input = Input(main_frame, placeholder="Поиск студента...")
        self.search_input.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        self.search_input.bind("<KeyRelease>", lambda e: self._update_students_list())
        
        filters_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filters_frame.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
        
        self.filter_buttons = {}
        filter_buttons = [
            ("all", "Все"),
            ("allowed", "Допущенные"),
            ("notAllowed", "Недопущенные")
        ]
        
        for filter_type, label in filter_buttons:
            btn = ctk.CTkButton(
                filters_frame,
                text=label,
                height=36,
                corner_radius=BorderRadius.BUTTON,
                fg_color=Colors.PRIMARY if self.filter_type == filter_type else "transparent",
                border_color=Colors.BORDER if self.filter_type != filter_type else Colors.PRIMARY,
                border_width=2 if self.filter_type != filter_type else 0,
                text_color=Colors.FOREGROUND,
                command=lambda ft=filter_type: self._set_filter(ft)
            )
            btn.pack(side="left", fill="x", expand=True, padx=(0, Spacing.SMALL_SPACING))
            self.filter_buttons[filter_type] = btn
        
        self.students_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.students_frame.pack(fill="both", expand=True)
        self._update_students_list()
    
    def _set_filter(self, filter_type: str):
        """Установить фильтр"""
        self.filter_type = filter_type
        if hasattr(self, 'filter_buttons'):
            for ft, btn in self.filter_buttons.items():
                is_active = ft == filter_type
                btn.configure(
                    fg_color=Colors.PRIMARY if is_active else "transparent",
                    border_color=Colors.PRIMARY if is_active else Colors.BORDER,
                    border_width=0 if is_active else 2
                )
        self._update_students_list()
    
    def _update_students_list(self):
        """Обновить список студентов"""
        for widget in self.students_frame.winfo_children():
            widget.destroy()
        
        self.search_query = self.search_input.get().strip().lower()
        
        filtered_students = self.students.copy()
        
        if self.search_query:
            filtered_students = [
                s for s in filtered_students
                if self.search_query in s.full_name.lower()
            ]
        
        if self.filter_type == "allowed":
            filtered_students = [
                s for s in filtered_students
                if self._is_student_allowed(s)
            ]
        elif self.filter_type == "notAllowed":
            filtered_students = [
                s for s in filtered_students
                if not self._is_student_allowed(s)
            ]
        
        filtered_students.sort(key=lambda s: s.full_name)
        
        if not filtered_students:
            empty_label = Label(
                self.students_frame,
                text="Студенты не найдены" if self.search_query else "Нет студентов",
                font=Typography.SMALL,
                text_color=Colors.MUTED_FOREGROUND
            )
            empty_label.pack(pady=Spacing.ELEMENT_SPACING * 3)
            return
        
        for student in filtered_students:
            group = next((g for g in self.groups if g.id == student.group_id), None)
            is_allowed = self._is_student_allowed(student)
            
            card = Card(self.students_frame)
            if is_allowed:
                card.configure(border_color=Colors.SUCCESS_GLOW, border_width=2)
            card.pack(fill="x", pady=(0, Spacing.ELEMENT_SPACING))
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=Spacing.CARD_PADDING, pady=Spacing.CARD_PADDING)
            
            Label(content, text=student.format_name(), font=Typography.BASE).pack(anchor="w", pady=(0, 4))
            if group:
                Label(content, text=group.name, font=Typography.SMALL,
                     text_color=Colors.MUTED_FOREGROUND).pack(anchor="w", pady=(0, Spacing.SMALL_SPACING))
            
            grades_frame = ctk.CTkFrame(content, fg_color="transparent")
            grades_frame.pack(fill="x")
            
            for i, grade in enumerate(student.grades):
                badge = GradeBadge(
                    grades_frame,
                    grade,
                    command=lambda idx=i, sid=student.id: self._open_grade_selector(sid, idx)
                )
                badge.pack(side="left", padx=(0, Spacing.SMALL_SPACING))
    
    def _is_student_allowed(self, student: Student) -> bool:
        """Проверить, допущен ли студент"""
        group = next((g for g in self.groups if g.id == student.group_id), None)
        if not group:
            return False
        return student.is_allowed(group.control_sum)
    
    def _open_grade_selector(self, student_id: int, grade_index: int):
        """Открыть диалог выбора оценки"""
        student = next((s for s in self.students if s.id == student_id), None)
        if not student:
            return
        
        def on_select(grade: Optional[Grade]):
            self.api.update_student_grade(student_id, grade_index, grade)
            self._load_data()
            self._update_students_list()
        
        dialog = GradeSelectorDialog(self, on_select)


class NotFoundScreen(BaseScreen):
    """Страница 404"""
    
    def __init__(self, parent, api: ApiService, on_navigate: Callable[[str], None]):
        super().__init__(parent, api, on_navigate)
        self._build_ui()
    
    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both")
        
        Label(container, text="404", font=("Arial", 48, "bold")).pack(pady=Spacing.ELEMENT_SPACING)
        Label(container, text="Oops! Page not found",
             font=Typography.CARD_TITLE, text_color=Colors.MUTED_FOREGROUND).pack(pady=(0, Spacing.ELEMENT_SPACING))
        
        home_btn = ctk.CTkLabel(
            container,
            text="Return to Home",
            font=Typography.SMALL,
            text_color=Colors.PRIMARY,
            cursor="hand2"
        )
        home_btn.pack()
        home_btn.bind("<Button-1>", lambda e: self.on_navigate("/"))
