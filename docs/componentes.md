# Componentes de las notas (sintaxis de Quarto)

Guía rápida para escribir y para pedir cambios. Ejemplo completo y renderizado: `cursos/econometria-3/nivel-local.qmd`.

## Encabezado de cada nota

```yaml
---
title: "Título de la nota"
description: "Una oración."
author: "Mario Peñaloza"
date: 2026-10-07
categories: [curso, tema]
draft: true   # borrador: no se publica
---
```

## Definiciones, teoremas y demás

Los identificadores llevan prefijo y definen el tipo: `def-`, `thm-`, `lem-`, `prp-`, `cor-`, `exm-`, `exr-`. El título va en un encabezado de nivel 2 dentro del recuadro.

```markdown
::: {#thm-ejemplo}
## Título del teorema

Enunciado con $x \in \R$ y referencia a la @def-otra.
:::

::: {.proof}
Demostración, con cada paso justificado en una oración.
:::
```

Se cita con `@thm-ejemplo`, que produce "Teorema 1" con enlace. Las demostraciones y observaciones usan `{.proof}` y `{.remark}`.

## Ecuaciones

```markdown
$$
\begin{aligned}
y_t &= \mu_t + \varepsilon_t, \\
\mu_{t+1} &= \mu_t + \xi_t.
\end{aligned}
$$ {#eq-modelo}
```

Se cita con `@eq-modelo`. Reglas de estilo del autor: en ecuaciones de varias filas se repite el lado izquierdo en cada fila; las matrices se escriben completas, con sus ceros.

Macros disponibles (en `assets/macros.html` y `assets/macros.tex`, deben mantenerse iguales): `\E`, `\Var`, `\Cov`, `\N`, `\R`, `\Y`, `\iid`, `\tr`, `\plim`.

## Código y figuras

````markdown
```{python}
#| label: fig-ejemplo
#| fig-cap: "Descripción de la figura."
#| fig-alt: "Texto alternativo."
import numpy as np
```
````

Los resultados se guardan en `_freeze/` y no se recalculan mientras el código no cambie. Stata, EViews y Matlab no se ejecutan en la nube: se corren en local y se incrustan sus tablas y figuras como archivos.

## Solución desplegable

```markdown
::: {.callout-tip collapse="true" title="Solución"}
Texto de la solución.
:::
```

## Citas

Agregar la entrada a `references.bib` y citar con `@clave` o `[@clave, p. 12]`. Estilo APA 7 (`assets/apa.csl`). No inventar DOI ni páginas: lo no verificado se deja fuera o se marca como pendiente.
