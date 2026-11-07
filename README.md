# Una prueba perfecta no demuestra un sistema mejor

## ¿Para qué te puede servir?

Imagina que organizas las inscripciones a un taller. Alguien te pasa una lista de notas en inglés: «Approved», «Not approved», «Approval pending»… Quieres separar las que **parecen confirmadas** de las que **requieren revisión**.

Es tentador escribir una regla sencilla: *si aparece «approved», marca «ALLOW»; si no, «BLOCK»*. Pero ¿qué ocurre con «unapproved» o «approved, but not ready»? Una coincidencia de palabras puede dar por buena una frase que significa lo contrario.

**En este ejercicio no estamos autorizando inscripciones reales.** Usamos frases inventadas para aprender a probar un programa antes de confiar en él.

### ¿Dónde puedes aplicar esta idea?

Si trabajas con software, IA o automatizaciones, puedes reconocer el mismo problema en situaciones como estas:

- **Aplicaciones que incorporan IA:** comprobar si un asistente clasifica *correctamente* consultas ficticias como «urgente» o «normal» antes de aceptar una nueva versión. Puedes **adaptar** `Case` y `score` si tu aplicación devuelve etiquetas con una respuesta esperada inequívoca; aquí no hemos conectado ni evaluado un LLM.
- **Programación de sistemas deterministas:** probar las reglas que interpretan estados como «pendiente», «entregado» o «devuelto», incluyendo negaciones y casos ambiguos. Es el uso **más directo** del evaluador del ejemplo.
- **Pruebas de regresión de aplicaciones:** guardar entradas y resultados esperados para descubrir si una modificación del código estropea comportamientos que antes funcionaban. La prueba real exige ejecutar también la versión modificada.
- **Automatización de documentos y procesos:** diseñar casos sintéticos para comprobar un clasificador de notas de facturas, correos o solicitudes. La lectura de PDFs, los datos de negocio y las integraciones no están incluidos: serían trabajo adicional.
- **Workflows con agentes de IA:** contrastar propuestas de clasificación o estados de un agente con respuestas de referencia, en un entorno de pruebas. **Esto no comprueba permisos, ejecución de herramientas ni seguridad del agente**.

Lo reutilizable hoy es el mecanismo **`Case` + `score`** para funciones que reciben texto y devuelven una etiqueta exacta. En problemas abiertos —por ejemplo, evaluar la creatividad de un texto generado por IA— hace falta diseñar otro evaluador; contar coincidencias de palabras no basta.

### Dos ejemplos cotidianos donde ocurre lo mismo

- **Pedidos online:** «pedido enviado» no significa «pedido entregado»; y «entregado, pero devuelto» tampoco debería contarse como una entrega satisfactoria.
- **Facturas o recibos:** detectar la palabra «pagado» dentro de «no pagado» puede producir un resultado equivocado si ignoras la negación.

Estos son ejemplos para entender el problema, **no sistemas que hayamos probado**. La dificultad compartida es que las palabras por sí solas no representan todo el estado de un proceso.

### ¿Qué vamos a comprobar?

Comparamos dos programas minúsculos escritos en Python:

1. **Versión inicial (*baseline*):** responde siempre `ALLOW` («parece aprobado»).
2. **Versión candidata:** primero busca `not approved` o `pending` y marca `BLOCK`; de lo contrario, si encuentra `approved`, marca `ALLOW`.

Ninguno comprende el significado de las frases. **No hay un modelo de IA detrás:** son reglas deterministas cuyo comportamiento puedes inspeccionar línea por línea.

Primero probamos ambos con **cuatro frases ficticias**. Después, un revisor elige **otras seis frases** para intentar encontrar fallos. No son una muestra aleatoria ni un examen representativo de la vida real.

### El resultado, explicado sin tecnicismos

| Qué probamos | Versión inicial | Versión candidata |
| --- | ---: | ---: |
| 4 frases originales | 2 aciertos de 4 | **4 de 4** |
| 6 frases de desafío | 1 acierto de 6 | **3 de 6** |

Al principio parecía un pleno: `4/4`. Pero con las seis contrapruebas —`3/6`— encontramos **tres errores**.

