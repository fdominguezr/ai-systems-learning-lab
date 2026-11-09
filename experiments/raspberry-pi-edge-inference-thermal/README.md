# ¿Cuánto se calienta una Raspberry Pi ejecutando IA?

*Lo que descubrimos al medirla cada cinco segundos.*

**Un pico inesperado, una recuperación térmica y una lección sobre lo que nuestros instrumentos pueden —y no pueden— demostrar.**

Una Raspberry Pi 4B puede ejecutar modelos de lenguaje localmente sin una GPU dedicada. Pero, ¿cómo responde su temperatura cuando se mantiene trabajando durante horas? Para averiguarlo registramos la temperatura durante tres observaciones: una con baja actividad y dos con cargas de inferencia de distinta duración.

![Carcasa de Raspberry Pi 4 junto a un montaje artesanal Noctua](figures/raspberry-pi-noctua-historico-2020.jpg)

*Fotografía histórica del proyecto de refrigeración Noctua, tomada en **2020**. Muestra la familia de hardware utilizada en la serie, **no** acredita que ese ventilador estuviera instalado durante las pruebas de inferencia de 2026.*

## Lee la serie

| Página | Qué descubrirás |
| --- | --- |
| [1. Hardware y modelos](01-hardware-modelos.md) | Cómo funciona la inferencia en CPU y qué tamaños probamos |
| [2. Cómo medimos](02-como-medimos.md) | Un registro cada cinco segundos, controles puntuales y cobertura |
| [3. Primera prueba: calentamiento y recuperación](03-primera-prueba.md) | Casi cuatro horas de inferencia y descenso térmico posterior |
| [4. Segunda prueba: un pico inesperado](04-segunda-prueba.md) | Diferencia entre instrumentos y el límite del registro |
| [5. ¿Calienta más un modelo grande?](05-modelos-y-temperatura.md) | Qué muestran los máximos y por qué no prueban eficiencia |
| [6. Qué aprendimos y siguiente experimento](06-conclusiones.md) | Resumen y preguntas para reproducirlo |

![Comparación de tamaños nominales de los modelos evaluados](figures/modelos_parametros.png)

*Los parámetros muestran el tamaño nominal de un modelo, no su temperatura, velocidad ni memoria real utilizada.*

## Dónde encaja este artículo

Continuamos la investigación sobre refrigeración y ruido iniciada en [Raspberry Pi 4 + Noctua: montaje, alimentación y acústica](../raspberry-pi-noctua-phase1/README.md). **No asumimos que la configuración de ventilación de aquellas fotografías de 2020 estuviera presente en las sesiones térmicas actuales.**

**Alcance de la publicación:** análisis exploratorio, no benchmark controlado. Los tres resúmenes de telemetría están disponibles, pero los CSV originales y los eventos de aplicación todavía no han podido verificarse por SHA-256 en esta preparación; por ello las figuras no simulan una curva continua cuando faltan sus muestras.
