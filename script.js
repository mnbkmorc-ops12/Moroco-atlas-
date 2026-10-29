:root {
  --bg: #0d1728;
  --bg-alt: #101d33;
  --panel: rgba(16, 27, 42, 0.82);
  --line: rgba(255,255,255,0.12);
  --text: #edf6ff;
  --muted: #bfcae0;
  --primary: #f59e0b;
  --primary-dark: #d97706;
  --secondary: #24c38e;
  --cyan: #8ad7ff;
  --shadow: rgba(15, 23, 42, 0.55);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Cairo", sans-serif;
  background: radial-gradient(circle at top, rgba(245,158,11,0.14), transparent 22%), linear-gradient(180deg, #0b1320 0%, #0d1728 100%);
  color: var(--text);
}

a { color: inherit; text-decoration: none; }
img { max-width: 100%; display: block; }
button, input, select, textarea { font: inherit; }
.container { width: min(1180px, calc(100% - 32px)); margin: 0 auto; }

.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(16px);
  background: rgba(11, 19, 32, 0.72);
  border-bottom: 1px solid var(--line);
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 800;
}

.logo {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #0d1728;
  font-weight: 800;
}

nav {
  display: flex;
  align-items: center;
  gap: 20px;
  color: var(--muted);
  flex-wrap: wrap;
}

.hero, .highlights, .destinations, .map-section, .planner, .experience-section, .booking-section, .gallery, .faq {
  padding: 54px 0;
}

.hero-copy h1, .section-heading h2, .booking-form-wrap h2, .planner-panel h2, .itinerary-panel h3 {
  margin: 0;
  line-height: 1.08;
  letter-spacing: -0.05em;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 32px;
  align-items: center;
}

.eyebrow {
  margin: 0 0 12px;
  color: var(--cyan);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 0.72rem;
  font-weight: 700;
}

.hero-copy h1 { font-size: clamp(2.8rem, 6vw, 5rem); max-width: 680px; }
.lead { margin-top: 22px; color: var(--muted); line-height: 1.9; max-width: 640px; }
.section-heading { margin-bottom: 28px; }
.section-heading h2 { font-size: clamp(2rem, 4vw, 3rem); }

.actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 32px;
}

.primary, .secondary, .filter, .detail-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 22px;
  border-radius: 999px;
  border: 1px solid transparent;
  font-weight: 700;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.primary {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #0d1728;
  box-shadow: 0 18px 40px rgba(245,158,11,0.25);
}
.secondary {
  background: rgba(255,255,255,0.03);
  border-color: var(--line);
}
.detail-button {
  background: rgba(125,211,252,0.08);
  border-color: rgba(125,211,252,0.2);
  color: var(--text);
}
.primary:hover, .secondary:hover, .filter:hover, .detail-button:hover, .destination-card:hover { transform: translateY(-1px); }

.stats {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
  margin: 36px 0 0;
}
.stats li {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: var(--muted);
}
.stats strong { color: var(--text); font-size: 1.8rem; }

.hero-card {
  position: relative;
  min-height: 500px;
  overflow: hidden;
  border-radius: 28px;
  background: linear-gradient(180deg, rgba(15,23,42,0.78), rgba(19,31,49,0.94));
  border: 1px solid var(--line);
  box-shadow: var(--shadow);
}

.card-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 30% 20%, rgba(34,197,94,0.18), transparent 30%), radial-gradient(circle at 70% 65%, rgba(125,211,252,0.12), transparent 30%);
}

.mini-map {
  position: absolute;
  inset: 20px;
  border-radius: 22px;
  border: 1px solid rgba(255,255,255,0.12);
  background: linear-gradient(135deg, rgba(245,158,11,0.22), rgba(37,99,235,0.08)), linear-gradient(180deg, rgba(28,41,59,0.94), rgba(15,23,42,0.94));
}
.mini-map::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent 0 20%, rgba(255,255,255,0.12) 20% 21%, transparent 21% 40%, rgba(255,255,255,0.12) 40% 41%, transparent 41%), linear-gradient(transparent 0 25%, rgba(255,255,255,0.12) 25% 26%, transparent 26% 50%, rgba(255,255,255,0.12) 50% 51%, transparent 51%);
}
.pin {
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #fbbf24, #f97316);
  box-shadow: 0 0 0 7px rgba(251,191,36,0.18);
}
.pin-1 { top: 30%; left: 28%; }
.pin-2 { top: 48%; left: 58%; }
.pin-3 { top: 66%; left: 38%; }
.pin-4 { top: 32%; right: 26%; }

