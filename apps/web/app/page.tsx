const principles = [
  { code: "01", title: "الدليل قبل الاستنتاج", detail: "لا يتحول الادعاء إلى حقيقة دون دليل قابل للفحص." },
  { code: "02", title: "UNKNOWN يبقى UNKNOWN", detail: "غياب الدليل لا يُفسَّر على أنه نجاح أو فشل." },
  { code: "03", title: "لا إعادة تلقائية", detail: "الحالة غير المحسومة تحتاج إلى مصالحة موثقة قبل أي إجراء جديد." }
];

const decisionStates = [
  { code: "AUTHORIZED", title: "مصرّح", detail: "لا تعني السماح بالتنفيذ إلا بعد تحقق القاعدة والدليل والصلاحية.", tone: "state-authorized" },
  { code: "DENIED", title: "مرفوض", detail: "القاعدة تمنع الطلب؛ لا يجوز تجاوز الرفض من الواجهة.", tone: "state-denied" },
  { code: "UNRESOLVED", title: "غير محسوم", detail: "الدليل غير كافٍ. لا تنفيذ ولا إعادة تلقائية؛ يلزم تحقق مستقل.", tone: "state-unresolved" }
];

const executionStates = [
  "PENDING", "CLAIMED", "RUNNING", "SUCCEEDED", "FAILED", "UNKNOWN", "CANCELLED"
];

export default function Home() {
  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="MIZAN CORE الرئيسية">
          <span className="brand-mark">م</span>
          <span><strong>MIZAN CORE</strong><small>نواة الحوكمة المستقلة</small></span>
        </a>
        <span className="environment"><i /> وضع المعاينة · لا تنفيذ</span>
      </header>

      <section className="hero">
        <p className="eyebrow">GOVERNANCE · EVIDENCE · AUDIT</p>
        <h1>لا سلطة إلا <em>للمعنى</em></h1>
        <p className="intro">كل قرار يحتاج إلى قاعدة صريحة ودليل قابل للتحقق وسجل تدقيق. هاد الواجهة كتشرح نموذج الحوكمة؛ ماشي اتصال حي بقاعدة البيانات، وما كتمنح حتى صلاحية للتنفيذ.</p>
        <div className="status-row">
          <div className="status-card"><span>حالة الواجهة</span><strong>جاهزة للمعاينة</strong></div>
          <div className="status-card"><span>اتصال API</span><strong className="muted">غير موصول</strong></div>
          <div className="status-card"><span>التنفيذ الفعلي</span><strong>معطّل</strong></div>
        </div>
      </section>

      <section className="section-heading">
        <div><p className="eyebrow">DECISION GATE</p><h2>حالات القرار</h2></div>
        <span className="count">نموذج الحوكمة · غير حي</span>
      </section>
      <section className="decision-grid" aria-label="حالات القرار">
        {decisionStates.map((item) => (
          <article className="decision-card" key={item.code}>
            <span className={`decision-code ${item.tone}`}>{item.code}</span>
            <h3>{item.title}</h3>
            <p>{item.detail}</p>
          </article>
        ))}
      </section>

      <section className="section-heading execution-heading">
        <div><p className="eyebrow">EXECUTION LIFECYCLE</p><h2>دورة حالة التنفيذ</h2></div>
        <span className="count">عرض توضيحي فقط</span>
      </section>
      <section className="execution-panel">
        <p>هاد الحالات جزء من النموذج المستهدف، وماشي سجل عمليات حي. الحالة UNKNOWN ما كتعاودش تلقائياً؛ خاص المصالحة بالدليل قبل أي قرار جديد.</p>
        <div className="state-list">
          {executionStates.map((state) => <span key={state}>{state}</span>)}
        </div>
      </section>

      <section className="section-heading rules-heading">
        <div><p className="eyebrow">NON-NEGOTIABLE RULES</p><h2>قواعد لا يجوز تجاوزها</h2></div>
        <span className="count">03 مبادئ</span>
      </section>
      <section className="principles">
        {principles.map((item) => (
          <article className="principle" key={item.code}>
            <span className="principle-code">{item.code}</span>
            <div><h3>{item.title}</h3><p>{item.detail}</p></div>
            <span className="arrow" aria-hidden="true">↙</span>
          </article>
        ))}
      </section>
      <footer><span>MIZAN CORE · Recovery Workspace</span><span>القرار يحتاج إلى دليل مستقل</span></footer>
    </main>
  );
}
