const panel = { background: "#11151b", border: "1px solid #29313b", borderRadius: 18, padding: 22 };
const muted = { color: "#aab4c0", lineHeight: 1.8 };
const pill = { display: "inline-flex", alignItems: "center", border: "1px solid #394553", borderRadius: 999, padding: "6px 11px", fontSize: 13, color: "#dce4ed", background: "#121922" };

function SectionTitle({ eyebrow, title, text }: { eyebrow: string; title: string; text?: string }) {
  return <div className="section-title"><span className="eyebrow">{eyebrow}</span><h2>{title}</h2>{text && <p>{text}</p>}</div>;
}

export default function Home() {
  return (
    <main dir="rtl">
      <style>{`
        * { box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { margin: 0; background: #090b0f; color: #f4f6f8; font-family: Arial, "Noto Sans Arabic", sans-serif; }
        a { color: inherit; text-decoration: none; }
        .wrap { width: min(1120px, calc(100% - 36px)); margin: 0 auto; }
        .topbar { border-bottom: 1px solid #222a34; background: rgba(9,11,15,.94); }
        .nav { display:flex; align-items:center; justify-content:space-between; gap:18px; min-height:76px; }
        .brand { font-size:19px; font-weight:800; letter-spacing:.08em; direction:ltr; }
        .brand small { display:block; direction:rtl; letter-spacing:0; font-size:11px; color:#9aa7b5; margin-top:4px; font-weight:500; }
        .navlinks { display:flex; gap:20px; flex-wrap:wrap; color:#b6c0cb; font-size:14px; }
        .navlinks a:hover { color:#fff; }
        .hero { padding:76px 0 58px; background: radial-gradient(ellipse at 15% 0%, #172331 0%, #090b0f 56%); }
        .hero-grid { display:grid; grid-template-columns:1.35fr .65fr; gap:36px; align-items:center; }
        .eyebrow { color:#a9c7e6; font-size:12px; letter-spacing:.12em; font-weight:700; }
        h1 { font-size:clamp(36px, 6vw, 68px); line-height:1.13; margin:18px 0; letter-spacing:-.04em; }
        .lead { color:#c2cbd5; font-size:18px; line-height:1.9; max-width:720px; }
        .actions { display:flex; gap:12px; flex-wrap:wrap; margin-top:26px; }
        .btn { display:inline-block; padding:12px 17px; border-radius:11px; font-weight:700; font-size:14px; border:1px solid #45515e; }
        .btn-primary { background:#e7edf4; color:#10151b; border-color:#e7edf4; }
        .status-card { background:linear-gradient(145deg,#151d27,#0e1218); border:1px solid #303b48; border-radius:20px; padding:24px; }
        .status-line { display:flex; justify-content:space-between; gap:12px; padding:13px 0; border-bottom:1px solid #27303a; font-size:14px; }
        .status-line:last-child { border-bottom:0; }
        .state { color:#e5c98b; font-weight:700; }
        section { padding:62px 0; border-top:1px solid #1c232c; }
        .section-title { max-width:760px; margin-bottom:28px; }
        h2 { font-size:clamp(26px,4vw,38px); margin:10px 0 12px; }
        .section-title p { color:#aab4c0; line-height:1.9; margin:0; }
        .grid3 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:15px; }
        .grid2 { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:15px; }
        .card h3 { margin:0 0 10px; font-size:18px; }
        .card p { color:#aab4c0; line-height:1.8; margin:0; font-size:14px; }
        .tagrow { display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }
        .number { color:#91bde7; font-size:12px; font-weight:800; letter-spacing:.1em; margin-bottom:14px; }
        .metrics { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }
        .metric { background:#10151b; border:1px solid #28313b; border-radius:15px; padding:19px; }
        .metric strong { display:block; font-size:30px; margin-bottom:7px; }
        .metric span { color:#aab4c0; font-size:13px; line-height:1.7; }
        .notice { border:1px solid #5b4b2b; background:#1a1710; color:#e5d6b7; padding:17px 19px; border-radius:13px; line-height:1.8; margin-top:18px; }
        .proof { display:flex; align-items:flex-start; justify-content:space-between; gap:15px; padding:16px 0; border-bottom:1px solid #28313b; }
        .proof:last-child { border:0; }
        .proof p { margin:5px 0 0; color:#aab4c0; font-size:13px; line-height:1.7; }
        .label { flex-shrink:0; border-radius:8px; padding:5px 8px; background:#242b33; color:#e5c98b; font-size:11px; font-weight:800; }
        .flow { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; align-items:stretch; }
        .flow .card { position:relative; }
        .code { font-family:ui-monospace, SFMono-Regular, Menlo, monospace; direction:ltr; text-align:left; overflow-wrap:anywhere; color:#d7e3ef; font-size:12px; }
        footer { border-top:1px solid #252d37; padding:28px 0 38px; color:#8f9ba8; font-size:13px; line-height:1.9; }
        @media(max-width:760px) { .hero-grid,.grid3,.grid2,.metrics,.flow { grid-template-columns:1fr; } .hero { padding-top:52px; } .nav { align-items:flex-start; padding:17px 0; flex-direction:column; } .navlinks { gap:13px; } .status-card { margin-top:8px; } section { padding:48px 0; } }
      `}</style>

      <header className="topbar">
        <div className="wrap nav">
          <a href="#top" className="brand">MIZAN CORE<small>نواة حوكمة مستقلة</small></a>
          <nav className="navlinks" aria-label="التنقل الرئيسي">
            <a href="#principles">المبادئ</a><a href="#architecture">المعمارية</a><a href="#evidence">الأدلة</a><a href="#scope">النطاق والحدود</a>
          </nav>
        </div>
      </header>

      <div id="top" className="hero">
        <div className="wrap hero-grid">
          <div>
            <span className="eyebrow">GOVERNANCE · EVIDENCE · AUDIT</span>
            <h1>لا سلطة إلا للمعنى.</h1>
            <p className="lead">MIZAN CORE نواة حوكمة تهدف إلى جعل القرار والتنفيذ قابلين للفحص والتدقيق. لا يُعامل اقتراح الذكاء الاصطناعي كسلطة، ولا تُعتبر النتيجة غير المحسومة نجاحاً.</p>
            <div className="tagrow"><span style={pill}>الدليل قبل الاستنتاج</span><span style={pill}>القرار منفصل عن التنفيذ</span><span style={pill}>سجل قابل للتحقق</span></div>
            <div className="actions"><a className="btn btn-primary" href="#architecture">استكشف المعمارية</a><a className="btn" href="#evidence">راجع حالة الأدلة</a></div>
          </div>
          <aside className="status-card" aria-label="الحالة الحالية">
            <span className="eyebrow">الحالة الحالية · CURRENT STATUS</span>
            <h3 style={{fontSize:22,margin:"13px 0 4px"}}>معاينة عامة للقراءة فقط</h3>
            <p style={muted}>الموقع يعرض معلومات المشروع ولقطة اختبار تاريخية؛ لا ينفّذ عمليات ولا يتصل حالياً بقاعدة البيانات.</p>
            <div className="status-line"><span>واجهة الموقع</span><strong style={{color:"#a7d9b4"}}>منشورة</strong></div>
            <div className="status-line"><span>اتصال قاعدة البيانات</span><strong className="state">غير موصول</strong></div>
            <div className="status-line"><span>التنفيذ عبر الواجهة</span><strong className="state">معطّل</strong></div>
            <div className="status-line"><span>اختبار التزامن الأخير</span><strong className="state">UNKNOWN</strong></div>
          </aside>
        </div>
      </div>

      <section id="principles">
        <div className="wrap">
          <SectionTitle eyebrow="01 / المبادئ" title="قواعد الحوكمة قبل الأتمتة" text="التصميم يفصل بين السياسة والقرار والتنفيذ والأدلة. وجود مكوّن في المعمارية لا يعني وحده أن جميع وظائفه مكتملة أو معتمدة." />
          <div className="grid3">
            <article className="card" style={panel}><div className="number">PRINCIPLE 01</div><h3>الدليل قبل الاستنتاج</h3><p>كل ادعاء عن نتيجة تشغيل يحتاج إلى دليل يمكن مراجعته. غياب الدليل يبقي الحالة غير محسومة.</p></article>
            <article className="card" style={panel}><div className="number">PRINCIPLE 02</div><h3>الذكاء الاصطناعي ليس سلطة</h3><p>مخرجات الذكاء الاصطناعي مقترحات للفحص، وليست إذناً مستقلاً بتنفيذ فعل.</p></article>
            <article className="card" style={panel}><div className="number">PRINCIPLE 03</div><h3>لا إعادة تلقائية للمجهول</h3><p>الحالة UNKNOWN لا تُحوّل إلى نجاح، ولا تُعاد العملية تلقائياً دون سياسة واضحة ومراجعة مناسبة.</p></article>
          </div>
        </div>
      </section>

      <section id="architecture">
        <div className="wrap">
          <SectionTitle eyebrow="02 / المعمارية" title="ثلاث مسؤوليات منفصلة" text="تقسيم المسؤوليات المقترح يمنع خلط وضع السياسة بإصدار القرار وبمراجعة الأدلة." />
          <div className="grid3">
            <article className="card" style={panel}><div className="number">01 · GOVERNANCE</div><h3>MIZAN</h3><p>طبقة الحوكمة: تفحص القواعد والشروط وتحدد ما إذا كان القرار مسموحاً أو مرفوضاً أو غير محسوم.</p><div className="tagrow"><span style={pill}>AUTHORIZED</span><span style={pill}>DENIED</span><span style={pill}>UNRESOLVED</span></div></article>
            <article className="card" style={panel}><div className="number">02 · AUDIT</div><h3>WITNESS</h3><p>طبقة التدقيق: تهدف إلى حفظ الأدلة ومراجعة الاتساق وإظهار ما يمكن إثباته وما لا يزال يحتاج إلى تحقق.</p><div className="tagrow"><span style={pill}>Evidence</span><span style={pill}>Audit trail</span></div></article>
            <article className="card" style={panel}><div className="number">03 · POLICY</div><h3>ORIS</h3><p>طبقة السياسات: تحدد قواعد العمل والقيود التي ينبغي أن يخضع لها القرار والتنفيذ.</p><div className="tagrow"><span style={pill}>Policy</span><span style={pill}>Constraints</span></div></article>
          </div>
          <div className="notice">هذا وصف معماري للمشروع، وليس ادعاءً بأن كل مكوّن متصل حالياً أو يعمل في بيئة إنتاجية.</div>
        </div>
      </section>

      <section id="evidence">
        <div className="wrap">
          <SectionTitle eyebrow="03 / الأدلة" title="حالة الاختبارات المعلنة" text="المعلومات أدناه مستندة إلى لقطة قاعدة الاختبار المؤرخة 27 أكتوبر 2026 وسجل التحقق المتاح. ليست لوحة بيانات حية." />
          <div className="metrics">
            <div className="metric"><strong>101</strong><span>سجل في mizan_ledger<br/>لقطة اختبار تاريخية</span></div>
            <div className="metric"><strong>101</strong><span>سجل في mizan_idempotency<br/>لقطة اختبار تاريخية</span></div>
            <div className="metric"><strong>1</strong><span>سجل رأس في mizan_ledger_head<br/>لقطة اختبار تاريخية</span></div>
            <div className="metric"><strong>6</strong><span>عمليات في mizan_outbox<br/>لقطة اختبار تاريخية</span></div>
          </div>
          <div className="grid2" style={{marginTop:16}}>
            <div style={panel}>
              <h3 style={{marginTop:0}}>سجل التحقق</h3>
              <div className="proof"><div><strong>اتساق سلسلة التجزئة</strong><p>آخر نتيجة متاحة: STRUCTURE_AND_CHAIN_CONSISTENT، مع صفر اختلافات مسجلة في اللقطة.</p></div><span className="label" style={{color:"#a7d9b4"}}>PASS سابق</span></div>
              <div className="proof"><div><strong>اختبار 100 كتابة متزامنة</strong><p>لا توجد نتيجة تشغيل مؤكدة ضمن الأدلة المتاحة.</p></div><span className="label">UNKNOWN</span></div>
              <div className="proof"><div><strong>اختبارات CI بعد آخر إصلاح</strong><p>يلزم الحصول على نتيجة موثقة من تشغيل الاختبارات.</p></div><span className="label">UNKNOWN</span></div>
            </div>
            <div style={panel}>
              <h3 style={{marginTop:0}}>حالات التنفيذ</h3>
              <p style={muted}>تُستخدم الحالات للتمييز بين ما ينتظر التنفيذ وما بدأ وما اكتمل وما فشل أو لم تُحسم نتيجته.</p>
              <div className="tagrow"><span style={pill}>PENDING</span><span style={pill}>CLAIMED</span><span style={pill}>RUNNING</span><span style={pill}>SUCCEEDED</span><span style={pill}>FAILED</span><span style={pill}>UNKNOWN</span><span style={pill}>CANCELLED</span></div>
              <div className="notice">PASS السابق يخص فحص السلسلة في لقطة محددة فقط؛ لا يثبت سلامة النظام كله أو اختبار التزامن.</div>
            </div>
          </div>
        </div>
      </section>

      <section id="scope">
        <div className="wrap">
          <SectionTitle eyebrow="04 / النطاق والحدود" title="ما الذي تعرضه هذه النسخة؟" text="نوضح الحالة الحالية كما هي حتى يستطيع الزائر التمييز بين واجهة العرض، والمكوّنات الأولية، والوظائف التي تحتاج إلى إثبات إضافي." />
          <div className="grid2">
            <article className="card" style={panel}><h3>المكونات الموجودة في سجل المشروع</h3><ul style={{...muted,paddingRight:20}}><li><span className="code">mizan_governance.py</span> — قواعد القرار</li><li><span className="code">mizan_execution_store.py</span> — مخزن التنفيذ</li><li><span className="code">mizan_sqlite_ledger.py</span> — سجل محلي مترابط التجزئة</li><li><span className="code">mizan_reconciliation.py</span> — سياسة المصالحة</li><li><span className="code">mizan_reconciliation_journal.py</span> — سجل أدلة المصالحة</li><li><span className="code">supabase/functions/mizan-api/handler.ts</span> — واجهة أولية لفحص الصحة</li></ul></article>
            <article className="card" style={panel}><h3>الحدود الحالية</h3><ul style={{...muted,paddingRight:20}}><li>قاعدة البيانات غير موصولة بهذه المعاينة.</li><li>لا توجد عمليات تنفيذ فعلية من الواجهة.</li><li>الأرقام المعروضة لقطة تاريخية وليست مباشرة.</li><li>اختبار التزامن واختبارات CI الأخيرة غير محسومة.</li><li>قاعدة الإنتاج خارج نطاق هذه المعاينة.</li></ul></article>
          </div>
          <div className="notice">الحالة UNKNOWN ليست PASS وليست FAIL: معناها أن الدليل المتاح لا يكفي لإصدار حكم.</div>
        </div>
      </section>

      <footer>
        <div className="wrap">
          <div style={{display:"flex",justifyContent:"space-between",gap:18,flexWrap:"wrap"}}>
            <div><strong style={{color:"#e8edf3"}}>MIZAN CORE</strong><div>لا سلطة إلا للمعنى · الدليل قبل الاستنتاج</div></div>
            <div>نسخة تعريفية للقراءة فقط · بيانات الاختبار مؤرخة وليست مباشرة</div>
          </div>
          <p style={{marginTop:18}}>MIZAN CORE مشروع تقني قيد التطوير. هذا الموقع لا يقدم خدمات مالية ولا يتيح تنفيذ عمليات على أنظمة الإنتاج.</p>
        </div>
      </footer>
    </main>
  );
}
