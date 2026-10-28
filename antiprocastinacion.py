import os
import sys
import random
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import pygame
import pygetwindow as gw  # Detecta la ventana activa en Windows sin extensiones

# Obtener rutas absolutas automáticas de los archivos multimedia
# Si se ejecuta como .exe empaquetado con PyInstaller, buscar en _MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO_PATH = os.path.join(BASE_DIR, "gato_chancano.mp4")
AUDIO_PATH = os.path.join(BASE_DIR, "gato_audio.mp3")

# Lista de palabras clave que activarán el castigo al aparecer en el navegador o apps
SITIOS_PROHIBIDOS = [
    "youtube", "facebook", "tiktok", "instagram", 
    "twitter", "x.com", "reddit", "twitch", "discord"
]

# Inicializar sistema de audio
pygame.mixer.init()
if os.path.exists(AUDIO_PATH):
    pygame.mixer.music.load(AUDIO_PATH)
else:
    print(f"⚠️ Advertencia: No se encontró el audio en {AUDIO_PATH}")


class VentanaCastigo:
    def __init__(self, root):
        self.root = root
        self.root.title("¡AntiProcastinador - Gato Chancano!")

        # Bloquear el botón de cierre (X) de la ventana principal
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.win_width = int(screen_width * 0.4)
        self.win_height = int(screen_height * 0.4)
        self.pos_x = int((screen_width - self.win_width) / 2)
        self.pos_y = int((screen_height - self.win_height) / 2)

        self.root.geometry(f"{self.win_width}x{self.win_height}+{self.pos_x}+{self.pos_y}")
        self.root.attributes('-topmost', True)
        self.root.configure(background='black')

        self.label = tk.Label(root, background='black')
        self.label.pack(expand=True, fill='both')

        # Cargar video con OpenCV
        self.cap = cv2.VideoCapture(VIDEO_PATH)

        self.aux_windows = []
        self.is_visible = False
        self.timer_id = None

        # Mantener la ventana oculta al iniciar el programa
        self.root.withdraw()

        # Iniciar los bucles de renderizado de video y monitoreo de ventanas
        self.update_frame()
        self.verificar_ventanas_activas()

    def mostrar_ventana(self):
        if not self.is_visible:
            self.is_visible = True
            try:
                pygame.mixer.music.play(-1) # Audio en bucle infinito
            except Exception as e:
                print(f"Error al reproducir audio: {e}")
                
            self.root.deiconify()
            self.root.lift()
            self.root.attributes('-topmost', True)

            # Iniciar el temporizador para el ejército de gatos
            self.programar_multiplicacion()

    def ocultar_ventana(self):
        if self.is_visible:
            self.is_visible = False
            try:
                pygame.mixer.music.stop()
            except:
                pass
            self.root.withdraw()

            # Cancelar el temporizador activo
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

            # Destruir instantáneamente todas las ventanas del ejército de gatos
            for win in self.aux_windows:
                try:
                    win.destroy()
                except:
                    pass
            self.aux_windows.clear()

    def programar_multiplicacion(self):
        # Configurado a 10 segundos (10000 milisegundos)
        if self.is_visible:
            self.timer_id = self.root.after(10000, self.multiplicar_gato)

    def multiplicar_gato(self):
        # 🛡️ LÍMITE DE SEGURIDAD: Solo multiplica si es visible Y hay menos de 10 ventanas extra.
        # Esto evita por completo cualquier trabón o consumo excesivo de memoria si se deja abierto horas.
        if self.is_visible and len(self.aux_windows) < 10:
            extra_win = tk.Toplevel(self.root)
            extra_win.title("¡Ejército de Gatos Activo!")
            
            offset_x = random.randint(-150, 150)
            offset_y = random.randint(-100, 100)
            
            ew, eh = 300, 120
            px = max(50, self.pos_x + offset_x)
            py = max(50, self.pos_y + offset_y)

            extra_win.geometry(f"{ew}x{eh}+{px}+{py}")
            extra_win.attributes('-topmost', True)
            extra_win.protocol("WM_DELETE_WINDOW", lambda: None)
            extra_win.configure(background="#1a1a1a")

            lbl = tk.Label(
                extra_win, 
                text="🚨 ¡Aún sigues procrastinando!\nCierra la pestaña prohibida\npara calmar a los gatos.", 
                fg="#ff4444", 
                bg="#1a1a1a", 
                font=("Arial", 10, "bold"),
                justify="center"
            )
            lbl.pack(expand=True, pady=10)

            self.aux_windows.append(extra_win)
            self.programar_multiplicacion()

    def update_frame(self):
        """Bucle continuo para renderizar el video del gato en movimiento"""
        if self.is_visible:
            current_geo = self.root.geometry().split('+')[0]
            self.root.geometry(f"{current_geo}+{self.pos_x}+{self.pos_y}")

            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                image = image.resize((self.win_width, self.win_height), Image.Resampling.LANCZOS)

                self.photo = ImageTk.PhotoImage(image)
                self.label.config(image=self.photo)

        self.root.after(30, self.update_frame)

    def verificar_ventanas_activas(self):
        """Vigila cada medio segundo qué ventana tiene el foco activo en Windows"""
        try:
            ventana_activa = gw.getActiveWindow()
            if ventana_activa and ventana_activa.title:
                titulo_lower = ventana_activa.title.lower()

                # Evitar que el programa se detecte a sí mismo y entre en bucle
                if "antiprocastinador" not in titulo_lower and "ejército de gatos" not in titulo_lower:
                    # Comprobar si hay alguna palabra prohibida en la ventana actual
                    debe_bloquear = any(sitio in titulo_lower for sitio in SITIOS_PROHIBIDOS)

                    if debe_bloquear:
                        if not self.is_visible:
                            self.mostrar_ventana()
                    else:
                        if self.is_visible:
                            self.ocultar_ventana()
        except Exception as e:
            pass

        # Chequear de nuevo en 500 milisegundos (0.5 segundos)
        self.root.after(500, self.verificar_ventanas_activas)


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaCastigo(root)
    root.mainloop()