const destinations = [
  {
    name: "مراكش",
    type: "city",
    tag: "مدينة حمراء",
    image: "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة نابضة بالحياة تجمع بين القصور والحمامات والحدائق والأسواق العريقة.",
    highlights: ["سوق الدباغة", "جامع الفنا", "الحدائق"],
    details: ["مقاهي أنيقة", "تجارب ثقافية", "أجواء موسيقية"],
    badge: "مشهد تاريخي",
    summary: "مراكش هي قلب المغرب العاطفي، حيث تتداخل القهوة الساخنة، الأسواق الملونة، والقصور الجذابة في تجربة ثقافية لا تُنسى.",
    experiences: ["جولة في السوق", "جلسة شاي", "رحلة في الأطلس"],
    budget: "متوسط إلى مرتفع",
    bestFor: "العائلات والمؤرخين"
  },
  {
    name: "الدار البيضاء",
    type: "city",
    tag: "عاصمة الاقتصاد",
    image: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة عصرية ذات طابع عالمي، تجمع بين الواجهة البحرية والهندسة المعمارية المميزة.",
    highlights: ["مسجد الحسن الثاني", "الكورنيش", "العمارة الحديثة"],
    details: ["أنشطة بحرية", "مراكز تسوق", "مطاعم فاخرة"],
    badge: "عصرية",
    summary: "الدار البيضاء تمزج بين الحداثة والهوية البحرية، وتقدم تجربة حضرية فاخرة ومريحة للزوار.",
    experiences: ["كورنيش البحر", "متحف", "تجربة طعام"],
    budget: "مرتفع",
    bestFor: "رحلات الأعمال والسياحة العصرية"
  },
  {
    name: "طنجة",
    type: "city",
    tag: "بوابة الشمال",
    image: "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة ساحلية مليئة بالهواء المتوسط والثقافة المتعددة والواجهة البحرية الساحرة.",
    highlights: ["مغارة هرقل", "القصبة", "واجهة المضيق"],
    details: ["مزيج ثقافات", "مناظر بحرية", "أسواق فنية"],
    badge: "شمالية",
    summary: "طنجة هي نقطة الالتقاء بين الثقافات، والمدينة التي تشهد تآلفاً بين البحر والهوية المحيطية.",
    experiences: ["جولة بالمدينة", "مراقبة البحر", "سوق فني"],
    budget: "متوسط",
    bestFor: "السياحة الثقافية"
  },
  {
    name: "فاس",
    type: "city",
    tag: "مدينة العقول",
    image: "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة عتيقة مشهورة بمدينتها القديمة، أسواقها، وطرقها الملتوية العريقة.",
    highlights: ["فاس البالي", "الدباغة", "المدارس"],
    details: ["حرف يدوية", "تاريخ عميق", "أجواء أصلية"],
    badge: "مغر��ية أصيلة",
    summary: "فاس تروي قصة المغرب من خلال الأزقة القديمة، والصناعات الحرفية، والهوية الثقافية العميقة.",
    experiences: ["المدينة القديمة", "الدباغة", "الفن التقليدي"],
    budget: "متوسط",
    bestFor: "المتأملين والمحبين للتاريخ"
  },
  {
    name: "أكادير",
    type: "coast",
    tag: "ساحل الأطلسي",
    image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة استرخاء مع شواطئ طويلة، أجواء دافئة، وسبل راحة ممتازة خلال السنة.",
    highlights: ["الشواطئ", "المنطقة البحرية", "المقاهي"],
    details: ["رحلات بحرية", "أجواء عائلية", "شاطئ هادئ"],
    badge: "ساحل",
    summary: "أكادير رائعة لمن يبحث عن استرخاء على الشواطئ وهدوء الجزر الواعدة في جنوب المغرب.",
    experiences: ["شاطئ", "مطعم بحري", "جلسة بحرية"],
    budget: "متوسط",
    bestFor: "العائلات والسياحة البحرية"
  },
  {
    name: "الصحراء",
    type: "desert",
    tag: "سهرات الكثبان",
    image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
    description: "رحلة إلى قلب الصحراء، مع كهوف رملية، ليالٍ تحت النجوم، ومغامرات عظيمة.",
    highlights: ["الكثبان", "الرحلات الليلية", "المخيمات"],
    details: ["نجوم", "أجواء هادئة", "تجربة فريدة"],
    badge: "صحراء",
    summary: "الصحراء المغربية تُعرّف الزائر بحجم الفضاء، وهدوء الليل، وروح البداوة الأصيلة.",
    experiences: ["ركوب الجمل", "المخيم", "غروب الصحراء"],
    budget: "متوسط إلى مرتفع",
    bestFor: "المغامرين والمصورين"
  },
  {
    name: "شفشاون",
    type: "mountain",
    tag: "جبال الريف",
    image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة زرقاء هادئة محاطة بالجبال، مع أجواء روحية وملامح طبيعية ساحرة.",
    highlights: ["المدينة الزرقاء", "الجبال", "الحرف"],
    details: ["أجواء هادئة", "مناظر طبيعية", "منطقة تصويرية"],
    badge: "جبال",
    summary: "شفشاون تحمل ألوان الطبيعة والهدوء، وتقدم تجربة مميزة في قلب الجبال الشمالية.",
    experiences: ["الممرات الجبلية", "مدينة زرقاء", "جلسة فنجان"],
    budget: "متوسط",
    bestFor: "المصورين والباحثين عن الهدوء"
  },
  {
    name: "الرباط",
    type: "city",
    tag: "العاصمة",
    image: "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة عاصمة متوازنة تجمع بين التاريخ والمنطقة الساحلية والحياة الثقافية.",
    highlights: ["قصبة الأوداية", "الميناء", "المتاحف"],
    details: ["ثقافة", "واجهة بحرية", "أجواء عصرية"],
    badge: "عاصمة",
    summary: "الرباط تقدم توازنًا رائعًا بين الهدوء، التاريخ، والواجهة البحرية المريحة.",
    experiences: ["قصبة", "منتزهات", "متحف"],
    budget: "متوسط",
    bestFor: "رحلات مركزية ومشاهدة المدن"
  }
];

