const principles = [
  { code: "01", title: "الدليل قبل الاستنتاج", detail: "لا يتحول الادعاء إلى حقيقة دون دليل قابل للفحص." },
  { code: "02", title: "UNKNOWN يبقى UNKNOWN", detail: "غياب الدليل لا يُفسَّر على أنه نجاح أو فشل." },
  { code: "03", title: "لا إعادة تلقائية", detail: "الحالة غير المحسومة تحتاج إلى مصالحة موثقة قبل أي إجراء جديد." }
];

export default function Home() {
  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="MIZAN CORE الرئيسية">
          <span className="brand-mark">م</span>
          <span><strong>MIZAN CORE</strong><small>نواة الحوكمة المستقلة</small></span>
        </a>
        <span className="environment"><i /> وضع المعاينة</span>
      </header>

      <section className="hero">
        <p className="eyebrow">GOVERNANCE · EVIDENCE · AUDIT</p>
        <h1>لا سلطة إلا <em>للمعنى</em></h1>
        <p className="intro">كل تنفيذ يحتاج إلى قاعدة صريحة، ودليل قابل للتحقق، وسجل تدقيق. هذه الواجهة هي نقطة انطلاق للحوكمة؛ وليست دليلاً على اتصالها بخدمات الإنتاج.</p>
        <div className="status-row">
          <div className="status-card"><span>حالة الواجهة</span><strong>جاهزة للمعاينة</strong></div>
          <div className="status-card"><span>اتصال API</span><strong className="muted">غير موصول بعد</strong></div>
          <div className="status-card"><span>مصدر القرار</span><strong>قواعد + أدلة</strong></div>
        </div>
      </section>

      <section className="section-heading">
        <div><p className="eyebrow">GOVERNANCE RULES</p><h2>قواعد لا يجوز تجاوزها</h2></div>
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
