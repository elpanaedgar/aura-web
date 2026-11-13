# AURĀ · web demo

Web publicada en **https://demo.tuwebexpres.com/aura/**.

- `aura/` → lo que se publica (index.html, sw.js, manifest, iconos). Cada cambio en esta carpeta que llegue a `main` avisa al servidor, y `aura/actualizar.php` descarga la versión nueva desde GitHub (sin FTP). `aura/archivos.txt` es la lista de archivos que se descargan.
- `src/` → código fuente. `python3 src/build.py` genera la página y `python3 src/deploy.py` prepara la carpeta publicable (ejecutar desde `src/`, con salida en `deploy/aura`, copiar luego a `aura/`). Cambiar `VERSION` en `deploy.py` en cada publicación para que el navegador cargue la versión nueva.

## Configuración (una sola vez)
1. El repositorio tiene que ser **público** (el servidor descarga los archivos sin contraseña).
2. Subir `aura/actualizar.php` a la carpeta `demo.tuwebexpres.com/aura` del servidor.

Después, cada cambio en `aura/` se publica solo. Para forzar una actualización: Actions → «Publicar AURĀ…» → Run workflow.