.destination-info {
  position: absolute;
  left: 28px;
  right: 28px;
  bottom: 24px;
  background: rgba(15,23,42,0.72);
  border: 1px solid var(--line);
  border-radius: 20px;
  backdrop-filter: blur(12px);
  padding: 18px 20px;
}
.destination-info p, .destination-info small { margin: 0; color: var(--muted); }
.destination-info h2 { margin: 6px 0; font-size: clamp(1.8rem, 3vw, 2.5rem); }

.highlight-grid, .experience-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; }
.feature, .experience-card, .destination-card, .planner-panel, .itinerary-panel, .faq-list details, .city-detail, .map-panel, .detail-panel, .booking-form-wrap, .booking-summary {
  background: rgba(17,24,39,0.72);
  border: 1px solid var(--line);
  border-radius: 22px;
}
.feature, .experience-card { padding: 24px 20px; }
.icon {
  display: inline-flex;
  width: 54px;
  height: 54px;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: rgba(245,158,11,0.12);
  font-size: 1.9rem;
}
.feature h3, .experience-card h3 { margin: 20px 0 12px; }
.feature p, .experience-card p, .destination-card p, .faq-list details p, .city-detail p, .detail-summary, .booking-summary p { margin: 0; color: var(--muted); line-height: 1.8; }

.split { display: flex; gap: 20px; align-items: end; justify-content: space-between; }
.filter-bar { display: flex; flex-wrap: wrap; gap: 10px; }
.filter {
  background: rgba(255,255,255,0.02);
  border-color: var(--line);
  color: var(--text);
  cursor: pointer;
  min-height: 42px;
  padding: 0 18px;
}
.filter.active { background: rgba(245,158,11,0.12); border-color: rgba(245,158,11,0.4); }

.search-box { margin: 18px 0 24px; }
.search-box input {
  width: 100%;
  min-height: 54px;
  background: rgba(255,255,255,0.02);
  color: var(--text);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 0 18px;
}
.search-box input::placeholder { color: var(--muted); }

.destination-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
.destination-card { overflow: hidden; }
.destination-image {
  min-height: 250px;
  display: flex;
  align-items: end;
  padding: 22px;
  background-position: center;
  background-size: cover;
}
.destination-image span {
  display: inline-block;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(15,23,42,0.7);
  border: 1px solid rgba(255,255,255,0.14);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.destination-card-content { padding: 18px 18px 22px; }
.destination-card h3 { margin: 0 0 8px; font-size: 1.45rem; }
.destination-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
.destination-meta span {
  padding: 7px 10px;
  border-radius: 999px;
  background: rgba(125,211,252,0.08);
  color: #d7f3ff;
  border: 1px solid rgba(125,211,252,0.18);
  font-size: 0.76rem;
}

.detail-panel { overflow: hidden; }
.detail-hero {
  min-height: 290px;
  padding: 24px;
  display: flex;
  align-items: end;
  background-size: cover;
  background-position: center;
  position: relative;
}
.detail-hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(12,17,27,0.12), rgba(12,17,27,0.82));
}
.detail-hero-content { position: relative; z-index: 1; }
.detail-hero h3 { font-size: clamp(2.3rem, 4vw, 3.3rem); margin: 0 0 8px; }
.detail-hero p { margin: 0; color: rgba(255,255,255,0.9); max-width: 680px; }
.detail-body {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 20px;
  padding: 24px;
}
.detail-facts, .detail-experiences {
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px;
}
.detail-facts ul, .detail-experiences ul { margin: 14px 0 0; padding-inline-start: 20px; color: var(--muted); line-height: 1.9; }

