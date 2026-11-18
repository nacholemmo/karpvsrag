/* Landing: todos los números salen de datos/results.json (copia de resultados/results.json). */
(function () {
  "use strict";

  const BRAZOS = [
    { id: "contexto", nombre: "Contexto completo", color: "var(--s-contexto)" },
    { id: "wiki", nombre: "Wiki LLM", color: "var(--s-wiki)" },
    { id: "rag", nombre: "RAG híbrido", color: "var(--s-rag)" },
  ];
  const TIPOS = [
    ["dato", "Dato puntual"], ["procedimiento", "Procedimiento"], ["cruce", "Cruce de documentos"],
    ["contradiccion", "Contradicción"], ["version", "Versión vigente"], ["sin_respuesta", "Sin respuesta"],
  ];
  const VEREDICTOS = [
    { id: "correcta", nombre: "Correcta", color: "var(--ok)", tinta: "var(--en-ok)" },
    { id: "parcial", nombre: "Parcial", color: "var(--parcial)", tinta: "var(--en-parcial)" },
    { id: "incorrecta", nombre: "Incorrecta", color: "var(--mal)", tinta: "var(--en-mal)" },
  ];
  const SVGNS = "http://www.w3.org/2000/svg";

  const num = (x, d = 2) => Number(x).toLocaleString("es-AR", { minimumFractionDigits: d, maximumFractionDigits: d });
  const usd = (x, d = 4) => "USD " + num(x, d);
  const pct = (x) => num(x, 0) + "%";
  const el = (tag, attrs = {}, hijos = []) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) k === "text" ? (n.textContent = v) : n.setAttribute(k, v);
    for (const h of [].concat(hijos)) if (h) n.append(h);
    return n;
  };
  const sv = (tag, attrs = {}) => {
    const n = document.createElementNS(SVGNS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    return n;
  };
  // Ancho real disponible: el SVG se dibuja en píxeles de pantalla para que el texto no se achique en celular.
  const anchoDe = (fig) => Math.max(300, Math.min(680, fig.clientWidth - 34));
  function lienzo(fig, svg) {
    let l = fig.querySelector(".lienzo");
    if (!l) {
      l = el("div", { class: "lienzo" });
      const det = fig.querySelector("details");
      det ? fig.insertBefore(l, det) : fig.append(l);
    }
    l.replaceChildren(svg);
  }
  const punto = (color) => el("span", { class: "punto", style: `background:${color}` });

  // --- Links al repo (una sola constante en config.js) ---
  const repo = (window.REPO_URL || "").replace(/\/$/, "");
  document.querySelectorAll("a.repo").forEach((a) => {
    const ruta = a.getAttribute("data-ruta");
    a.href = ruta ? `${repo}/blob/main/${ruta}` : repo;
  });

  // --- Tooltip compartido ---
  const globo = document.getElementById("globo");
  function conGlobo(marca, texto) {
    marca.setAttribute("tabindex", "0");
    marca.setAttribute("aria-label", texto);
    marca.classList.add("marca");
    const t = sv("title");
    t.textContent = texto;
    marca.append(t);
    const mostrar = (x, y) => {
      globo.textContent = texto;
      globo.style.left = Math.min(x + 12, window.innerWidth - 270) + "px";
      globo.style.top = y + 12 + "px";
      globo.classList.add("visible");
    };
    marca.addEventListener("pointermove", (e) => mostrar(e.clientX, e.clientY));
    marca.addEventListener("pointerleave", () => globo.classList.remove("visible"));
    marca.addEventListener("focus", () => {
      const r = marca.getBoundingClientRect();
      mostrar(r.left + r.width / 2, r.top);
    });
    marca.addEventListener("blur", () => globo.classList.remove("visible"));
  }

  function leyenda(items) {
    return el("ul", { class: "leyenda" }, items.map((i) =>
      el("li", {}, [el("span", { class: "muestra", style: `background:${i.color}` }), i.nombre])));
  }

  function tablaDetalle(titulo, cabeceras, filas) {
    const t = el("table");
    t.append(el("thead", {}, el("tr", {}, cabeceras.map((c) => el("th", { text: c })))));
    t.append(el("tbody", {}, filas.map((f) => el("tr", {}, f.map((c) => el("td", { text: c }))))));
    return el("details", {}, [el("summary", { text: titulo }), el("div", { class: "tabla-envoltura" }, t)]);
  }

  // Barra con extremo de dato redondeado (4 px) y base recta, horizontal.
  function barraH(x, y, ancho, alto, color) {
    const r = Math.min(4, ancho / 2, alto / 2);
    if (ancho <= 0) return sv("rect", { x, y, width: 0, height: alto });
    const d = `M${x},${y} h${ancho - r} a${r},${r} 0 0 1 ${r},${r} v${alto - 2 * r} a${r},${r} 0 0 1 -${r},${r} h-${ancho - r} z`;
    return sv("path", { d, fill: color });
  }

  // --- Cifras de cabecera ---
  function cifras(r) {
    const cont = document.getElementById("cifras");
    for (const b of BRAZOS) {
      const m = r.brazos[b.id];
      cont.append(el("div", { class: "cifra" }, [
        el("div", { class: "nombre" }, [punto(b.color), b.nombre]),
        el("div", { class: "valor", text: num(m.exactitud.puntaje) }),
        el("div", { class: "detalle", text: `${pct(m.exactitud.pct_correcta)} correctas · ${usd(m.costo_usd.media)} por consulta` }),
      ]));
    }
    document.getElementById("nota-cifras").textContent =
      "Puntaje de 0 a 1 sobre 50 preguntas (correctas + 0,5 × parciales). Modelo: Claude Haiku 5.5 en los tres brazos.";
  }

  // --- Tabla de resultados ---
  function tablaResultados(r) {
    const p = r.preparacion;
    const prep = {
      contexto: "Ninguna",
      rag: `Indexación local ${num(p.rag.indexacion_segundos, 0)} s · USD 0`,
      wiki: `${usd(p.wiki.ingesta_costo_usd + p.wiki.lint_costo_usd, 2)} · ${num(p.wiki.ingesta_segundos / 60, 0)} min`,
    };
    const t = document.getElementById("tabla-resultados");
    t.append(el("thead", {}, el("tr", {}, ["Brazo", "Puntaje", "Correctas", "Parciales", "Incorrectas",
      "Costo / consulta", "Latencia (mediana)", "Llamadas / consulta", "Preparación"].map((c) => el("th", { scope: "col", text: c })))));
    const cuerpo = el("tbody");
    for (const b of BRAZOS) {
      const m = r.brazos[b.id];
      const e = m.exactitud;
      cuerpo.append(el("tr", {}, [
        el("th", { scope: "row" }, [punto(b.color), " ", b.nombre]),
        el("td", { text: num(e.puntaje) }), el("td", { text: `${e.correcta} (${pct(e.pct_correcta)})` }),
        el("td", { text: String(e.parcial) }), el("td", { text: String(e.incorrecta) }),
        el("td", { text: usd(m.costo_usd.media) }), el("td", { text: num(m.latencia_s.mediana, 1) + " s" }),
        el("td", { text: num(m.llamadas_por_pregunta.media, 1) }), el("td", { text: prep[b.id] }),
      ]));
    }
    t.append(cuerpo);
    const est = r.brazos._estabilidad_juez;
    const orig = r.brazos_referencias_originales;
    document.getElementById("nota-tabla").textContent =
      `Juez: voto de ${est.corridas} corridas; ${est.unanime} de ${est.respuestas} veredictos fueron unánimes. ` +
      `Con las referencias originales, antes de corregir las preguntas sin respuesta: ` +
      BRAZOS.map((b) => `${b.nombre} ${num(orig[b.id].exactitud.puntaje)}`).join(", ") + ".";
  }

  // --- Gráfico 1: puntaje por tipo (barras horizontales agrupadas) ---
  function graficoTipos(r) {
    const fig = document.getElementById("g-tipos");
    if (!fig.querySelector(".leyenda")) fig.append(leyenda(BRAZOS));
    const W = anchoDe(fig), izq = W < 460 ? 118 : 150, der = 40, altoBarra = 9, hueco = 2, grupo = BRAZOS.length * (altoBarra + hueco) + 14;
    const H = TIPOS.length * grupo + 24;
    const svg = sv("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": "Puntaje por tipo de pregunta y brazo" });
    const xs = (v) => izq + v * (W - izq - der);
    for (const t of [0, 0.5, 1]) {
      svg.append(sv("line", { x1: xs(t), x2: xs(t), y1: 0, y2: H - 20, class: t === 0 ? "eje" : "rejilla" }));
      const lab = sv("text", { x: xs(t), y: H - 4, "text-anchor": "middle" });
      lab.textContent = num(t, t === 0.5 ? 1 : 0);
      svg.append(lab);
    }
    TIPOS.forEach(([id, nombre], i) => {
      const y0 = i * grupo + 4;
      const lab = sv("text", { x: izq - 10, y: y0 + (BRAZOS.length * (altoBarra + hueco)) / 2 + 4, "text-anchor": "end" });
      lab.textContent = W < 460 && nombre === "Cruce de documentos" ? "Cruce" : nombre;
      svg.append(lab);
      BRAZOS.forEach((b, j) => {
        const d = r.brazos[b.id].por_tipo[id];
        const y = y0 + j * (altoBarra + hueco);
        const barra = barraH(xs(0), y, xs(d.puntaje) - xs(0), altoBarra, b.color);
        conGlobo(barra, `${b.nombre} · ${nombre}: ${num(d.puntaje)} (${d.correcta} correctas, ${d.parcial} parciales de ${d.n})`);
        svg.append(barra);
        const v = sv("text", { x: xs(d.puntaje) + 4, y: y + altoBarra - 1, class: "valor" });
        v.textContent = num(d.puntaje);
        v.setAttribute("font-size", "10");
        svg.append(v);
      });
    });
    lienzo(fig, svg);
    if (fig.querySelector("details")) return;
    fig.append(tablaDetalle("Ver como tabla", ["Tipo", ...BRAZOS.map((b) => b.nombre)],
      TIPOS.map(([id, nombre]) => [nombre, ...BRAZOS.map((b) => {
        const d = r.brazos[b.id].por_tipo[id];
        return `${num(d.puntaje)} (${d.correcta}/${d.n})`;
      })])));
  }

  // --- Gráfico 2: veredictos apilados por brazo ---
  function graficoVeredictos(r) {
    const fig = document.getElementById("g-veredictos");
    if (!fig.querySelector(".leyenda")) fig.append(leyenda(VEREDICTOS));
    const W = anchoDe(fig), izq = W < 460 ? 118 : 150, der = 10, alto = 26, sep = 14, H = BRAZOS.length * (alto + sep) + 4;
    const svg = sv("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": "Veredictos por brazo" });
    BRAZOS.forEach((b, i) => {
      const e = r.brazos[b.id].exactitud;
      const y = i * (alto + sep) + 2;
      const lab = sv("text", { x: izq - 10, y: y + alto / 2 + 4, "text-anchor": "end" });
      lab.textContent = b.nombre;
      svg.append(lab);
      let x = izq;
      const total = e.n, escala = (W - izq - der) / total;
      VEREDICTOS.forEach((v, k) => {
        const n = e[v.id];
        if (!n) return;
        const ancho = n * escala - (k < VEREDICTOS.length - 1 ? 2 : 0); // separador de 2 px entre segmentos
        const rect = sv("rect", { x, y, width: Math.max(ancho, 0), height: alto, rx: 3, fill: v.color });
        conGlobo(rect, `${b.nombre}: ${n} ${v.nombre.toLowerCase()}${n === 1 ? "" : "s"} de ${total}`);
        svg.append(rect);
        if (ancho > 26) {
          const t = sv("text", { x: x + ancho / 2, y: y + alto / 2 + 4, "text-anchor": "middle" });
          t.textContent = n;
          t.style.fill = v.tinta;
          svg.append(t);
        }
        x += n * escala;
      });
    });
    lienzo(fig, svg);
    if (fig.querySelector("details")) return;
    fig.append(tablaDetalle("Ver como tabla", ["Brazo", "Correctas", "Parciales", "Incorrectas"],
      BRAZOS.map((b) => {
        const e = r.brazos[b.id].exactitud;
        return [b.nombre, String(e.correcta), String(e.parcial), String(e.incorrecta)];
      })));
  }

  // --- Gráfico 3: costo por consulta vs. puntaje (un eje por dimensión) ---
  function graficoCosto(r) {
    const fig = document.getElementById("g-costo");
    const W = anchoDe(fig), H = 260, izq = 56, der = W < 460 ? 20 : 140, arr = 14, abajo = 40;
    const costos = BRAZOS.map((b) => r.brazos[b.id].costo_usd.media);
    const maxC = Math.ceil((Math.max(...costos) * 1.15) / 0.0005) * 0.0005;
    const minP = 0.7, maxP = 1.0;
    const xs = (c) => izq + (c / maxC) * (W - izq - der);
    const ys = (p) => arr + (1 - (p - minP) / (maxP - minP)) * (H - arr - abajo);
    const svg = sv("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": "Costo por consulta contra puntaje" });
    for (const p of [0.7, 0.8, 0.9, 1.0]) {
      svg.append(sv("line", { x1: izq, x2: W - der, y1: ys(p), y2: ys(p), class: p === minP ? "eje" : "rejilla" }));
      const t = sv("text", { x: izq - 8, y: ys(p) + 4, "text-anchor": "end" });
      t.textContent = num(p, 1);
      svg.append(t);
    }
    const paso = W < 460 ? 0.001 : 0.0005;
    for (let c = 0; c <= maxC + 1e-9; c += paso) {
      const t = sv("text", { x: xs(c), y: H - abajo + 18, "text-anchor": "middle" });
      t.textContent = num(c, 4);
      svg.append(t);
    }
    const tx = sv("text", { x: izq + (W - izq - der) / 2, y: H - 4, "text-anchor": "middle" });
    tx.textContent = "USD por consulta (media)";
    svg.append(tx);
    const ty = sv("text", { x: 12, y: arr + (H - arr - abajo) / 2, "text-anchor": "middle", transform: `rotate(-90 12 ${arr + (H - arr - abajo) / 2})` });
    ty.textContent = "Puntaje";
    svg.append(ty);
    BRAZOS.forEach((b) => {
      const m = r.brazos[b.id];
      const cx = xs(m.costo_usd.media), cy = ys(m.exactitud.puntaje);
      const c = sv("circle", { cx, cy, r: 7, fill: b.color, stroke: "var(--superficie)", "stroke-width": 2 });
      conGlobo(c, `${b.nombre}: puntaje ${num(m.exactitud.puntaje)}, ${usd(m.costo_usd.media)} por consulta`);
      svg.append(c);
      const aIzq = cx > W - der - 120;  // si la etiqueta no entra a la derecha, va a la izquierda del punto
      const t = sv("text", { x: aIzq ? cx - 12 : cx + 12, y: cy + 4, class: "valor", "text-anchor": aIzq ? "end" : "start" });
      t.textContent = `${b.nombre} (${num(m.exactitud.puntaje)})`;
      svg.append(t);
    });
    lienzo(fig, svg);
    if (fig.querySelector("details")) return;
    fig.append(tablaDetalle("Ver como tabla", ["Brazo", "USD por consulta", "Puntaje"],
      BRAZOS.map((b) => [b.nombre, usd(r.brazos[b.id].costo_usd.media), num(r.brazos[b.id].exactitud.puntaje)])));
    fig.append(el("p", { class: "sub", text: "La wiki usa en promedio 3 llamadas por pregunta (índice y páginas). El costo de compilarla va aparte, en la tabla de resultados." }));
  }

  // --- Actualización ---
  function tablaActualizacion(r) {
    const a = r.actualizacion;
    const t = document.getElementById("tabla-actualizacion");
    t.append(el("thead", {}, el("tr", {}, ["Brazo", "Puntaje (10 preguntas)", "Costo de actualizar", "Tiempo de actualizar"].map((c) => el("th", { scope: "col", text: c })))));
    const desc = {
      contexto: ["USD 0 (solo reescribe la caché en la primera consulta)", "—"],
      rag: ["USD 0", `${num(a.costo_y_tiempo_de_actualizar.rag.segundos, 0)} s (reindexación local)`],
      wiki: [usd(a.costo_y_tiempo_de_actualizar.wiki.costo_usd, 3), `${num(a.costo_y_tiempo_de_actualizar.wiki.segundos / 60, 1)} min (reingesta de 3 documentos)`],
    };
    const cuerpo = el("tbody");
    for (const b of BRAZOS) {
      const e = a.brazos[b.id].exactitud;
      cuerpo.append(el("tr", {}, [el("th", { scope: "row" }, [punto(b.color), " ", b.nombre]),
        el("td", { text: `${num(e.puntaje)} (${e.correcta} correctas)` }), el("td", { text: desc[b.id][0] }), el("td", { text: desc[b.id][1] })]));
    }
    t.append(cuerpo);
  }

  function acuerdoYLimites(r) {
    const a = r.acuerdo_humano_juez;
    if (a && a.v1) {
      document.getElementById("acuerdo").innerHTML = "";
      document.getElementById("acuerdo").append(el("strong", { text: "Control del juez: " }),
        `en una muestra de 15 respuestas revisadas a mano, el juez coincidió en ${a.v1.acuerdo} de 15 con la rúbrica original ` +
        `y en ${a.v2.acuerdo} de 15 después de ajustarla mirando esa misma muestra.`);
    }
    const ul = document.getElementById("limites");
    for (const texto of r.meta.advertencias) ul.append(el("li", { text: texto }));
    ul.append(el("li", { text: "Con unos 92 mil tokens, el corpus entra entero en el contexto. Con un corpus mucho más grande, el contexto completo deja de ser viable y la comparación cambia." }));
    ul.append(el("li", { text: "La wiki se compiló tres veces: la primera tenía errores del harness y la segunda un esquema que filtraba respuestas. Los resultados usan la tercera." }));
  }

  fetch("datos/results.json")
    .then((resp) => { if (!resp.ok) throw new Error(resp.status); return resp.json(); })
    .then((r) => {
      cifras(r);
      tablaResultados(r);
      const dibujar = () => { graficoTipos(r); graficoVeredictos(r); graficoCosto(r); };
      dibujar();
      let espera;
      window.addEventListener("resize", () => { clearTimeout(espera); espera = setTimeout(dibujar, 150); });
      tablaActualizacion(r);
      acuerdoYLimites(r);
    })
    .catch((e) => {
      document.getElementById("cifras").append(el("p", { class: "error", text: "No se pudieron cargar los resultados (" + e.message + "). Están en resultados/results.json del repositorio." }));
    });
})();
