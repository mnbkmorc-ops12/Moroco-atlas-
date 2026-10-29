const destinations = [
  {
    name: "مراكش",
    type: "city",
    tag: "مدينة حمراء",
    image: "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة نابضة بالحياة تجمع بين القصور والحمامات والحدائق والأسواق العريقة.",
    highlights: ["سوق الدباغة", "جامع الفنا", "الحدائق"],
    details: ["مقاهي أنيقة", "مدن تاريخية", "ليالي موسيقية"],
    badge: "مشهد تاريخي"
  },
  {
    name: "الدار البيضاء",
    type: "city",
    tag: "عاصمة الاقتصاد",
    image: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة عصرية ذات طابع عالمي، تجمع بين الواجهة البحرية والهندسة المعمارية المميزة.",
    highlights: ["مسجد الحسن الثاني", "الكورنيش", "العمارة الحديثة"],
    details: ["أفضل مطاعم", "سياحة حضرية", "مناطق عصرية"],
    badge: "عصرية"
  },
  {
    name: "طنجة",
    type: "city",
    tag: "بوابة الشمال",
    image: "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة ساحلية مليئة بالهواء المتوسط والروائح البحرية والثقافة المتعددة.",
    highlights: ["مغارة هرقل", "القصبة", "الواجهة البحرية"],
    details: ["أجواء إيطالية", "مزيج ثقافات", "اشتقاقات بحرية"],
    badge: "شمالية"
  },
  {
    name: "فاس",
    type: "city",
    tag: "مدينة العقول",
    image: "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة عتيقة مشهورة بمدينتها القديمة، أسواقها، وطرقها الملتوية العريقة.",
    highlights: ["فاس البالي", "الدباغة", "المدارس"],
    details: ["تاريخ عميق", "حرف يدوية", "أجواء قديمة"],
    badge: "مغربية أصيلة"
  },
  {
    name: "أكادير",
    type: "coast",
    tag: "ساحل الأطلسي",
    image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة استرخاء وسلاحف بحرية والشواطئ الذهبية والهواء اللطيف على مدار العام.",
    highlights: ["الشواطئ", "نافورة", "الرحلات البحرية"],
    details: ["سياحة بحرية", "مياه هادئة", "مناسب للعائلات"],
    badge: "ساحل"
  },
  {
    name: "الصحراء",
    type: "desert",
    tag: "سهرات الكثبان",
    image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
    description: "رحلة إلى قلب الصحراء، مع كهوف رملية، شوارع عراقية، وليالي تحت النجوم.",
    highlights: ["الكثبان", "الرحلات الليلية", "المخيمات"],
    details: ["نجوم", "أجواء هادئة", "جمال طبيعي"],
    badge: "صحراء"
  },
  {
    name: "شفشاون",
    type: "mountain",
    tag: "جبال الريف",
    image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة زرقاء هادئة محاطة بالجبال، مع أجواء دافئة وقدرات تصوير رائعة.",
    highlights: ["المدينة الزرقاء", "الجبال", "الحرف"],
    details: ["أجواء هادئة", "مشاهد طبيعية", "أزياء محلية"],
    badge: "جبال"
  },
  {
    name: "الرباط",
    type: "city",
    tag: "العاصمة",
    image: "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80",
    description: "مدينة عاصمة متوازنة تجمع بين تاريخها وواجهة البحر والأجواء السياسية والثقافية.",
    highlights: ["قصبة الأوداية", "الميناء", "المتاحف"],
    details: ["اهتمام ثقافي", "ساحل", "حياة عصرية"],
    badge: "عاصمة"
  }
];

const cityMap = {
  "مراكش": "ابدأ بتجولك في الساحة ومتابعة أنشطة السوق ثم استمتع بغروب الشمس في الحدائق.",
  "الدار البيضاء": "توجه إلى كورنيش البحر ومشاهدة مسجد الحسن الثاني في المساء.",
  "طنجة": "استمتع بمشهد المضيق وسوق المدينة القديمة مع نزهة ساحلية.",
  "فاس": "خصص يومًا كاملًا للمدينة القديمة والعناية بالحرف اليدوية التقليدية.",
  "أكادير": "استمتع بالشواطئ، ثم جولة في المدينة ومقاهيها الساحلية.",
  "الصحراء": "خطط لرحلة رملية عند الغروب وتخييم تحت السماء المرصعة بالنجوم.",
  "شفشاون": "قضاء يوم هادئ في الأزقة الزرقاء والاستمتاع بإطلالات الجبال.",
  "الرباط": "استخدم يومًا للاستمتاع بالواجهة البحرية والتاريخ في القصبة.",
};

const destinationGrid = document.getElementById("destinationGrid");
const cityDetail = document.getElementById("cityDetail");
const filters = document.querySelectorAll(".filter");
const itineraryForm = document.getElementById("itineraryForm");
const citySelect = document.getElementById("citySelect");
const tripDuration = document.getElementById("tripDuration");
const itineraryOutput = document.getElementById("itineraryOutput");
const yearNode = document.getElementById("year");
const mapPoints = document.querySelectorAll(".map-point");

function renderDestinationCards(filter = "all") {
  const visible = filter === "all"
    ? destinations
    : destinations.filter((item) => item.type === filter);

  destinationGrid.innerHTML = visible
    .map(
      (destination) => `
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
          </div>
        </article>
      `
    )
    .join("");
}

function renderCityDetail(cityName) {
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
  mapPoints.forEach((point) => {
    const active = point.dataset.city === cityName;
    point.classList.toggle("active", active);
  });
  renderCityDetail(cityName);
}

function populateCitySelect() {
  citySelect.innerHTML = destinations
    .map((city) => `<option value="${city.name}">${city.name}</option>`)
    .join("");
}

function generateItinerary(event) {
  event.preventDefault();

  const city = citySelect.value;
  const days = Number(tripDuration.value);

  const route = [
    `اليوم 1: الوصول إلى ${city} واستقرار الإقامة في قلب المدينة.`,
    `اليوم 2: استكشاف أحياء المدينة والأسواق والتجارب المحلية.`,
    `اليوم 3: زيارة المعالم الأكثر شهرة واستراحة في مكان شهي.`,
    `اليوم 4: جولة طبيعية أو نقطة مشاهدة بديعة في المنطقة.`,
    `اليوم 5: تجربة ثقافية أو سوقيّة مميزة في محيط المدينة.`,
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
    <div class="route-step">
      <strong>المدينة الأساسية</strong>
      <p>${city}</p>
    </div>
    <div class="route-step">
      <strong>معلومة ذكية</strong>
      <p>${cityMap[city] || "استمتع بالأجواء المحلية وكن مرنًا في خطتك."}</p>
    </div>
    ${steps}
  `;
}

filters.forEach((button) => {
  button.addEventListener("click", () => {
    filters.forEach((item) => item.classList.toggle("active", item === button));
    renderDestinationCards(button.dataset.filter);
  });
});

mapPoints.forEach((point) => {
  point.addEventListener("click", () => {
    const selectedCity = point.dataset.city;
    citySelect.value = selectedCity;
    applyMapSelection(selectedCity);
  });
});

itineraryForm.addEventListener("submit", generateItinerary);

renderDestinationCards();
populateCitySelect();
renderCityDetail("مراكش");
applyMapSelection("مراكش");
yearNode.textContent = new Date().getFullYear();