.map-layout { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 20px; align-items: center; }
.map-panel { padding: 20px; }
.morocco-map { width: 100%; height: 520px; display: block; }
.map-shape { fill: rgba(125,211,252,0.12); stroke: rgba(125,211,252,0.42); stroke-width: 3; }
.map-point {
  fill: rgba(245,158,11,0.9);
  stroke: rgba(255,255,255,0.8);
  stroke-width: 3;
  cursor: pointer;
  transition: transform 0.2s ease, fill 0.2s ease;
}
.map-point:hover, .map-point.active { fill: #22c55e; transform: scale(1.2); }

.city-detail { padding: 22px 20px; min-height: 300px; }
.city-detail .badge {
  display: inline-block;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(34,197,94,0.12);
  color: #baf9da;
  border: 1px solid rgba(34,197,94,0.24);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.city-detail h3 { margin: 18px 0 14px; font-size: clamp(1.8rem, 2.8vw, 2.5rem); }
.city-detail ul { margin: 16px 0 0; padding-inline-start: 20px; color: var(--muted); line-height: 1.9; }

.planner-grid { display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 20px; }
.planner-panel, .itinerary-panel { padding: 22px 20px; }
.compact { margin-bottom: 20px; }
.itinerary-form, .booking-form { display: grid; gap: 18px; }
.itinerary-form label, .booking-form label { display: grid; gap: 8px; color: var(--muted); }
.itinerary-form select, .booking-form select, .booking-form input, .booking-form textarea {
  border: 1px solid var(--line);
  border-radius: 12px;
  background: rgba(255,255,255,0.02);
  color: var(--text);
  padding: 12px 14px;
}
.booking-form input::placeholder, .booking-form textarea::placeholder { color: var(--muted); }
.field-row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.full-width { width: 100%; border: none; cursor: pointer; }
.itinerary-output { display: grid; gap: 12px; margin-top: 18px; }
.route-step {
  padding: 12px 14px;
  border-radius: 14px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--line);
}
.route-step strong { display: block; margin-bottom: 6px; }

.experience-card .tag {
  display: inline-block;
  background: rgba(34,197,94,0.12);
  color: #afffdb;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(34,197,94,0.2);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.booking-grid { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 20px; }
.booking-form-wrap, .booking-summary { padding: 22px 20px; }
.booking-summary h3 { margin: 0 0 12px; font-size: 1.8rem; }
.summary-box {
  margin-top: 18px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 14px 16px;
}

.gallery-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-auto-rows: 200px; gap: 16px; }
.gallery-item {
  display: flex;
  align-items: end;
  justify-content: flex-start;
  border-radius: 20px;
  padding: 18px;
  color: white;
  font-weight: 700;
  border: 1px solid var(--line);
  background: linear-gradient(135deg, rgba(0,0,0,0.08), rgba(0,0,0,0.42)), linear-gradient(135deg, #f59e0b, #0ea5e9);
}
.gallery-item:nth-child(1) { background: linear-gradient(135deg, rgba(0,0,0,0.08), rgba(0,0,0,0.42)), linear-gradient(135deg, #f59e0b, #a16207); }
.gallery-item:nth-child(2) { background: linear-gradient(135deg, rgba(0,0,0,0.08), rgba(0,0,0,0.42)), linear-gradient(135deg, #3b82f6, #1d4ed8); }
.gallery-item:nth-child(3) { background: linear-gradient(135deg, rgba(0,0,0,0.08), rgba(0,0,0,0.42)), linear-gradient(135deg, #34d399, #059669); }
.gallery-item:nth-child(4) { background: linear-gradient(135deg, rgba(0,0,0,0.08), rgba(0,0,0,0.42)), linear-gradient(135deg, #f472b6, #db2777); }
.gallery-item.tall { grid-row: span 2; }
.gallery-item.wide { grid-column: span 2; }

.faq-list { display: grid; gap: 14px; }
.faq-list details { padding: 18px 20px; }
.faq-list summary { cursor: pointer; font-weight: 700; }
.faq-list details p { margin-top: 12px; }

.footer { padding: 18px 0 34px; border-top: 1px solid var(--line); }
.footer-row { display: flex; justify-content: space-between; align-items: center; gap: 16px; color: var(--muted); }

.city-page-main, .booking-page-main { padding: 40px 0 70px; }
.city-page-content { display: grid; gap: 18px; }
.city-page-wrap { display: grid; }
.booking-page-grid { padding-top: 24px; }

@media (max-width: 900px) {
  .hero-grid, .highlight-grid, .destination-grid, .experience-grid, .planner-grid, .map-layout, .detail-body, .booking-grid, .field-row { grid-template-columns: 1fr; }
  .split { flex-direction: column; align-items: flex-start; }
}

@media (max-width: 620px) {
  nav { gap: 8px; font-size: 0.84rem; }
  .actions { flex-direction: column; align-items: stretch; }
  .primary, .secondary, .detail-button { width: 100%; }
  .gallery-grid { grid-template-columns: 1fr; }
  .gallery-item, .gallery-item.wide, .gallery-item.tall { grid-column: auto; grid-row: auto; min-height: 180px; }
}
