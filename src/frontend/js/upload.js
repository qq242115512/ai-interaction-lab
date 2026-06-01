window.selectedFile = null;
window.selectedDimensions = new Set();

window.initUpload = function () {
  var zone = document.getElementById("uploadZone");
  var input = document.getElementById("uploadInput");

  if (!zone || !input) return;

  zone.addEventListener("click", function () {
    input.click();
  });

  zone.addEventListener("dragover", function (e) {
    e.preventDefault();
    zone.classList.add("drag-over");
  });

  zone.addEventListener("dragleave", function () {
    zone.classList.remove("drag-over");
  });

  zone.addEventListener("drop", function (e) {
    e.preventDefault();
    zone.classList.remove("drag-over");
    var file = e.dataTransfer.files[0];
    if (file) window.setFile(file);
  });

  input.addEventListener("change", function () {
    if (input.files[0]) window.setFile(input.files[0]);
  });

  // Dimension cards
  document.querySelectorAll(".dimension-card").forEach(function (card) {
    card.addEventListener("click", function () {
      var dim = card.getAttribute("data-dimension");
      if (window.selectedDimensions.has(dim)) {
        window.selectedDimensions.delete(dim);
        card.classList.remove("selected");
      } else {
        window.selectedDimensions.add(dim);
        card.classList.add("selected");
      }
      window.updateSubmitBtn();
    });
  });
};

window.setFile = function (file) {
  if (!file.type.match(/^image\//)) {
    window.showError("请上传 PNG、JPG 或 WebP 格式的图片。");
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    window.showError("图片不能超过 10MB。");
    return;
  }
  window.selectedFile = file;

  var reader = new FileReader();
  reader.onload = function (e) {
    var img = document.getElementById("previewImg");
    if (img) img.src = e.target.result;
  };
  reader.readAsDataURL(file);

  var name = document.getElementById("previewName");
  var size = document.getElementById("previewSize");
  var placeholder = document.getElementById("uploadPlaceholder");
  var preview = document.getElementById("uploadPreview");
  var zone = document.getElementById("uploadZone");

  if (name) name.textContent = file.name;
  if (size) size.textContent = (file.size / 1024).toFixed(0) + " KB";
  if (placeholder) placeholder.style.display = "none";
  if (preview) preview.style.display = "flex";
  if (zone) zone.classList.add("has-image");

  window.updateSubmitBtn();
};

window.removeFile = function () {
  window.selectedFile = null;
  var input = document.getElementById("uploadInput");
  if (input) input.value = "";

  var placeholder = document.getElementById("uploadPlaceholder");
  var preview = document.getElementById("uploadPreview");
  var zone = document.getElementById("uploadZone");

  if (placeholder) placeholder.style.display = "";
  if (preview) preview.style.display = "none";
  if (zone) zone.classList.remove("has-image");

  window.updateSubmitBtn();
};

window.updateSubmitBtn = function () {
  var btn = document.getElementById("submitBtn");
  if (btn) {
    btn.disabled = !window.selectedFile || window.selectedDimensions.size === 0;
  }
};
