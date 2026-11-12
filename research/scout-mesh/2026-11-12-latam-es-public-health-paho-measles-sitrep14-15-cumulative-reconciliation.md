# OPS/OMS sarampión 2026 — conciliación de informes #14 y #15 (revisión pública, NO distribuida)

- **Fecha de revisión:** 2026-11-12 UTC.
- **Celda Scout:** `latam-es-public-health` (Américas, español, vigilancia de salud pública).
- **Tipo:** verificación de series temporales / prevención de interpretaciones erróneas; no se detecta error atribuible a la OPS.
- **Estado:** comparación de textos de resúmenes publicados en el dominio oficial, pendiente de corroboración del PDF/visualización original en navegador sin caché.
- **Autoridad:** OPS/OMS; el proyecto no sustituye recomendaciones nacionales de vacunación ni hace vigilancia epidemiológica independiente.

## Fuentes primarias

1. OPS/OMS, [Informe de situación #14: Sarampión en la Región de las Américas, 22 oct 2026](https://www.paho.org/es/documentos/informe-situacion-14-sarampion-region-americas-22-octubre-2026). Datos acumulados SE 1–41, cierre 17 oct.
2. OPS/OMS, [Informe de situación #15: Sarampión en la Región de las Américas, 6 nov 2026](https://www.paho.org/es/documentos/informe-situacion-15-sarampion-region-americas-6-noviembre-2026). Datos acumulados SE 1–43, cierre 31 oct.
3. OPS/OMS, [Portal de brote multipaís de sarampión 2026](https://www.paho.org/es/brote-multi-pais-sarampion-2026), que enlaza ambos informes y clasifica el riesgo regional general como «Muy Alto».

**Método y límite de acceso:** Los resúmenes textuales de #14 y #15 fueron recuperados en resultados indexados del dominio oficial `paho.org` el 12 nov; las aperturas directas del lector web a ambas páginas devolvieron HTTP 403. Por tanto, esto es una conciliación de contenido oficial indexado, **no** verificación de PDF íntegro ni lectura en navegador ordinario sin caché. Las fechas de corte son las declaradas en los resúmenes, no la fecha de consulta.

## Comparación verificable

| Indicador | #14 (hasta SE 41, 17 oct) | #15 (hasta SE 43, 31 oct) | Diferencia entre cortes |
|---|---:|---:|---:|
| Casos confirmados acumulados | 56.753 | 57.666 | +913 |
| Países/territorios notificantes | 17 | 17 | 0 |
| Defunciones acumuladas notificadas | 81 | 81 | 0 |
| Guatemala, acumulado | 34.535 | 34.748 | +213 |
| México, acumulado | 13.691 | 13.761 | +70 |
| Estados Unidos, acumulado | 4.410 | 4.852 | +442 |
| Perú, acumulado | 2.698 | 2.862 | +164 |
| Canadá, acumulado | 1.124 | 1.126 | +2 |

**Control aritmético:** 57.666 − 56.753 = **913**. Las variaciones de los cinco países citados suman **891**; quedan **22** de diferencia neta entre los demás países/territorios, sin atribución país por país en esta nota. El recuento de defunciones no cambió entre estos dos cortes, lo cual **no** demuestra ausencia de muertes durante el intervalo (pueden existir demoras y revisiones).

## No confundir «casos nuevos» con variación del acumulado

- El informe #14 describe **643** casos nuevos notificados en SE 39–40, con un contexto de notificaciones retrospectivas.
- El informe #15 describe **547** casos nuevos en SE 41–42. Al comparar retrospectivamente SE 39–40, el propio #15 cita **885**, de los cuales **242** se contabilizaron retrospectivamente desde el informe anterior; **643 + 242 = 885**.
- Por ello, **913 casos adicionales en el acumulado entre ediciones no equivale necesariamente a 913 infecciones ocurridas durante esas dos semanas**, y tampoco equivale a los 547 casos asignados a SE 41–42. No atribuir los 124 restantes por resta a una causa específica sin revisar tablas/fechas de actualización del informe completo.
- Los multiplicadores interanuales publicados (4,8 veces en #14 y 4,7 veces en #15) usan **periodos de comparación distintos**; su cambio no prueba que el brote haya terminado.

## Nota pública en español, para revisión humana (NO enviada)

> Según los informes de situación #14 (22 de octubre) y #15 (6 de noviembre) de la OPS/OMS, el total de casos confirmados de sarampión notificados en las Américas pasó de 56.753 (hasta la semana epidemiológica 41) a 57.666 (hasta la semana 43). Las 81 defunciones acumuladas notificadas no variaron entre ambos resúmenes. Estos son **cortes de vigilancia con revisiones retrospectivas**: la diferencia entre totales no debe presentarse como el número exacto de contagios ocurridos en las últimas dos semanas. Para conocer las recomendaciones de vacunación y los avisos locales, consulte a la autoridad sanitaria de su país.

## Decisión y siguiente paso

**Decisión Scout:** `verified_candidate` **solo para mejora de interpretación y comunicación de datos**; no es una nueva alerta epidemiológica ni un defecto oficial confirmado. Novedad 0,35; utilidad 0,72; calidad de evidencia 0,74; incertidumbre 0,35 (puntuaciones heurísticas, no medidas científicas). STEEP+: social/salud, tecnología de información pública, ética de comunicación y gobernanza; TIPPO: mejora de prácticas de verificación y divulgación; Tres Horizontes: H1 vigilancia actual; Triángulo: empuje (boletines nuevos), atracción (mensajes comparables), peso (revisiones retrospectivas). Riesgo cruzado: titulares que exageren la incidencia reciente o minimicen un brote aún activo.

**Falsificación / cierre:** Si el PDF íntegro muestra cifras o definiciones diferentes de los resúmenes indexados, corregir o retirar esta nota; si no, mantener como ayuda de interpretación, no como informe de impacto.

**Siguiente acción no ejecutada:** Verificar los PDFs/figuras/tablas originales en navegador sin caché y obtener revisión cualificada de epidemiología/comunicación en español antes de cualquier distribución. Ningún contacto institucional, publicación fuera del repositorio, recomendación clínica individual ni resultado sanitario verificado.
