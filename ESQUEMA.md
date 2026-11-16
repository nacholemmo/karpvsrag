# Esquema de la wiki

La wiki en `wiki/` es la versión compilada y ordenada de los documentos internos de `corpus/` de Distribuidora Quebracho Azul S.A. La escribe y mantiene un agente. Otro agente la usa para responder preguntas **sin acceso a `corpus/`**, así que todo lo que importa tiene que quedar en la wiki, con su fuente.

## Reglas obligatorias

1. **Nunca se modifica `corpus/`.** Solo se escribe en `wiki/`.
2. **Toda afirmación lleva su fuente**, con el formato `[fuente: archivo.md]` al final de la línea o del ítem, usando el nombre exacto del archivo de `corpus/`. Si una línea combina dos documentos, se citan los dos: `[fuente: a.md] [fuente: b.md]`.
3. **Los datos duros se copian textualmente** del documento: montos (`$ 1.500.000`), plazos (`48 horas hábiles`), porcentajes, horarios, responsables y códigos. No se redondean, no se reformulan y no se cambian unidades.
4. **Versiones.** Si un documento nuevo cambia un valor de uno viejo, la página muestra el valor **vigente** primero y deja el anterior marcado:
   `- Plazo vigente: 48 horas hábiles [fuente: nuevo.md]. Antes (reemplazado): 24 horas de recibida [fuente: viejo.md].`
   Para saber cuál rige, se usan la fecha del documento y lo que diga sobre reemplazos. No se borra la versión vieja.
5. **Contradicciones.** Si dos documentos vigentes dicen cosas distintas y ninguno indica cuál prevalece, **no se resuelve**. Se registra en una sección:
   `### ⚠ Contradicción` con las dos posturas, cada una con su fuente.
6. **Huecos.** Si un documento menciona un tema sin definirlo (por ejemplo, "se evalúa más adelante"), se anota tal cual: `No definido en la documentación: …`, con su fuente. Nunca se completa con suposiciones.
7. **Referencias cruzadas.** Si un documento remite a otro ("según el punto 4 de la Política…"), en la wiki se resuelve: se escribe el dato con la fuente del documento que lo contiene y se agrega un enlace a la página correspondiente.

## Tipos de página y nombres

Los nombres van en minúsculas, en kebab-case y sin tildes ni ñ (`cobranza-de-mora.md`). Una página por tema; antes de crear una página nueva, se revisa si ya hay una que lo cubra.

| Carpeta | Contenido | Ejemplo |
|---|---|---|
| `proceso/` | Un proceso operativo: pasos, plazos, responsables, excepciones | `proceso/recepcion-de-mercaderia.md` |
| `politica/` | Reglas, condiciones, límites, montos | `politica/creditos-y-cobranzas.md` |
| `rol/` | Un puesto: qué hace, qué aprueba y quién lo ocupa | `rol/jefa-de-creditos-y-cobranzas.md` |
| `sistema/` | Un sistema interno (Tacuarí, Lapacho, Mostrador, Fénix) | `sistema/tacuari.md` |
| raíz | `index.md` (índice) y `glosario.md` (términos y siglas) | |

Estructura de cada página:

```markdown
# Título

Resumen de 1 a 2 líneas.

## <secciones del tema>
- Dato o paso [fuente: archivo.md]

## Relacionado
- [Otra página](../tipo/otra-pagina.md)
```

## Enlaces e índice

- Los enlaces son relativos: `[texto](../tipo/pagina.md)` desde una página de carpeta, y `[texto](tipo/pagina.md)` desde `index.md`.
- **`index.md`** tiene una línea por página: `- [Título](tipo/pagina.md): de qué trata, con palabras clave`. Cada página nueva se agrega al índice en la misma sesión. El índice es lo primero que lee quien consulta, así que las descripciones tienen que permitir encontrar el tema: montos, plazos, aprobaciones o excepciones.
- Ninguna página puede quedar fuera del índice.
- Escribí pocas páginas por turno, una o dos: una respuesta con muchas páginas largas se corta y se pierde.
