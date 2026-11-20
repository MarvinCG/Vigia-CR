# Vigía CR

Monitor ciudadano que cada 6 horas busca novedades sobre seguridad pública y cárceles en Costa Rica (Asamblea Legislativa, Sala IV y juzgados, Defensoría/MNPT, noticias y OIJ), marca posibles choques normativos para revisión y publica todo en una web pública con fuentes.

Costo: **₡0**. Usa GitHub Actions (búsqueda programada) y GitHub Pages (web), gratis en repositorios públicos.

## Puesta en marcha (10 minutos)

1. Cree una cuenta en github.com y un repositorio **público** nuevo, por ejemplo `vigia-cr`.
2. Suba todo el contenido de esta carpeta (botón **Add file → Upload files**, o con `git push`). La carpeta `.github` es obligatoria.
3. En el repositorio: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. En **Settings → Actions → General → Workflow permissions**, elija **Read and write permissions** y guarde.
5. Vaya a **Actions → Monitor y publicación → Run workflow** para la primera corrida.
6. La web queda en `https://SU-USUARIO.github.io/vigia-cr/`.

A partir de ahí se actualiza sola cada 6 horas. Para cambiar la frecuencia, edite `cron` en `.github/workflows/monitor.yml`.

## Qué editar

| Archivo | Para qué |
|---|---|
| `scraper/config.py` | Búsquedas, páginas oficiales vigiladas, temas y palabras que marcan "para revisar" |
| `data/contenido.json` | Textos fijos: derechos, fallas legales, impacto, otra postura, qué hacer |
| `site/index.html` | Diseño de la web |

## Reglas de contenido

- Todo dato publicado lleva enlace a su fuente. Sin fuente, no se publica.
- La marca "Para revisar" es automática por palabras clave. **No es una conclusión legal**: alguien debe leer el documento.
- `comparaciones` (preso vs. ciudadano común) está vacío a propósito. Agregue entradas solo con cifras oficiales y fuente para ambos lados, con este formato:
  `{"preso": "...", "ciudadano": "...", "fuente": "...", "url": "https://..."}`
- No publique datos personales de particulares (víctimas, familiares o reos sin condena firme).

## Probar en su computadora

```bash
python3 scraper/monitor.py --fixture   # datos de ejemplo, sin internet
python3 scraper/monitor.py             # búsqueda real
mkdir -p site/data && cp data/*.json site/data/
cd site && python3 -m http.server 8000  # abra http://localhost:8000
```

## Mejoras posibles

- Resúmenes y detección de contradicciones con IA: agregar una clave de API como *secret* del repositorio y un paso que analice los elementos marcados.
- Alertas por correo o Telegram cuando aparezca un fallo de la Sala IV.
- Descargar y leer el texto de PDFs de la Defensoría y la Asamblea.
