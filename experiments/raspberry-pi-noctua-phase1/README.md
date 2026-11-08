# Raspberry Pi 4 + Noctua: ¿puede refrigerar bien y seguir sonando?

**Artículo técnico — edición pública textual.** El montaje fotográfico corresponde a mayo de 2020; las observaciones térmicas y acústicas descritas pertenecen a otras pruebas de octubre-noviembre de 2026. Las imágenes de archivo todavía no están incorporadas a esta edición.

## El problema real

La primera pregunta no era cómo programar un ventilador, sino cómo mantener una Raspberry Pi 4 funcionando, estable y sin ruido molesto. Montamos un **Noctua NF-A4x20 5V de tres hilos**, disipadores de cobre y una tapa adaptada artesanalmente. El archivo fotográfico de esa etapa documenta la adaptación mecánica; las imágenes permanecen pendientes de revisión para su incorporación pública.

La tapa adaptada alojaba el ventilador junto a la carcasa de la Raspberry Pi. No hay fotografía incorporada a esta edición.

Noctua es una marca reconocida por sus ventiladores silenciosos, pero una buena especificación de catálogo no prueba el ruido del conjunto real. El mueble, la carcasa, la alimentación, las resonancias y la posición del micrófono también importan.

## Montaje y limitaciones mecánicas

El prototipo incluía una adaptación interior y un perfil condicionado por el espacio disponible. Esta solución artesanal permitía ensayar un ventilador concreto; no es una guía de montaje certificada, ni documenta todavía un esquema eléctrico reproducible.

El ventilador instalado era **de 3 pines**: la línea de tacómetro no es una entrada PWM dedicada. No se comprobó control PWM continuo del Noctua en esta etapa.

## Primero, alimentación y temperatura

Las pruebas históricas comunicaron subtensión con una fuente alternativa. Con la fuente original se registró una prueba de 10 minutos bajo carga y una temperatura máxima **reportada** de **51,6 °C** sin throttling en las muestras indicadas. También se comunicó un baseline F3 de siete días.

**Advertencia de procedencia:** el archivo primario F3 no está disponible en esta revisión. Las cifras anteriores **no** deben presentarse como auditadas o reproducidas ahora.

## Después, el ruido: ¿qué decía el espectro?

Reanalizamos tres audios originales: grabación de octubre con desplazamiento aproximado de 1 m a 1 cm y regreso; dos grabaciones de noviembre históricamente atribuidas a unos 5 cm y 1 m. Se utilizó ventana Hann de 4 s, solapamiento del 50 % y mediana de espectros.

| Audio | Banda baja | Banda próxima a 7× | Banda próxima a 16× |
| --- | ---: | ---: | ---: |
| Octubre | **91,00 Hz** | **637,25 Hz** | **1.456,50 Hz** |
| Noviembre, cercano* | **87,50 Hz** | **612,25 Hz** | **1.399,50 Hz** |
| Noviembre, lejano* | **87,25 Hz** | **611,25 Hz** | **1.397,75 Hz** |

*La atribución de distancia es histórica; no se mide a partir del audio.*

Los picos son compatibles con una fuente periódica y sus armónicos. **No prueban RPM, no identifican la pieza causante ni indican dB(A)**. La grabación con móvil no equivale a un sonómetro calibrado. No hay una comparación acústica equivalente con el ventilador posterior Armor Lite.

## ¿Por qué no una alternativa de disipador mayor?

En octubre de 2026 evaluamos también una alternativa **Scythe** con heatpipes y fijaciones. **No era el montaje Noctua de 2020.** El estudio mecánico con una regla sirvió para considerar volumen, interferencias y costes de integración que no siempre se aprecian en las fichas técnicas.

Las fotografías de la alternativa Scythe permanecen en revisión y aún no están publicadas.

## Qué puedes aprovechar

En tu Raspberry Pi puedes comenzar con observaciones **sin alterar el hardware**:

```sh
tr -d '\000' < /proc/device-tree/model; printf '\n'
uname -r
if command -v vcgencmd >/dev/null 2>&1; then
  vcgencmd measure_temp
  vcgencmd get_throttled
fi
```

Registra las condiciones, separa problemas de alimentación de ruido y temperatura, y conserva los audios originales si quieres estudiar espectros. Si encuentras un error o reproduces el fenómeno, abre una issue indicando modelo, montaje, alimentación y protocolo de medida (sin datos privados).

**Estado de la investigación:** inventario de fotografías originales documentado en revisión privada, con imágenes todavía no incorporadas; acústica reanalizada en la revisión anterior; fuente primaria de F3 pendiente; sin medición SPL calibrada ni publicación de audios brutos.

**Fuentes:** [Raspberry Pi documentación oficial](https://www.raspberrypi.com/documentation/computers/os.html) · [Noctua NF-A4x20 5V](https://www.noctua.at/en/products/nf-a4x20-5v/specifications).


## Alcance editorial y reutilización

Esta edición pública contiene únicamente texto técnico. No incorpora fotografías, archivos de audio, telemetría bruta, documentos de control interno ni materiales de otros proyectos. Los resultados históricos señalados como *reportados* no constituyen verificaciones independientes.

Las condiciones de reutilización de este artículo específico están pendientes de determinación por su titular. La licencia [CONTENT_LICENSE.md](../../CONTENT_LICENSE.md) existente identifica expresamente otros materiales del repositorio y no debe interpretarse como una autorización automática sobre este artículo o fotografías futuras.
