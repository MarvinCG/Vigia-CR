"""Configuración del monitor: qué buscar y cómo clasificarlo.

Edite estas listas para ajustar la búsqueda. No hace falta tocar el resto del código.
"""

# Búsquedas en Google News (RSS público, gratis, sin clave).
# Cada entrada: (categoría, consulta)
QUERIES = [
    # Asamblea Legislativa
    ("asamblea", "Asamblea Legislativa proyecto de ley seguridad crimen organizado"),
    ("asamblea", "Comisión de Seguridad y Narcotráfico expediente"),
    ("asamblea", "ley ejecución de la pena Costa Rica"),
    ("asamblea", "reforma Código Procesal Penal prisión preventiva Costa Rica"),
    # Sala IV y juzgados
    ("tribunales", "Sala Constitucional privados de libertad"),
    ("tribunales", "Sala IV alta contención recurso de amparo"),
    ("tribunales", "Juzgado de Ejecución de la Pena ordena"),
    ("tribunales", "Sala IV acción de inconstitucionalidad reglamento penitenciario"),
    # Defensoría / MNPT
    ("defensoria", "Defensoría de los Habitantes privados de libertad"),
    ("defensoria", "Mecanismo Nacional de Prevención de la Tortura informe"),
    ("defensoria", "CACCO Centro de Alta Contención"),
    # Noticias y OIJ
    ("noticias", "OIJ homicidios Costa Rica"),
    ("noticias", "Ministerio de Justicia y Paz cárceles Costa Rica"),
    ("noticias", "delito ordenado desde la cárcel Costa Rica"),
    ("noticias", "celulares decomisados cárcel Costa Rica"),
]

# Páginas oficiales que se revisan directamente para detectar cambios
# (si cambian, se registra un aviso con enlace).
WATCH_PAGES = [
    ("defensoria", "Defensoría - comunicados", "https://www.dhr.go.cr/"),
    ("tribunales", "Poder Judicial - noticias", "https://pj.poder-judicial.go.cr/"),
    ("asamblea", "Asamblea Legislativa - inicio", "https://www.asamblea.go.cr/"),
]

# Temas: palabra clave -> etiqueta
TOPICS = {
    "llamada": "Llamadas", "teléfono": "Llamadas", "telefon": "Llamadas", "celular": "Celulares",
    "visita": "Visitas", "conyugal": "Visitas", "íntima": "Visitas",
    "encomienda": "Encomiendas",
    "prisión preventiva": "Prisión preventiva", "medidas cautelares": "Prisión preventiva",
    "beneficio": "Beneficios penitenciarios", "año carcelario": "Beneficios penitenciarios",
    "libertad condicional": "Beneficios penitenciarios", "descuento": "Beneficios penitenciarios",
    "reincid": "Reincidencia",
    "alta contención": "Alta contención", "máxima seguridad": "Alta contención", "cacco": "Alta contención",
    "homicidio": "Homicidios", "sicariato": "Sicariato",
    "extradición": "Extradición",
    "lavado": "Lavado de dinero",
    "víctima": "Derechos de víctimas",
}

# Señales de posible contradicción o choque normativo.
# Se marcan para revisión humana: NO son conclusiones automáticas.
CONTRADICTION_SIGNALS = [
    "contradice", "contradicción", "desacata", "mayor rango", "rango normativo",
    "jerarquía", "ilegal", "inconstitucional", "anula", "deja sin efecto",
    "ordena restablecer", "restablecer", "con lugar", "sin lugar", "rechaza",
    "vacío legal", "laguna", "ambigüedad", "no acatará", "incumpl", "choca",
    "reglamento", "circular", "directriz", "decreto",
]

MAX_ITEMS = 1500       # cuántos elementos guardar como máximo
MAX_PER_QUERY = 15     # resultados por búsqueda en cada corrida