| Frase de la prueba | Debería marcar | El programa marca | Por qué falla |
| --- | --- | --- | --- |
| `unapproved` | `BLOCK` | `ALLOW` | Contiene las letras de «approved» |
| `Approved, but revoke approval` | `BLOCK` | `ALLOW` | Ignora que la aprobación se revocó |
| `Approved, but not ready` | `BLOCK` | `ALLOW` | Confunde aprobado con preparado |

Las otras tres frases de desafío se clasificaron correctamente. Las seis fueron **diseñadas después para intentar romper la regla**: no constituyen una muestra independiente representativa, ni permiten estimar el porcentaje de aciertos de un sistema real.

**La lección:** que un programa acierte todos los ejemplos que tú preparaste no significa que funcione igual de bien con entradas diferentes.

### Pruébalo en dos minutos

Necesitas **Python 3.10 o superior**, sin instalar librerías adicionales. Guarda juntos `example.py` y `test_example.py` y ejecuta:

```sh
python -B example.py
python -B -m unittest test_example.py -v
```

Deberías obtener estos recuentos: `(2, 4)`, `(4, 4)`, `(1, 6)`, `(3, 6)`. Los tests pasan porque **describen lo que el programa hace**, incluidos sus errores. Pasar los tests no implica que la regla sea segura.

### Reutiliza el evaluador en tu propio proyecto

La parte interesante para reutilizar **no es la regla de aprobación**, que hemos demostrado que falla. Son las piezas `Case` y `score`: sirven para definir ejemplos con un resultado esperado y contar cuántos acierta una función cualquiera que reciba texto.

Por ejemplo, supongamos que quieres **probar una función de clasificación de notas de pedidos** con datos inventados. Crea un archivo `prueba_pedidos.py` junto a `example.py`, pega lo siguiente y ejecútalo.

```python
from example import Case, score

casos = (
    Case("Pedido entregado", "LISTO"),
    Case("Pedido pendiente", "REVISAR"),
    Case("Pedido entregado pero devuelto", "REVISAR"),
    Case("Pedido enviado", "REVISAR"),
)

def clasificar_nota(texto):
    # Ejemplo didáctico: sólo reconoce una frase exacta.
    return "LISTO" if texto.strip().lower() == "pedido entregado" else "REVISAR"

print(score(clasificar_nota, casos))  # (4, 4) en estos cuatro casos
```

Ejecuta `python -B prueba_pedidos.py`. Si cambias la función o agregas frases ambiguas, podrás repetir la misma prueba sin preparar una herramienta nueva. **El resultado `(4, 4)` sólo describe esos cuatro ejemplos inventados**, no demuestra que el clasificador pueda gestionar pedidos reales.

Si luego trabajas con un LLM, puedes reutilizar este **esquema de evaluación** para salidas deterministas, siempre que definas criterios adecuados; no basta con usar el mismo contador para evaluar creatividad, razonamiento o seguridad de una IA.

### Qué hacer antes de aplicar esta idea de verdad

- Define qué significa acertar **antes** de mirar los resultados.
- Separa los casos con los que desarrollas de los que empleas para comprobar cambios.
- Añade negaciones, ambigüedades y ejemplos que contradigan tus suposiciones.
- Anota fallos y condiciones: no informes sólo del número de aciertos.
- En un proceso real, usa **estados estructurados** y controles apropiados; no conviertas coincidencias de texto en permisos ni decisiones automáticas.

**No utilizar este código** para autorizar acciones, mover dinero, procesar datos personales o tomar decisiones de seguridad. Tampoco hemos probado un LLM: es un ejercicio didáctico sobre cómo evaluar una función.

### Procedencia y licencias

Ejercicio sintético de clasificación mediante reglas deterministas, preparado con asistencia de IA y revisado con contrapruebas. No se utilizan datos reales ni modelos LLM.

El código (`example.py`, `test_example.py`) se ofrece bajo MIT y los textos explicativos bajo CC BY 4.0. Consulta `LICENSE`, `CONTENT_LICENSE.md` y `PROVENANCE.md`.

### ¿Qué podríamos aprender después?

Como ejercicio, prueba negaciones distintas, errores ortográficos y frases en otros idiomas. Pregúntate qué cambiarías en el programa y qué datos necesitarías para evaluar esa nueva versión de forma independiente. **Estas ampliaciones no se han ejecutado en el experimento actual.**

---
**Status:** educational experiment; not a production guarantee.
**Licenses:** MIT (code); CC BY 4.0 (documentation).
