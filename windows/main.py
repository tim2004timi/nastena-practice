import customtkinter as ctk
from typing import Optional
from models import User
from design_system import DesignSystem, Colors
from api_service import ApiService
from screens import (
    LoginScreen, RegisterScreen, ProfileScreen,
    GroupsScreen, AddGroupScreen, GroupDetailScreen,
    StudentsScreen, NotFoundScreen
)
from components import FooterNav


class App(ctk.CTk):
    """Главное приложение"""
    
    def __init__(self):
        super().__init__()
        
        DesignSystem.setup_theme()
        
        self.title("Успеваемость студентов")
        self.geometry("1000x1000")
        self.minsize(800, 600)
        
        self.configure(fg_color=Colors.BACKGROUND)
        
        self.api = ApiService()
        
        self.current_user: Optional[User] = None
        
        self.current_route = "/login"
        
        self.screens = {}
        
        self.footer_nav: Optional[FooterNav] = None
        
        self._init_ui()
        self._navigate("/login")
    
    def _init_ui(self):
        """Инициализация UI"""
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        self.footer_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, height=64)
        self.footer_container.pack(fill="x", side="bottom")
    
    def _navigate(self, route: str):
        """Навигация по маршрутам"""
        for screen in self.screens.values():
            screen.hide()
        
        if self.footer_nav:
            self.footer_nav.destroy()
            self.footer_nav = None
        
        self.current_route = route
        
        if route not in ["/login", "/register"]:
            if not self.current_user:
                route = "/login"
        
        if route not in self.screens:
            self.screens[route] = self._create_screen(route)
        
        if route in self.screens:
            self.screens[route].show()
        
        if route in ["/", "/students", "/groups"]:
            self._show_footer()
        elif route.startswith("/groups/") and route != "/groups/add":
            self._show_footer()
    
    def _create_screen(self, route: str):
        """Создать экран по маршруту"""
        if route == "/login":
            return LoginScreen(
                self.main_container,
                self.api,
                self._navigate,
                self._on_login_success
            )
        elif route == "/register":
            return RegisterScreen(
                self.main_container,
                self.api,
                self._navigate,
                self._on_register_success
            )
        elif route == "/":
            if not self.current_user:
                return None
            return ProfileScreen(
                self.main_container,
                self.api,
                self._navigate,
                self.current_user,
                self._on_logout
            )
        elif route == "/groups":
            return GroupsScreen(
                self.main_container,
                self.api,
                self._navigate
            )
        elif route == "/groups/add":
            return AddGroupScreen(
                self.main_container,
                self.api,
                self._navigate
            )
        elif route.startswith("/groups/") and route != "/groups/add":
            group_id_str = route.split("/")[-1]
            if group_id_str:
                try:
                    group_id = int(group_id_str)
                    return GroupDetailScreen(
                        self.main_container,
                        self.api,
                        self._navigate,
                        group_id
                    )
                except ValueError:
                    return None
        elif route == "/students":
            return StudentsScreen(
                self.main_container,
                self.api,
                self._navigate
            )
        else:
            return NotFoundScreen(
                self.main_container,
                self.api,
                self._navigate
            )
    
    def _show_footer(self):
        """Показать футер-навигацию"""
        self.footer_nav = FooterNav(
            self.footer_container,
            self._navigate,
            self.current_route
        )
        self.footer_nav.pack(fill="x", side="bottom")
    
    def _on_login_success(self, user: User):
        """Обработка успешного входа"""
        self.current_user = user
        if "/" in self.screens:
            del self.screens["/"]
        self._navigate("/")
    
    def _on_register_success(self, user: User):
        """Обработка успешной регистрации"""
        self.current_user = user
        if "/" in self.screens:
            del self.screens["/"]
        self._navigate("/")
    
    def _on_logout(self):
        """Обработка выхода"""
        self.current_user = None
        for screen in list(self.screens.values()):
            screen.hide()
            screen.destroy()
        self.screens.clear()
        self.api.set_token("")
        self._navigate("/login")
    
    def run(self):
        """Запустить приложение"""
        self.mainloop()


def main():
    """Точка входа"""
    app = App()
    app.run()


if __name__ == "__main__":
    main()

