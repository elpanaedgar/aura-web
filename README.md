# AURĀ · web demo

Web publicada en **https://demo.tuwebexpres.com/aura/**.

- `aura/` → lo que se publica (index.html, sw.js, manifest, iconos). Cada cambio en esta carpeta que llegue a `main` se sube solo al servidor por FTP (ver `.github/workflows/deploy.yml`).
- `src/` → código fuente. `python3 src/build.py` genera la página y `python3 src/deploy.py` prepara la carpeta publicable (ejecutar desde `src/`, con salida en `deploy/aura`, copiar luego a `aura/`). Cambiar `VERSION` en `deploy.py` en cada publicación para que el navegador cargue la versión nueva.

## Configuración (una sola vez)
Secretos del repositorio (Settings → Secrets and variables → Actions):
- `FTP_SERVER` — servidor FTP de Webempresa
- `FTP_USERNAME` — cuenta FTP limitada a la carpeta `aura`
- `FTP_PASSWORD` — su contraseña

Las contraseñas solo se guardan en GitHub, nunca en el código.
