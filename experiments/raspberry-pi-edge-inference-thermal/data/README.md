# Datos derivados mínimos

`resumen_sesiones.csv` contiene exclusivamente estadísticos procedentes de los tres resúmenes MAX7. **No** contiene series temporales reconstruidas ni materiales originales. Las columnas `temp_min_c` y `temp_max_c` son mínimos/máximos de cada ventana observada, no de modelos aislados. `observadas` y `previstas` son recuentos de muestras. `integridad_sha_csv=pendiente` indica que los CSV originales todavía no se han cotejado byte a byte con el SHA-256 declarado por cada resumen.

**Fuente:** tres ficheros resumen de la Biblioteca del proyecto, accesibles en fecha de preparación. La integridad de los CSV y la asociación detallada modelo→muestra siguen pendientes. La cadencia nominal de los registros es 5 s; no se publican horas absolutas ni datos privados.
