# 5. Cómo investigar tu propia Raspberry Pi sin modificarla

[← Scythe](alternativa-scythe.md) · [Índice](README.md) · [Siguiente: fotografías →](fotografias.md)

## Objetivo

Obtener una observación básica del modelo, kernel, temperatura comunicada y estado de throttling. **Este procedimiento no realiza un test de estrés ni modifica GPIO, PWM, alimentación o configuración térmica.** No reproduce por sí solo los ensayos históricos de 2020/2026.

## 1. Comprobación de solo lectura

En una terminal Linux de la Raspberry Pi:

```sh
tr -d '\000' < /proc/device-tree/model; printf '\n'
uname -r
if command -v vcgencmd >/dev/null 2>&1; then
  vcgencmd measure_temp
  vcgencmd get_throttled
fi
```

Los comandos consultan información del sistema. La disponibilidad de `vcgencmd` depende del entorno instalado. Un valor de temperatura aislado no demuestra estabilidad ni calidad de refrigeración.

## 2. Anota el contexto

| Campo | Ejemplo de qué registrar |
| --- | --- |
| Placa y SO | Modelo exacto, kernel |
| Alimentación | Fuente utilizada, sin identificadores privados |
| Refrigeración | Disipador, ventilador, carcasa |
| Entorno | Temperatura ambiente y ubicación general de la prueba |
| Condición de carga | Reposo o carga definida, sin mezclarlas |
| Observación | Hora, temperatura, throttling y advertencias |

## 3. Interpreta con prudencia

- **Temperatura:** depende de carga, ambiente y montaje.
- **Throttling:** revisa si el estado refleja eventos históricos además del instante actual, según la interpretación aplicable a tu equipo.
- **Ruido:** describe primero cuándo aparece; medir dB(A) requiere equipo y protocolo adecuados.
- **Comparación:** conserva constantes todas las condiciones que no quieras estudiar.

## 4. Comparte una reproducción útil

Si abres una issue, incluye modelo, alimentación, refrigeración, versión del sistema, condiciones de medición y resultado observado. **No compartas IP, credenciales, rutas privadas ni fotografías que muestren datos personales.**

Esta guía es observacional: no habilita una intervención eléctrica ni es una validación del prototipo histórico.

[← Scythe](alternativa-scythe.md) · [Índice](README.md) · [Siguiente: fotografías →](fotografias.md)
