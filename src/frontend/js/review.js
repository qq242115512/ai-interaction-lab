window.currentSessionId = null;

window.scoreClass = function (score) {
  if (score >= 8) return "high";
  if (score >= 5) return "mid";
  return "low";
};

window.renderReview = function (data) {
  window.currentSessionId = data.session_id;

  var overallEl = document.getElementById("overallNumber");
  if (overallEl) {
    overallEl.textContent = data.overall_score.toFixed(1);
  }

  var container = document.getElementById("dimensionsContainer");
  if (!container) return;
  container.innerHTML = "";

  data.dimensions.forEach(function (dim) {
    var card = document.createElement("div");
    card.className = "dimension-card-result";

    var findingsHTML = "";
    dim.findings.forEach(function (f) {
      var badgeText = f.type === "issue" ? "可改进" : "亮点";
      findingsHTML +=
        '<div class="finding-item">' +
        '<div class="finding-header">' +
        '<span class="finding-badge ' +
        f.type +
        '">' +
        badgeText +
        "</span>" +
        '<span class="finding-title">' +
        window.escHtml(f.title) +
        "</span>" +
        "</div>" +
        '<div class="finding-desc">' +
        window.escHtml(f.description) +
        "</div>" +
        '<div class="principle-card">' +
        '<div class="principle-name">' +
        window.escHtml(f.principle.name) +
        "</div>" +
        '<div class="principle-brief">' +
        window.escHtml(f.principle.brief) +
        "</div>" +
        '<details class="principle-detail">' +
        "<summary>展开讲解</summary>" +
        "<p><strong>通俗解释：</strong>" +
        window.escHtml(f.principle.explanation) +
        "</p>" +
        "<p><strong>在你的设计里：</strong>" +
        window.escHtml(f.principle.application) +
        "</p>" +
        "<p><strong>改进方向：</strong>" +
        window.escHtml(f.principle.suggestion) +
        "</p>" +
        "</details>" +
        "</div>" +
        "</div>";
    });

    card.innerHTML =
      '<div class="dim-header">' +
      '<span class="dim-name">' +
      window.escHtml(dim.name) +
      "</span>" +
      '<span class="dim-score ' +
      window.scoreClass(dim.score) +
      '">' +
      dim.score +
      "/10</span>" +
      "</div>" +
      '<div class="dim-summary">' +
      window.escHtml(dim.summary) +
      "</div>" +
      findingsHTML;

    container.appendChild(card);
  });

  // Show results, hide loading
  var loading = document.getElementById("loadingOverlay");
  if (loading) loading.classList.remove("active");

  var results = document.getElementById("reviewResults");
  if (results) results.classList.add("active");

  var chatSec = document.getElementById("chatSection");
  if (chatSec) chatSec.style.display = "block";

  var chatMsgs = document.getElementById("chatMessages");
  if (chatMsgs) chatMsgs.innerHTML = "";

  // Scroll to results
  if (results) {
    results.scrollIntoView({ behavior: "smooth" });
  }
};