const experiences = [
  { title: "رحلة الأطلس", tag: "مغامرة", description: "استمتع برحلة جبلية متكاملة مع جولات في القرى والحدائق والأماكن الخفية.", icon: "⛰️" },
  { title: "تجربة الجمال في الصحراء", tag: "صحاري", description: "رمل، شروق، وجلسة غروب تحت النجوم مع معسكر فاخر في قلب الصحراء.", icon: "🏜️" },
  { title: "لقاء مع الأسواق المغربية", tag: "ثقافة", description: "اكتشف البهارات، الحرف، والهوية المحلية في أحياء السوق العتيقة.", icon: "🧺" },
  { title: "رحلة ساحلية ناعمة", tag: "بحر", description: "يوم هادئ على الشاطئ مع وجبات بحرية ومناظر شروق ممتعة.", icon: "🌊" }
];

const cityMap = {
  "مراكش": "ابدأ بتجولك في الساحة ومتابعة أنشطة السوق ثم استمتع بالغروب في الحدائق.",
  "الدار البيضاء": "توجه إلى كورنيش البحر ومشاهدة مسجد الحسن الثاني في المساء.",
  "طنجة": "استمتع بمشهد المضيق وسوق المدينة القديمة مع نزهة ساحلية.",
  "فاس": "خصص يومًا كاملًا للمدينة القديمة والعناية بالحرف اليدوية التقليدية.",
  "أكادير": "استمتع بالشواطئ، ثم جولة في المدينة ومقاهيها الساحلية.",
  "الصحراء": "خطط لرحلة رملية عند الغروب وتخييم تحت السماء المرصعة بالنجوم.",
  "شفشاون": "قضاء يوم هادئ في الأزقة الزرقاء والاستمتاع بإطلالات الجبال.",
  "الرباط": "استخدم يومًا للاستمتاع بالواجهة البحرية والتاريخ في القصبة.",
};

const page = document.body.dataset.page || "home";
const destinationGrid = document.getElementById("destinationGrid");
const cityDetail = document.getElementById("cityDetail");
const cityDetailPanel = document.getElementById("cityDetailPanel");
const filters = document.querySelectorAll(".filter");
const citySearch = document.getElementById("citySearch");
const itineraryForm = document.getElementById("itineraryForm");
const citySelect = document.getElementById("citySelect");
const tripDuration = document.getElementById("tripDuration");
const itineraryOutput = document.getElementById("itineraryOutput");
const yearNode = document.getElementById("year");
const mapPoints = document.querySelectorAll(".map-point");
const experienceGrid = document.getElementById("experienceGrid");
const bookingCity = document.getElementById("bookingCity");
const bookingForm = document.getElementById("bookingForm");
const bookingSummary = document.getElementById("bookingSummary");
const cityPageContent = document.getElementById("cityPageContent");

let currentFilter = "all";
let currentSearch = "";

function renderExperienceCards() {
  if (!experienceGrid) return;
  experienceGrid.innerHTML = experiences.map((experience) => `
    <article class="experience-card">
      <span class="tag">${experience.tag}</span>
      <h3>${experience.icon} ${experience.title}</h3>
      <p>${experience.description}</p>
    </article>
  `).join("");
}

