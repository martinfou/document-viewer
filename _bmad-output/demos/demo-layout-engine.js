/** Logique PDF.js + navigation documents — partagée par les démos de layout M1/M2/M3. */
pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

const pdfEngine = { doc: null, page: 1, scale: 1.15 };
const nativeViewerEnabled = document.body?.dataset?.nativeViewer === "true";

function layoutViewer() {
  return {
    docs: window.DEMO_DOCS,
    selected: 0,
    loading: false,
    error: null,
    fileProtocolWarning: false,
    pdfReady: false,
    pdfUiPage: 1,
    pdfUiNumPages: 0,
    pdfUiScalePct: 115,
    pdfThumbs: {},
    thumbsLoading: false,

    get current() {
      return this.docs[this.selected];
    },
    get currentLabel() {
      const d = this.current;
      return d ? `${d.name} — ${d.type} · ${d.category}` : "—";
    },
    get isPdf() {
      return this.current?.render === "pdf";
    },
    get pdfPageInfo() {
      if (!this.pdfReady) return "—";
      return `Page ${this.pdfUiPage} / ${this.pdfUiNumPages} · ${this.pdfUiScalePct}%`;
    },
    get viewerMode() {
      const d = this.current;
      if (!d) return "";
      if (nativeViewerEnabled) return "Viewer natif navigateur";
      return d.render === "pdf" ? "PDF.js / canvas" : "img";
    },
    thumbSrc(doc) {
      if (doc.render === "image") return this.assetUrl(doc.url);
      if (doc.thumbUrl) return this.assetUrl(doc.thumbUrl);
      return this.pdfThumbs[doc.id] || null;
    },

    async initWithThumbs() {
      this.fileProtocolWarning = window.location.protocol === "file:";
      await this.buildPdfThumbnails();
      this.$nextTick(() => this.loadCurrent());
    },

    async buildPdfThumbnails() {
      if (window.location.protocol === "file:") return;
      const pdfs = this.docs.filter((d) => d.render === "pdf");
      const needRender = [];
      for (const doc of pdfs) {
        if (doc.thumbUrl) {
          try {
            const res = await fetch(this.assetUrl(doc.thumbUrl), { method: "HEAD" });
            if (res.ok) continue;
          } catch {
            /* fallback PDF.js */
          }
        }
        needRender.push(doc);
      }
      if (!needRender.length) return;
      this.thumbsLoading = true;
      for (const doc of needRender) {
        try {
          const res = await fetch(this.assetUrl(doc.url));
          if (!res.ok) continue;
          const data = await res.arrayBuffer();
          const pdf = await pdfjsLib.getDocument({ data }).promise;
          const page = await pdf.getPage(1);
          const base = page.getViewport({ scale: 1 });
          const scale = 200 / base.width;
          const vp = page.getViewport({ scale });
          const canvas = document.createElement("canvas");
          const w = Math.floor(vp.width);
          const h = Math.floor(vp.height);
          canvas.width = w;
          canvas.height = h;
          await page.render({
            canvasContext: canvas.getContext("2d"),
            viewport: vp,
          }).promise;
          this.pdfThumbs[doc.id] = canvas.toDataURL("image/jpeg", 0.85);
        } catch (err) {
          console.warn("Vignette PDF:", doc.name, err);
        }
      }
      this.thumbsLoading = false;
    },

    resetPdf() {
      pdfEngine.doc = null;
      pdfEngine.page = 1;
      this.pdfReady = false;
      this.pdfUiPage = 1;
      this.pdfUiNumPages = 0;
    },

    assetUrl(relative) {
      return new URL(relative, window.location.href).href;
    },

    init() {
      this.fileProtocolWarning = window.location.protocol === "file:";
      this.$nextTick(() => this.loadCurrent());
    },

    select(i) {
      this.selected = i;
      this.loadCurrent();
    },

    docPrev() {
      if (this.selected > 0) this.select(this.selected - 1);
    },

    docNext() {
      if (this.selected < this.docs.length - 1) this.select(this.selected + 1);
    },

    onKey(e) {
      if (e.key === "ArrowRight" && this.selected < this.docs.length - 1) {
        e.preventDefault();
        this.select(this.selected + 1);
      }
      if (e.key === "ArrowLeft" && this.selected > 0) {
        e.preventDefault();
        this.select(this.selected - 1);
      }
    },

    clearHost() {
      const h = this.$refs.viewerHost;
      if (h) h.innerHTML = "";
    },

    async waitForViewerLayout() {
      for (let i = 0; i < 10; i++) {
        await new Promise((r) => requestAnimationFrame(r));
        if ((this.$refs.viewerHost?.clientWidth || 0) > 80) return;
      }
    },

    async loadCurrent() {
      const doc = this.current;
      if (!doc) return;
      this.error = null;
      this.loading = true;
      this.resetPdf();
      this.clearHost();
      try {
        if (doc.render === "pdf") {
          if (nativeViewerEnabled) await this.renderPdfNative(doc);
          else await this.renderPdf(doc.url);
        }
        else await this.renderImage(doc);
      } catch (err) {
        console.error(err);
        this.error = err.message || String(err);
      } finally {
        this.loading = false;
        if (!nativeViewerEnabled && doc.render === "pdf" && pdfEngine.doc && !this.error) {
          await this.$nextTick();
          await this.waitForViewerLayout();
          await this.pdfFitWidth();
        }
      }
    },

    async renderPdfNative(doc) {
      this.clearHost();
      const src = this.assetUrl(doc.url);
      const frame = document.createElement("iframe");
      frame.src = src;
      frame.title = doc.pillLabel || doc.name || "Document";
      frame.className = "w-full h-full bg-white";
      frame.setAttribute("loading", "eager");
      this.$refs.viewerHost.appendChild(frame);
    },

    openCurrentInNewTab() {
      const doc = this.current;
      if (!doc) return;
      window.open(this.assetUrl(doc.url), "_blank", "noopener,noreferrer");
    },

    async renderPdf(url) {
      if (window.location.protocol === "file:") {
        throw new Error(
          "PDF.js bloque file:// — utilisez GitHub Pages ou python3 serve-demos.py"
        );
      }
      const absolute = this.assetUrl(url);
      const res = await fetch(absolute);
      if (!res.ok) throw new Error(`Impossible de charger le PDF (HTTP ${res.status})`);
      const data = await res.arrayBuffer();
      pdfEngine.doc = await pdfjsLib.getDocument({ data }).promise;
      pdfEngine.page = 1;
      this.pdfReady = true;
      this.pdfUiPage = 1;
      this.pdfUiNumPages = pdfEngine.doc.numPages;
    },

    hostSize() {
      const host = this.$refs.viewerHost;
      const w = host?.clientWidth || 0;
      return { w: w > 0 ? w : 640, h: host?.clientHeight || 400 };
    },

    async pageAtScale1() {
      const page = await pdfEngine.doc.getPage(pdfEngine.page);
      return page.getViewport({ scale: 1 });
    },

    async pdfFitWidth() {
      if (!pdfEngine.doc) return;
      const base = await this.pageAtScale1();
      const { w } = this.hostSize();
      pdfEngine.scale = Math.min(2.5, Math.max(0.5, (w - 48) / base.width));
      this.pdfUiScalePct = Math.round(pdfEngine.scale * 100);
      await this.paintPdf();
    },

    async pdfFitHeight() {
      if (!pdfEngine.doc) return;
      const base = await this.pageAtScale1();
      const { h } = this.hostSize();
      pdfEngine.scale = Math.min(2.5, Math.max(0.5, (h - 24) / base.height));
      this.pdfUiScalePct = Math.round(pdfEngine.scale * 100);
      await this.paintPdf();
    },

    async paintPdf() {
      const doc = pdfEngine.doc;
      if (!doc) return;
      const page = await doc.getPage(pdfEngine.page);
      const vp = page.getViewport({ scale: pdfEngine.scale });
      const dpr = window.devicePixelRatio || 1;
      this.clearHost();
      const wrap = document.createElement("div");
      wrap.className = "inline-block leading-none shrink-0";
      const canvas = document.createElement("canvas");
      canvas.className = "shadow-lg bg-white block";
      const ctx = canvas.getContext("2d");
      const w = Math.floor(vp.width);
      const h = Math.floor(vp.height);
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;
      wrap.appendChild(canvas);
      this.$refs.viewerHost.appendChild(wrap);
      const transform = dpr !== 1 ? [dpr, 0, 0, dpr, 0, 0] : null;
      await page.render({ canvasContext: ctx, viewport: vp, transform }).promise;
    },

    async pdfPrev() {
      if (pdfEngine.page > 1) {
        pdfEngine.page--;
        this.pdfUiPage = pdfEngine.page;
        await this.pdfFitWidth();
      }
    },

    async pdfNext() {
      if (pdfEngine.doc && pdfEngine.page < pdfEngine.doc.numPages) {
        pdfEngine.page++;
        this.pdfUiPage = pdfEngine.page;
        await this.pdfFitWidth();
      }
    },

    async pdfZoom(d) {
      pdfEngine.scale = Math.min(2.5, Math.max(0.7, pdfEngine.scale + d));
      this.pdfUiScalePct = Math.round(pdfEngine.scale * 100);
      await this.paintPdf();
    },

    async renderImage(doc) {
      this.clearHost();
      const wrap = document.createElement("div");
      wrap.className = "w-full h-full flex items-center justify-center p-2";
      const img = document.createElement("img");
      img.src = this.assetUrl(doc.url);
      img.alt = doc.pillLabel || doc.name;
      img.className = "max-w-full max-h-full object-contain rounded-lg shadow-lg ring-2 ring-dj/50 block";
      wrap.appendChild(img);
      this.$refs.viewerHost.appendChild(wrap);
    },
  };
}
