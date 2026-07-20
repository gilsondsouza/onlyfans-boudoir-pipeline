const modelsGrid = document.getElementById("models-grid");
const modelsCount = document.getElementById("models-count");
const modelSelect = document.getElementById("model-select");
const runBtn = document.getElementById("run-pipeline");
const dryRun = document.getElementById("dry-run");
const stepsEl = document.getElementById("pipeline-steps");
const summaryEl = document.getElementById("pipeline-summary");
const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const resetChat = document.getElementById("reset-chat");
const healthEl = document.getElementById("health");

const SESSION_ID = "dashboard";
let selectedModel = "";

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

function selectModel(name) {
  selectedModel = name;
  modelSelect.value = name;
  runBtn.disabled = !name;
  document.querySelectorAll(".model-card").forEach((card) => {
    card.classList.toggle("active", card.dataset.name === name);
  });
}

function renderModels(models) {
  modelsCount.textContent = `${models.length} ativos`;
  modelsGrid.innerHTML = "";
  modelSelect.innerHTML = `<option value="">Escolha um modelo…</option>`;

  for (const model of models) {
    const option = document.createElement("option");
    option.value = model.name;
    option.textContent = model.display_name;
    modelSelect.appendChild(option);

    const card = document.createElement("button");
    card.type = "button";
    card.className = "model-card";
    card.dataset.name = model.name;
    card.innerHTML = `
      <h3>${model.display_name}</h3>
      <p class="model-meta">${model.persona.aesthetic.replaceAll("_", " ")} · ${model.posting.frequency}</p>
      <p class="model-meta">USD ${Number(model.pricing.subscription_usd).toFixed(2)} · pico ${model.posting.peak_hours.map((h) => `${h}h`).join(", ")}</p>
      <div class="swatches">
        ${(model.style.color_palette || [])
          .slice(0, 5)
          .map((c) => `<span class="swatch" style="background:${c}" title="${c}"></span>`)
          .join("")}
      </div>
    `;
    card.addEventListener("click", () => selectModel(model.name));
    modelsGrid.appendChild(card);
  }
}

function renderSteps(steps) {
  stepsEl.hidden = false;
  stepsEl.innerHTML = steps
    .map(
      (step) => `
      <div class="step">
        <span class="step-status ${step.status}">${step.status}</span>
        <div>
          <strong>${step.name}</strong>
          <div class="muted">${step.message || "—"}</div>
        </div>
      </div>`
    )
    .join("");
}

function addBubble(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
}

modelSelect.addEventListener("change", () => {
  selectModel(modelSelect.value);
});

runBtn.addEventListener("click", async () => {
  if (!selectedModel) return;
  runBtn.disabled = true;
  runBtn.textContent = "Executando…";
  stepsEl.hidden = true;
  summaryEl.hidden = true;
  try {
    const result = await api("/api/pipeline/run", {
      method: "POST",
      body: JSON.stringify({
        model_name: selectedModel,
        dry_run: dryRun.checked,
      }),
    });
    renderSteps(result.steps);
    summaryEl.hidden = false;
    summaryEl.textContent = result.summary;
  } catch (err) {
    summaryEl.hidden = false;
    summaryEl.textContent = `Erro: ${err.message}`;
  } finally {
    runBtn.disabled = !selectedModel;
    runBtn.textContent = "Executar";
  }
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;
  addBubble("user", message);
  chatInput.value = "";
  try {
    const data = await api("/api/agent/chat", {
      method: "POST",
      body: JSON.stringify({ message, session_id: SESSION_ID }),
    });
    addBubble("agent", data.reply);
  } catch (err) {
    addBubble("agent", `Erro: ${err.message}`);
  }
});

resetChat.addEventListener("click", async () => {
  await api("/api/agent/reset", {
    method: "POST",
    body: JSON.stringify({ session_id: SESSION_ID }),
  });
  chatLog.innerHTML = "";
  addBubble("agent", "Conversa reiniciada. Como posso ajudar?");
});

async function boot() {
  try {
    const health = await api("/api/health");
    healthEl.textContent = `API ${health.status} · localhost:8000`;
    const models = await api("/api/models");
    renderModels(models);
    addBubble("agent", "Olá — sou o agente do Boudoir Pipeline. Pergunte ou rode o pipeline ao lado.");
  } catch (err) {
    healthEl.textContent = `API indisponível: ${err.message}`;
    modelsGrid.innerHTML = `<p class="muted">Falha ao carregar modelos.</p>`;
  }
}

boot();
