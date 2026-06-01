window.showError = function (msg) {
  var banner = document.getElementById("errorBanner");
  banner.textContent = msg;
  banner.classList.add("active");
  setTimeout(function () {
    banner.classList.remove("active");
  }, 6000);
};

window.escHtml = function (str) {
  if (!str) return "";
  var div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
};

window.resetAll = function () {
  window.selectedFile = null;
  document.getElementById("uploadInput").value = "";
  document.getElementById("uploadPlaceholder").style.display = "";
  document.getElementById("uploadPreview").style.display = "none";
  document.getElementById("uploadZone").classList.remove("has-image");

  window.selectedDimensions.clear();
  document.querySelectorAll(".dimension-card").forEach(function (c) {
    c.classList.remove("selected");
  });

  document.getElementById("reviewResults").classList.remove("active");
  document.getElementById("dimensionsContainer").innerHTML = "";
  document.getElementById("chatSection").style.display = "none";
  document.getElementById("chatMessages").innerHTML = "";
  document.getElementById("errorBanner").classList.remove("active");
  document.getElementById("loadingOverlay").classList.remove("active");
  window.updateSubmitBtn();
  window.currentSessionId = null;
  window.scrollTo({ top: 0, behavior: "smooth" });
};

window.startReview = function () {
  var file = window.selectedFile;
  var dims = window.selectedDimensions;

  if (!file || dims.size === 0) {
    window.showError("请先上传设计截图并选择至少一个评审维度。");
    return;
  }

  // Hide previous results
  document.getElementById("reviewResults").classList.remove("active");
  document.getElementById("chatSection").style.display = "none";
  document.getElementById("errorBanner").classList.remove("active");

  // Show loading
  var loading = document.getElementById("loadingOverlay");
  var stepVisual = document.getElementById("loadingStepVisual");
  var stepReview = document.getElementById("loadingStepReview");
  var streamContainer = document.getElementById("streamTextContainer");
  var streamText = document.getElementById("streamText");

  loading.classList.add("active");
  var visualEl = document.getElementById("loadingStepVisual");
  var reviewEl = document.getElementById("loadingStepReview");
  var streamContainer = document.getElementById("streamTextContainer");
  var streamText = document.getElementById("streamText");

  visualEl.textContent = "正在连接 AI 视觉引擎...";
  visualEl.classList.remove("done");
  reviewEl.textContent = "";
  reviewEl.classList.remove("done");
  streamContainer.style.display = "block";
  streamText.textContent = "";
  document.getElementById("loadingOverlay").scrollIntoView({ behavior: "smooth" });

  var btn = document.getElementById("submitBtn");
  btn.disabled = true;
  btn.textContent = "评审中...";
  var t0 = Date.now();

  window.API.reviewStream(file, Array.from(dims), function (event) {
    if (event.step === "visual") {
      visualEl.textContent = "AI 正在识别设计元素... (GLM-4V 视觉分析)";
    } else if (event.step === "visual_done") {
      visualEl.textContent = "设计元素识别完成 ✓";
      visualEl.classList.add("done");
      reviewEl.textContent = "AI 正在生成评审报告...";
    } else if (event.step === "review") {
      reviewEl.textContent = "DeepSeek 流式生成中...";
    } else if (event.step === "retry") {
      reviewEl.textContent = event.message;
    } else if (event.step === "parsing") {
      reviewEl.textContent = "正在整理评审报告...";
    } else if (event.text !== undefined) {
      streamText.textContent += event.text;
      streamText.scrollTop = streamText.scrollHeight;
    } else if (event.overall_score !== undefined) {
      var elapsed = ((Date.now() - t0) / 1000).toFixed(1);
      reviewEl.textContent = "评审完成 (耗时 " + elapsed + " 秒)";
      reviewEl.classList.add("done");
      window.currentSessionId = event.session_id;

      setTimeout(function () {
        window.renderReview({
          session_id: event.session_id,
          overall_score: event.overall_score,
          dimensions: event.dimensions,
        });
        btn.disabled = false;
        btn.textContent = "开始评审";
      }, 300);
    } else if (event.message && event.message.indexOf("失败") !== -1) {
      loading.classList.remove("active");
      window.showError(event.message || "出了点问题，请重试。");
      btn.disabled = false;
      btn.textContent = "开始评审";
    }
  }).catch(function (err) {
    loading.classList.remove("active");
    window.showError(err.message || "出了点问题，请重试。");
    btn.disabled = false;
    btn.textContent = "开始评审";
  });
};

document.addEventListener("DOMContentLoaded", function () {
  window.initUpload();
  window.initChat();

  var submitBtn = document.getElementById("submitBtn");
  if (submitBtn) {
    submitBtn.addEventListener("click", window.startReview);
  }
});
