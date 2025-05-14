import pytest
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click_link_by_text(self, text: str):
        self.page.click(f"text={text}")

    def go_back(self):
        self.page.go_back()

    def wait_for_url(self, url_fragment: str):
        self.page.wait_for_url(f"**/{url_fragment}")


class MainPage(BasePage):
    def go_to_frames_page(self):
        self.click_link_by_text("Frames")
        self.wait_for_url("frames")


class FramesPage(BasePage):
    def go_to_nested_frames_page(self):
        self.click_link_by_text("Nested Frames")
        self.wait_for_url("nested_frames")

    def is_nested_frames_link_visible(self) -> bool:
        return self.page.locator("text=Nested Frames").is_visible()


class NestedFramesPage(BasePage):
    def get_frame_text_by_name(self, frame_name: str) -> str:
        # Busca el frame por nombre en la lista de todos los frames
        frame = next(f for f in self.page.frames if f.name == frame_name)
        return frame.locator("body").inner_text().strip()

    def verify_middle_and_left_texts(self):
        middle_text = self.get_frame_text_by_name("frame-middle")
        left_text = self.get_frame_text_by_name("frame-left")

        assert middle_text == "MIDDLE", f"Texto inesperado en frame-middle: {middle_text}"
        assert left_text == "LEFT", f"Texto inesperado en frame-left: {left_text}"

        print("✅ Verificación exitosa: 'MIDDLE' y 'LEFT' encontrados correctamente.")


# -------------------------------
# TEST PRINCIPAL
# -------------------------------
def test_nested_frames_navigation(page: Page):
    page.goto("https://the-internet.herokuapp.com/")

    main_page = MainPage(page)
    main_page.go_to_frames_page()

    frames_page = FramesPage(page)
    frames_page.go_to_nested_frames_page()

    nested_page = NestedFramesPage(page)
    nested_page.verify_middle_and_left_texts()

    # Regresar a la página anterior
    nested_page.go_back()
    frames_page.wait_for_url("frames")
    assert frames_page.is_nested_frames_link_visible(), "No se encontró el enlace 'Nested Frames' al volver atrás."
    print("🔙 Navegación atrás exitosa: se muestra el enlace 'Nested Frames'")
