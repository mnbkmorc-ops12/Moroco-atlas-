const regions = [
  {
    name: "Marrakech",
    label: "Red City",
    badge: "Popular",
    summary:
      "A vibrant maze of souks, riads, and garden courtyards where culture, color, and architecture come alive.",
    details: ["Medina", "Majorelle Garden", "Djemaa el-Fna", "Atlas foothills"],
  },
  {
    name: "Casablanca",
    label: "Atlantic hub",
    badge: "Modern",
    summary:
      "Morocco’s business capital balances contemporary design with a distinctive cosmopolitan coastal identity.",
    details: ["Hassan II Mosque", "Corniche", "Art deco architecture", "Fine dining"],
  },
  {
    name: "Rabat",
    label: "Capital",
    badge: "Historic",
    summary:
      "An elegant capital city where royal heritage, seaside promenades, and intellectual life coexist gracefully.",
    details: ["Kasbah of the Udayas", "Bouregreg", "Museum of History", "Government district"],
  },
  {
    name: "Fes",
    label: "Ancient soul",
    badge: "Heritage",
    summary:
      "One of the oldest imperial cities, famous for its atmospheric medina and profound scholarly traditions.",
    details: ["Fes el-Bali", "Leather tanneries", "Madrasas", "Alaouite heritage"],
  },
  {
    name: "Tangier",
    label: "Gateway to the north",
    badge: "Coastal",
    summary:
      "A city of sea breezes, international influences, and dramatic views over the Strait of Gibraltar.",
    details: ["Caves of Hercules", "Kasbah", "Mediterranean coast", "Cultural crossroads"],
  },
];

const regionList = document.getElementById("regionList");
const regionDetail = document.getElementById("regionDetail");
const yearNode = document.getElementById("year");

function renderRegionButtons(activeName = "Marrakech") {
  regionList.innerHTML = regions
    .map(
      (region) => `
        <button class="region-button ${region.name === activeName ? "active" : ""}" data-region="${region.name}">
          <strong>${region.name}</strong>
          <span>${region.label}</span>
        </button>
      `
    )
    .join("");

  const buttons = document.querySelectorAll(".region-button");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const selected = button.dataset.region;
      renderRegionButtons(selected);
      renderRegionDetail(selected);
    });
  });
}

function renderRegionDetail(name) {
  const region = regions.find((item) => item.name === name) ?? regions[0];

  regionDetail.innerHTML = `
    <span class="badge">${region.badge}</span>
    <h3>${region.name}</h3>
    <p>${region.summary}</p>
    <div class="region-meta">
      ${region.details.map((detail) => `<span>${detail}</span>`).join("")}
    </div>
  `;
}

renderRegionButtons();
renderRegionDetail("Marrakech");
yearNode.textContent = new Date().getFullYear();