function renderDestinationCards(filter = currentFilter, query = currentSearch) {
  if (!destinationGrid) return;

  const visible = destinations.filter((item) => {
    const matchesFilter = filter === "all" || item.type === filter;
    const matchesQuery = !query || item.name.toLowerCase().includes(query.toLowerCase()) || item.description.toLowerCase().includes(query.toLowerCase());
    return matchesFilter && matchesQuery;
  });

  destinationGrid.innerHTML = visible.map((destination) => `
    <article class="destination-card">
      <div class="destination-image" style="background-image: linear-gradient(135deg, rgba(0,0,0,0.15), rgba(0,0,0,0.45)), url('${destination.image}');">
        <span>${destination.tag}</span>
      </div>
      <div class="destination-card-content">
        <h3>${destination.name}</h3>
        <p>${destination.description}</p>
        <div class="destination-meta">
          ${destination.highlights.map((item) => `<span>${item}</span>`).join("")}
        </div>
        <div style="margin-top:16px;">
          <button class="detail-button" data-city="${destination.name}">عرض التفاصيل</button>
        </div>
      </div>
    </article>
  `).join("");

  document.querySelectorAll(".detail-button").forEach((button) => {
    button.addEventListener("click", () => {
      const selectedCity = button.dataset.city;
      window.location.href = `city.html?city=${encodeURIComponent(selectedCity)}`;
    });
  });
}

function renderCityDetailPanel(cityName) {
  if (!cityDetailPanel) return;

  const city = destinations.find((item) => item.name === cityName) || destinations[0];
  cityDetailPanel.innerHTML = `
    <div class="detail-hero" style="background-image: url('${city.image}');">
      <div class="detail-hero-content">
        <span class="badge">${city.badge}</span>
        <h3>${city.name}</h3>
        <p>${city.summary}</p>
      </div>
    </div>
    <div class="detail-body">
      <div class="detail-facts">
        <h4>معلومات أساسية</h4>
        <ul>
          <li>الميزانية: ${city.budget}</li>
          <li>الأفضل لـ: ${city.bestFor}</li>
          <li>الأنشطة: ${city.experiences.join(" • ")}</li>
        </ul>
      </div>
      <div class="detail-experiences">
        <h4>أفضل التجارب</h4>
        <ul>
          ${city.highlights.map((item) => `<li>${item}</li>`).join("")}
        </ul>
      </div>
    </div>
  `;
}

function renderCityDetail(cityName) {
  if (!cityDetail) return;
  const city = destinations.find((item) => item.name === cityName) || destinations[0];
  cityDetail.innerHTML = `
    <span class="badge">${city.badge}</span>
    <h3>${city.name}</h3>
    <p>${city.description}</p>
    <ul>
      ${city.details.map((item) => `<li>${item}</li>`).join("")}
    </ul>
  `;
}

function applyMapSelection(cityName) {
  if (!mapPoints.length) return;
  mapPoints.forEach((point) => {
    const active = point.dataset.city === cityName;
    point.classList.toggle("active", active);
  });
  renderCityDetail(cityName);
  renderCityDetailPanel(cityName);
}

function populateCitySelect() {
  if (citySelect) {
    citySelect.innerHTML = destinations.map((city) => `<option value="${city.name}">${city.name}</option>`).join("");
    citySelect.value = "مراكش";
  }

  if (bookingCity) {
    bookingCity.innerHTML = destinations.map((city) => `<option value="${city.name}">${city.name}</option>`).join("");
    bookingCity.value = "مراكش";
  }
}

function generateItinerary(event) {
  event.preventDefault();
  if (!citySelect || !tripDuration || !itineraryOutput) return;

  const city = citySelect.value;
  const days = Number(tripDuration.value);

  const route = [
    `اليوم 1: الوصول إلى ${city} واستقرار الإقامة في قلب المدينة.`,
    `اليوم 2: استكشاف أحياء المدينة والأسواق والتجارب المحلية.`,
    `اليوم 3: زيارة المعالم الأكثر شهرة واستراحة في مكان شهي.`,
    `اليوم 4: جولة طبيعية أو نقطة مشاهدة بديعة في المنطقة.`,
    `اليوم 5: تجربة ثقافية أو سوقية مميزة في محيط المدينة.`,
    `اليوم 6: استرخاء في المقاهي أو الساحل أو أماكن طبيعية.`,
    `اليوم 7: يوم تسوق ومشاهدة أخيرة قبل مغادرة الرحلة.`,
  ];

  const selectedDays = Math.min(days, route.length);
  const steps = route.slice(0, selectedDays).map((step, index) => `
    <div class="route-step">
      <strong>الخطوة ${index + 1}</strong>
      <p>${step}</p>
    </div>
  `).join("");

  itineraryOutput.innerHTML = `
    <div class="route-step"><strong>المدينة الأساسية</strong><p>${city}</p></div>
    <div class="route-step"><strong>معلومة ذكية</strong><p>${cityMap[city] || "استمتع بالأجواء المحلية وكن مرنًا في خطتك."}</p></div>
    ${steps}
  `;
}

