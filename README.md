# Apuntes web

Sitio de apuntes de economía y econometría de Mario Peñaloza, hecho con [Quarto](https://quarto.org): notas en `.qmd` (Markdown con LaTeX y código), ecuaciones con MathJax y publicación automática en GitHub Pages. Es el mismo esquema que usa el libro [Macroeconometría Aplicada con Python](https://renatovassallo.github.io/MacroeconometricsBook/chapters/00-preliminares.html).

## Ver el sitio en tu computadora

Requiere [uv](https://docs.astral.sh/uv/). En PowerShell, desde esta carpeta:

```powershell
uv sync
uv run quarto preview
```

`quarto preview` abre el navegador y recarga la página cada vez que guardas un `.qmd`. Para compilar sin abrir nada: `uv run quarto render` (la salida queda en `_site/`).

## Estructura

| Ruta | Contenido |
|---|---|
| `_quarto.yml` | Configuración: navegación, tema, MathJax, numeración, bibliografía |
| `index.qmd`, `sobre-mi.qmd` | Portada y perfil académico |
| `cursos/<curso>/` | Una carpeta por curso, con `index.qmd` y una nota `.qmd` por tema |
| `material/` | Presentaciones y guías descargables |
| `assets/` | Estilos (`estilo.scss`), macros de LaTeX, estilo de citas APA 7 y cabecera de seguridad |
| `references.bib` | Bibliografía en BibTeX |
| `_freeze/` | Resultados de código ya ejecutado (se versiona a propósito) |
| `docs/componentes.md` | Sintaxis de teoremas, ecuaciones, código, citas y soluciones |
| `scripts/tex_a_qmd.sh` | Borrador de `.qmd` a partir de un `.tex` existente (con pandoc) |
| `.github/workflows/` | `publish.yml` publica al hacer push a `main`; `revisar.yml` compila cada PR |

La nota de `cursos/econometria-3/17-modelo-de-nivel-local.qmd` es el piloto: muestra todos los componentes ya renderizados.

## Cómo se trabaja

1. Se crea o se edita un `.qmd` en la carpeta del curso y se agrega a la barra lateral en `_quarto.yml`.
2. Para pedir cambios, se señala el archivo y la sección ("reescribe la demostración del teorema 1 con más intuición"); solo se edita ese fragmento, sin regenerar el documento entero.
3. Los cambios a mano se hacen en cualquier editor y se ven en vivo con `quarto preview`; el diff de Git muestra qué se tocó.
4. Se compila antes de subir. Con un push a `main`, GitHub Actions publica el sitio.
5. Una nota con `draft: true` en su encabezado no se publica.

Los `.tex` existentes se convierten con `scripts/tex_a_qmd.sh`; el resultado se revisa a mano. Stata, EViews y Matlab no se ejecutan en la nube: se corren en local y se incrustan sus tablas y figuras.

## Ramas

| Rama | Uso |
|---|---|
| `main` | Producción. Lo que está aquí se publica. Protegida: solo entra por pull request con la compilación en verde |
| `nota/<curso>-<tema>` | Una rama por nota o grupo de cambios (por ejemplo `nota/econometria-3-kalman-general`). Se abre un pull request hacia `main`, que ejecuta `revisar.yml` |


## Diseño, imágenes y enlaces

- **Paleta y tipografía.** Los colores son los de las presentaciones Beamer (azul marino `#000066`, verde azulado `#006666`, azul polvo `#5b84a6`, fondo suave `#f5f5f7`); las tipografías son Source Serif 4 para el texto y Source Sans 3 para la interfaz, alojadas en `assets/fonts/` (licencia SIL OFL) para no depender de servidores externos. Hay modo claro y oscuro. Los estilos están en `assets/estilo.scss` y `assets/estilo-oscuro.scss`.
- **Escudo de la UNMSM.** Está en la barra superior y como ícono de pestaña (`assets/img/unmsm-escudo.png`, tomado de Wikimedia Commons, donde figura como dominio público).
- **Tu foto.** La portada usa hoy una silueta (`assets/img/foto-placeholder.svg`). Para poner tu foto, guarda un cuadrado de 800 por 800 píxeles o más como `assets/img/foto.jpg` y cambia el nombre del archivo en `index.qmd`.
- **Iconos y enlaces.** LinkedIn, GitHub y correo aparecen en la barra superior, en la portada y en el pie. El enlace de GitHub apunta a tu perfil `Mario-P-Antayhua`.
- **Google Drive.** Se puede enlazar una carpeta pública de Drive con un botón o un enlace normal en `material/index.qmd`. No se incrusta dentro de la página, porque la política de seguridad bloquea contenido de otros sitios y eso protege a los visitantes. Falta el enlace que quieras publicar.
- **Extensiones de terceros.** No se instaló ninguna extensión de Quarto ni complemento externo: ejecutan código durante la compilación y amplían la superficie de ataque. Todo lo usado viene incluido en Quarto (ventana ampliada de figuras, iconos de Bootstrap, listados de notas, modo oscuro, búsqueda).

## Dirección web

El sitio se publica desde el repositorio `Mario-P-Antayhua.github.io`, de modo que su dirección es `https://mario-p-antayhua.github.io/`. Para una dirección aún más corta, como `mariopenaloza.com`, se compra un dominio y se asocia en Settings, Pages, Custom domain.

## Seguridad

Un sitio estático no tiene servidor propio, base de datos ni formularios, de modo que la superficie de ataque se reduce a la cuenta de GitHub, la cadena de compilación y lo que se publica. Qué está resuelto en el código y qué se configura en GitHub:

**En el código**

- Cabecera `Content-Security-Policy` por `<meta>` (`assets/cabecera.html`): solo se cargan scripts del propio sitio y de `cdn.jsdelivr.net` (MathJax), sin objetos incrustados, formularios ni base alterna. Los encabezados HTTP `frame-ancestors`, `X-Frame-Options` y HSTS no se pueden fijar desde GitHub Pages.
- Las tipografías están alojadas en el propio sitio; el único script de terceros es MathJax. El polyfill de `cdnjs` que Quarto añade queda bloqueado por la política y no se necesita en navegadores actuales.
- Workflows con `permissions: contents: read` por defecto, `persist-credentials: false` en el checkout y permisos de despliegue solo en el trabajo que publica. Dependabot actualiza acciones y dependencias.
- Entorno de Python fijado con `uv.lock` y `uv sync --locked`.
- `.gitignore` excluye `.env`, claves y archivos locales.

**En GitHub (lista de verificación al crear el repositorio)**

1. Autenticación en dos pasos con passkey o app en la cuenta; revisar sesiones y claves SSH.
2. Protección de `main`: exigir pull request y la verificación `compilar`, bloquear force-push y borrado.
3. Activar secret scanning con push protection, alertas de Dependabot y code scanning si el plan lo permite.
4. En Settings, Actions: permisos por defecto de solo lectura, no ejecutar workflows de forks sin aprobación y limitar las acciones permitidas a las de GitHub y a verificadas.
5. En Pages: fuente "GitHub Actions" y "Enforce HTTPS" activado.
6. No subir datos personales, notas de alumnos, microdatos (ENAHO, Analitika) ni credenciales.

**Pendientes de endurecimiento**

- Fijar cada acción por SHA de commit en lugar de por versión (hoy usan etiquetas `@v4`); Dependabot mantiene los SHA al día.
- Servir MathJax desde el propio sitio para eliminar la dependencia del CDN.
- Si algún día se quiere acceso restringido o cabeceras HTTP propias, poner el sitio detrás de Cloudflare (Access y reglas de cabeceras).

Un sitio de GitHub Pages es público aunque el repositorio sea privado (salvo en planes Enterprise). Todo lo que se compila es público.
