from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
import fitz  # PyMuPDF
from PIL import Image
import os

# PDF Compression Function
def compress_scanned_pdf(input_pdf_path, output_pdf_path, max_size_kb=300, quality=50, dpi=100):
    pdf_document = fitz.open(input_pdf_path)
    new_doc = fitz.open()
    temp_image_paths = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72), colorspace=fitz.csRGB)
        img_path = f"temp_page_{page_num}.jpg"
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image.save(img_path, "JPEG", quality=quality)
        temp_image_paths.append(img_path)

        rect = fitz.Rect(0, 0, pix.width, pix.height)
        new_page = new_doc.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(rect, filename=img_path)

    new_doc.save(output_pdf_path, deflate=True)
    new_doc.close()
    pdf_document.close()

    for img_path in temp_image_paths:
        os.remove(img_path)

    if os.path.getsize(output_pdf_path) > max_size_kb * 1024:
        print(f"Warning: The output file is still larger than {max_size_kb} KB.")
    else:
        print(f"Successfully compressed to under {max_size_kb} KB.")

# KivyMD App Class
class PDFCompressorApp(MDApp):
    selected_file = StringProperty("No file selected")
    compression_quality = NumericProperty(50)
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        Window.size = (400, 600)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[".pdf"]
        )
        return super().build()  # The .kv file will be loaded automatically

    def show_file_manager(self):
        self.file_manager.show(os.path.expanduser("~"))  # Opens the home directory

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.selected_file = path
        self.exit_manager()

    def compress_pdf(self):
        if not self.selected_file or self.selected_file == "No file selected":
            self.show_dialog("Please select a PDF file first.")
            return

        output_path = self.selected_file.replace(".pdf", "_compressed.pdf")
        compress_scanned_pdf(
            input_pdf_path=self.selected_file,
            output_pdf_path=output_path,
            quality=self.compression_quality
        )
        self.show_dialog(f"Compression complete! Saved to: {output_path}")

    def show_dialog(self, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(title="Info", text=text, size_hint=(0.8, 1), buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

if __name__ == "__main__":
    PDFCompressorApp().run()


# def show_error_dialog(self, error_message):
#     error_dialog = MDDialog(
#         title="Error",
#         text=f"An error occurred: {error_message}",
#         buttons=[MDRaisedButton(text="OK", on_release=lambda x: error_dialog.dismiss())]
#     )
#     error_dialog.open()




# from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.core.window import Window
# from kivy.properties import StringProperty, NumericProperty
# from kivymd.app import MDApp
# from kivymd.uix.filemanager import MDFileManager
# from kivymd.uix.dialog import MDDialog
# import fitz  # PyMuPDF
# from PIL import Image
# import os

# # PDF Compression Function
# def compress_scanned_pdf(input_pdf_path, output_pdf_path, max_size_kb=300, quality=100, dpi=100):
#     pdf_document = fitz.open(input_pdf_path)
#     new_doc = fitz.open()
#     temp_image_paths = []

#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
#         pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72), colorspace=fitz.csRGB)
#         img_path = f"temp_page_{page_num}.jpg"
#         image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         image.save(img_path, "JPEG", quality=quality)
#         temp_image_paths.append(img_path)

#         rect = fitz.Rect(0, 0, pix.width, pix.height)
#         new_page = new_doc.new_page(width=pix.width, height=pix.height)
#         new_page.insert_image(rect, filename=img_path)

#     new_doc.save(output_pdf_path, deflate=True)
#     new_doc.close()
#     pdf_document.close()

#     for img_path in temp_image_paths:
#         os.remove(img_path)

#     if os.path.getsize(output_pdf_path) > max_size_kb * 1024:
#         print(f"Warning: The output file is still larger than {max_size_kb} KB.")
#     else:
#         print(f"Successfully compressed to under {max_size_kb} KB.")

# # KivyMD App Class
# class PDFCompressorApp(MDApp):
#     selected_file = StringProperty("No file selected")
#     compression_quality = NumericProperty(100)
#     dialog = None


#     def build(self):
#         self.theme_cls.primary_palette = "Blue"
#         self.theme_cls.theme_style = "Light"
#         Window.size = (400, 600)

#         self.file_manager = MDFileManager(
#             exit_manager=self.exit_manager,
#             select_path=self.select_path,
#             ext=[".pdf"]
#         )

#         return Builder.load_string(KV)

#     def show_file_manager(self):
#         self.file_manager.show(os.path.expanduser("~"))  # Opens the home directory

#     def exit_manager(self, *args):
#         self.file_manager.close()

#     def select_path(self, path):
#         self.selected_file = path
#         self.exit_manager()
#         # self.show_dialog(f"Selected: {path}")

#     def compress_pdf(self):
#         if not self.selected_file or self.selected_file == "No file selected":
#             self.show_dialog("Please select a PDF file first.")
#             return

#         output_path = self.selected_file.replace(".pdf", "_compressed.pdf")
#         compress_scanned_pdf(
#             input_pdf_path=self.selected_file,
#             output_pdf_path=output_path,
#             quality=self.compression_quality
#         )
#         self.show_dialog(f"Compression complete! Saved to: {output_path}")


#     # def show_dialog(self, text):
#     #     dialog = MDDialog(title="Info", text=text, size_hint=(0.8, 1))
#     #     dialog.open()

#     def show_dialog(self, text):
#         if self.dialog:
#             self.dialog.dismiss()
#         self.dialog = MDDialog(title="Info", text=text, size_hint=(0.8, 1))
#         self.dialog.open()

# KV = '''
# BoxLayout:
#     orientation: 'vertical'

#     MDTopAppBar:
#         title: "PDF Compressor"
#         elevation: 10

#     MDLabel:
#         text: app.selected_file
#         halign: "center"
#         size_hint_y: None
#         height: dp(40)

#     MDRaisedButton:
#         text: "Select PDF"
#         pos_hint: {"center_x": 0.5}
#         on_release: app.show_file_manager()

#     MDLabel:
#         text: f"Compression Quality: {app.compression_quality}%"
#         halign: "center"

#     MDSlider:
#         min: 10
#         max: 100
#         value: app.compression_quality
#         on_value: app.compression_quality = int(self.value)

#     MDRaisedButton:
#         text: "Compress PDF"
#         pos_hint: {"center_x": 0.5}
#         on_release: app.compress_pdf()
# '''

# if __name__ == "__main__":
#     PDFCompressorApp().run()
