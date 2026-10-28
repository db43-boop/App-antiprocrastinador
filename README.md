# AntiProcastinador - Guía de Instalación

Programa que muestra ventanas del "Gato Chancano" cuando detecta que estás en una red social (YouTube, TikTok, Instagram, Twitter/X, Discord). Presionando "Sí" o "Obvio" se cierran las ventanas del castigo y la pestaña de la red social.

---

## 📁 ¿Qué paquete necesita la persona?

Para que el programa funcione correctamente, enviá **todo el contenido de la carpeta** o al menos:

```
AntiProcastinador/
├── AntiProcastinador.exe   ← el ejecutable (obligatorio)
├── gato_audio.mp3          ← audio que reproduce el castigo
├── gato_chancano.mp4       ← video del gato que se muestra
└── extension/              ← extensión de Chrome (si querés usar el modo "pestañas de Chrome")
```

> Nota: puedes borrar `build/`, `dist/`, `build_fixed/`, `AntiProcastinador.spec` y `__pycache__` antes de compartir.

---

## 🔧 Modo A: Con extensión de Chrome (modo completo)

El programa detecta qué pestañas abres dentro de **Google Chrome** (YouTube, TikTok, Instagram, Twitter, Discord, etc.) y los va siguiendo por `localhost:5000`.

### Instalación (3 pasos)

#### 1. Ejecutar el programa
Hacé doble clic en `AntiProcastinador.exe`.  
Si Windows Defender o tu antivirus avisa que es desconocido, elegí **Más información → Ejecutar de todas formas** (es un falso positivo común de programas hechos con PyInstaller).

#### 2. Instalar la extensión en Chrome
1. Abrí Chrome y andá a `chrome://extensions`.
2. Activa **Modo desarrollador** (interruptor arriba a la derecha).
3. Clic en **Cargar sin empaquetado**.
4. Seleccioná la carpeta llamada `extension` que viene con este programa.

#### 3. Probarlo
Abrí una red social (YouTube, TikTok, Instagram, etc.).  
Deberían aparecer las ventanas del gato. Presioná **Sí** u **Obvio** para cerrarlas y la pestaña de la red social.

> ❌ Si no cargás la extensión, el programa **aún funciona**, pero solo detecta ventanas del escritorio (ventana activa de Windows). No notará las pestañas específicas de Chrome.

---

## 🪟 Modo B: Sin extensión de Chrome (modo mínimo)

Si **no** querés instalar la extensión, el programa funciona igual, pero detecta la **ventana activa de Windows** (no las pestañas de Chrome). Esto quiere decir:

- ✅ Detecta y castiga ventanas de: `cmd.exe`, `feh.exe`, `mpv.exe`, etc.
- ❌ No detecta automáticamente `youtube.com`, `tiktok.com`, etc. dentro de Chrome (solo "chrome.exe" como ventana).
- ⚡ El .exe no hace referencia a `localhost:5000` ni requiere que esté corriendo el servidor de la extensión.

### Cómo verificar que funciona en modo mínimo
Abre una ventana de **PowerShell** (u otro terminal) y ejecuta el `.exe`. En unos segundos verás la ventana del gato. Presiona **Sí** o **Obvio** para cerrarlo.

---

## 💡 Resumen rápido

| ¿Qué querés hacer? | ¿Necesitás extensión? |
|---|---|
| Detectar pestañas de Chrome (YouTube, TikTok, etc.) | ✅ Sí, carga la extension |
| Detectar cualquier ventana activa de Windows | ❌ No, no necesitás extension |
| Fallback si el antivirus bloquea el .exe | ✅ Sí, seguir el paso 1 |

---

## Uso

- El programa corre en segundo plano y usa `localhost:5000` para hablar con la extensión (si está instalada).
- Mientras haya una pestaña de red social abierta, aparecen ventanas del gato cada 10 segundos.
- Cerrá la pestaña de la red social manualmente o usá los botones para que el programa lo haga por vos.

---

## Solución de problemas

| Problema | Solución |
|----------|----------|
| No aparecen ventanas | Verificá que el `.exe` esté corriendo y que la extensión esté cargada en Chrome (modo completo). Si usás modo mínimo, abrí cualquier terminal o ventana de programa. |
| Las ventanas no se cierran al presionar "Sí"/"Obvio" | Reiniciá el `.exe` y recargá la extensión en `chrome://extensions`. |
| Antivirus bloquea el `.exe` | Agregalo a las exclusiones o ejecutolo como administrador. |
| Tengo que matar el proceso desde el Administrador de Tareas | Actualizá a esta versión (corrige el cierre de ventanas al cerrar la pestaña). |

---

## Compartir con otra persona

Enviá el archivo `.exe` **y** la carpeta `extension` si querés el modo completo.  
Si la persona solo va a usar el modo mínimo (detección de ventanas de escritorio), solo enviale el `.exe` y los archivos multimedia (`gato_audio.mp3`, `gato_chancano.mp4`).

---
