# ESTADO

**Fase actual:** 1 (Corpus), en implementación.

## Hecho
- Andamiaje del repo: git, `.gitignore`, `.env.example`, licencia MIT, Python 3.12 y `requirements.txt` pinneado.
- Diseño en `diseno/`: biblia de la empresa, catálogo de 50 documentos y 8 huecos.
- `hechos.csv`: 212 hechos, con 5 contradicciones, 12 procesos con versión vieja y nueva, y 16 cruces.
- `scripts/validar_hechos.py`, con sus tests (pasan).

## Pendiente (fase 1)
- [ ] Tanda 1 (D01, D08, D14, D15, D22, D24, D30, D33, D38, D44)
- [ ] Tanda 2
- [ ] Tanda 3
- [ ] Tanda 4
- [ ] Tanda 5
- [ ] Revisión independiente con un subagente y correcciones
- [ ] Actualizar CLAUDE.md, ESTADO.md y README; commit de cierre

## Próximos pasos
Escribir las tandas en orden. Al final de cada una, correr `validar_hechos.py --parcial --tanda N`.