function updateBookingSummary() {
  if (!bookingSummary || !bookingCity) return;

  const city = bookingCity.value;
  const experience = document.getElementById("bookingExperience").value;
  const guests = document.getElementById("bookingGuests").value;
  const date = document.getElementById("bookingDate").value || "لم يتم تحديد التاريخ";

  bookingSummary.innerHTML = `
    <h3>ملخص الطلب</h3>
    <p>تجربتك المفضلة في ${city}</p>
    <div class="summary-box">
      <strong>نوع التجربة:</strong> ${experience}<br />
      <strong>التاريخ:</strong> ${date}<br />
      <strong>عدد الأفراد:</strong> ${guests}
    </div>
  `;
}

function handleBookingSubmit(event) {
  event.preventDefault();
  if (!bookingSummary) return;

  const city = bookingCity.value;
  const experience = document.getElementById("bookingExperience").value;
  const name = document.getElementById("bookingName").value;
  const date = document.getElementById("bookingDate").value;
  const guests = document.getElementById("bookingGuests").value;

  bookingSummary.innerHTML = `
    <h3>تم تأكيد الطلب</h3>
    <div class="summary-box">
      <strong>اسم العميل:</strong> ${name}<br />
      <strong>المدينة:</strong> ${city}<br />
      <strong>التجربة:</strong> ${experience}<br />
      <strong>التاريخ:</strong> ${date}<br />
      <strong>الأفراد:</strong> ${guests}
    </div>
  `;
}

function renderCityPage() {
  if (!cityPageContent) return;
  const params = new URLSearchParams(window.location.search);
  const cityName = params.get("city") || "مراكش";
  const city = destinations.find((item) => item.name === cityName) || destinations[0];

  cityPageContent.innerHTML = `
    <article class="detail-panel">
      <div class="detail-hero" style="background-image: url('${city.image}');">
        <div class="detail-hero-content">
          <span class="badge">${city.badge}</span>
          <h3>${city.name}</h3>
          <p>${city.summary}</p>
        </div>
      </div>
      <div class="detail-body">
        <div class="detail-facts">
          <h4>معلومات أساسية</h4>
          <ul>
            <li>الميزانية: ${city.budget}</li>
            <li>الأفضل لـ: ${city.bestFor}</li>
            <li>الأنشطة: ${city.experiences.join(" • ")}</li>
          </ul>
        </div>
        <div class="detail-experiences">
          <h4>أبرز التجارب</h4>
          <ul>
            ${city.highlights.map((item) => `<li>${item}</li>`).join("")}
          </ul>
        </div>
      </div>
    </article>

    <section class="summary-box">
      <h3 style="margin:0 0 10px;">عن ${city.name}</h3>
      <p>${city.description}</p>
    </section>

    <section class="booking-summary booking-summary-card">
      <h3>خطّة مختصرة</h3>
      <div class="summary-box">
        ${city.details.map((item) => `<div>• ${item}</div>`).join("")}
      </div>
    </section>
  `;
}

if (page === "home") {
  filters.forEach((button) => {
    button.addEventListener("click", () => {
      filters.forEach((item) => item.classList.toggle("active", item === button));
      currentFilter = button.dataset.filter;
      renderDestinationCards(currentFilter, currentSearch);
    });
  });

  if (citySearch) {
    citySearch.addEventListener("input", (event) => {
      currentSearch = event.target.value.trim();
      renderDestinationCards(currentFilter, currentSearch);
    });
  }

  if (itineraryForm) {
    itineraryForm.addEventListener("submit", generateItinerary);
  }

  if (bookingForm) {
    bookingForm.addEventListener("submit", handleBookingSubmit);
    ["bookingCity", "bookingExperience", "bookingGuests", "bookingDate"].forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener("input", updateBookingSummary);
        el.addEventListener("change", updateBookingSummary);
      }
    });
  }

  mapPoints.forEach((point) => {
    point.addEventListener("click", () => {
      const selectedCity = point.dataset.city;
      citySelect.value = selectedCity;
      bookingCity.value = selectedCity;
      applyMapSelection(selectedCity);
      document.getElementById("city-detail-view").scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  renderExperienceCards();
  renderDestinationCards();
  populateCitySelect();
  renderCityDetail("مراكش");
  renderCityDetailPanel("مراكش");
  applyMapSelection("مراكش");
  updateBookingSummary();
}

if (page === "city") {
  renderCityPage();
}

if (page === "booking") {
  populateCitySelect();
  updateBookingSummary();
  bookingForm.addEventListener("submit", handleBookingSubmit);
  ["bookingCity", "bookingExperience", "bookingGuests", "bookingDate"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", updateBookingSummary);
      el.addEventListener("change", updateBookingSummary);
    }
  });
}

if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}
