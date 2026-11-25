// API Configuration: Uses relative path if behind Nginx (production), or localhost:8000 (local dev)
const API_BASE = window.location.port === "8000" || window.location.port === "3000" || window.location.port === "5500"
  ? "http://localhost:8000"
  : "";

let searchTimeout = null;

// Initial load
document.addEventListener("DOMContentLoaded", () => {
  fetchItems();
  checkActiveNode();
});

async function checkActiveNode() {
  const nodeSpan = document.getElementById("activeNode");
  if (!nodeSpan) return;
  try {
    const res = await fetch(`${API_BASE}/healthz`);
    if (res.ok) {
      const data = await res.json();
      nodeSpan.textContent = data.served_by || "online";
      nodeSpan.style.color = "#4ade80";
    }
  } catch (e) {
    nodeSpan.textContent = "Failover Mode";
    nodeSpan.style.color = "#f87171";
  }
}

function debounceSearch() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetchItems();
  }, 300);
}

async function fetchItems() {
  const search = document.getElementById("searchInput").value;
  const itemType = document.getElementById("typeFilter").value;
  const category = document.getElementById("categoryFilter").value;
  const grid = document.getElementById("itemsGrid");

  grid.innerHTML = '<div class="loading">Loading items from cloud backend...</div>';

  try {
    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (itemType !== "all") params.append("item_type", itemType);
    if (category !== "all") params.append("category", category);

    const response = await fetch(`${API_BASE}/api/items?${params.toString()}`);
    if (!response.ok) throw new Error("Network response was not ok");

    const items = await response.json();
    renderItems(items);
  } catch (error) {
    console.error("Error fetching items:", error);
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: #dc2626;">
        <p>⚠️ Could not connect to API server at <code>${API_BASE || window.location.origin}</code>.</p>
        <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">Ensure the backend container is running on port 8000.</p>
      </div>
    `;
  }
}

function renderItems(items) {
  const grid = document.getElementById("itemsGrid");
  if (!items || items.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #64748b;">
        <p style="font-size: 1.1rem; font-weight: 500;">No items found matching your filters.</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">Try adjusting your search terms or report a new item above.</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = items.map(item => {
    const isFound = item.type === "found";
    const imageUrl = item.image_url.startsWith("http") 
      ? item.image_url 
      : `${API_BASE}${item.image_url}`;

    return `
      <div class="item-card">
        <div class="item-img-container">
          <img src="${imageUrl}" alt="${item.title}" class="item-img" onerror="this.src='https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=500&auto=format&fit=crop&q=60'">
          <span class="badge ${isFound ? 'badge-found' : 'badge-lost'}">${item.type.toUpperCase()}</span>
        </div>
        <div class="item-content">
          <div class="item-category">${item.category}</div>
          <h3 class="item-title">${escapeHtml(item.title)}</h3>
          <div class="item-meta">
            <span>📍 ${escapeHtml(item.location)}</span>
            <span>📅 ${escapeHtml(item.date)}</span>
          </div>
          <p class="item-desc">${escapeHtml(item.description)}</p>
          <div class="item-footer">
            <span style="color: #64748b;">Contact:</span>
            <strong>${escapeHtml(item.contact)}</strong>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function openModal(type) {
  const modal = document.getElementById("reportModal");
  const modalTitle = document.getElementById("modalTitle");
  const typeInput = document.getElementById("formItemType");
  const submitBtn = document.getElementById("submitBtn");

  typeInput.value = type;
  if (type === "lost") {
    modalTitle.textContent = "Report a Lost Item";
    submitBtn.textContent = "Post Lost Report";
    submitBtn.style.backgroundColor = "#dc2626";
  } else {
    modalTitle.textContent = "Report a Found Item";
    submitBtn.textContent = "Post Found Item";
    submitBtn.style.backgroundColor = "#16a34a";
  }

  modal.style.display = "flex";
}

function closeModal() {
  document.getElementById("reportModal").style.display = "none";
  document.getElementById("itemForm").reset();
}

async function submitItem(event) {
  event.preventDefault();
  const submitBtn = document.getElementById("submitBtn");
  submitBtn.disabled = true;
  submitBtn.textContent = "Uploading to Cloud...";

  const formData = new FormData();
  formData.append("title", document.getElementById("formTitle").value);
  formData.append("item_type", document.getElementById("formItemType").value);
  formData.append("category", document.getElementById("formCategory").value);
  formData.append("location", document.getElementById("formLocation").value);
  formData.append("description", document.getElementById("formDescription").value);
  formData.append("contact", document.getElementById("formContact").value);

  const photoFile = document.getElementById("formPhoto").files[0];
  if (photoFile) {
    formData.append("photo", photoFile);
  }

  try {
    const res = await fetch(`${API_BASE}/api/items`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("Failed to post item");

    closeModal();
    fetchItems();
  } catch (error) {
    alert("Error uploading item to cloud: " + error.message);
  } finally {
    submitBtn.disabled = false;
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}
