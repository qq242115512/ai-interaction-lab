window.initChat = function () {
  var input = document.getElementById("chatInput");
  var sendBtn = document.getElementById("chatSendBtn");

  if (sendBtn) {
    sendBtn.addEventListener("click", window.sendMessage);
  }
  if (input) {
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        window.sendMessage();
      }
    });
  }
};

window.sendMessage = function () {
  var input = document.getElementById("chatInput");
  var msg = input ? input.value.trim() : "";
  if (!msg || !window.currentSessionId) return;

  if (msg.length > 500) {
    window.showError("消息过长，请控制在 500 字以内。");
    return;
  }

  window.appendMessage("user", msg);
  if (input) input.value = "";
  if (input) input.disabled = true;

  var sendBtn = document.getElementById("chatSendBtn");
  if (sendBtn) sendBtn.disabled = true;

  var typingEl = window.appendMessage("ai", "思考中...", true);

  window.API.chat(window.currentSessionId, msg)
    .then(function (data) {
      if (typingEl) typingEl.remove();
      window.appendMessage("ai", data.reply, false, data.references);
    })
    .catch(function (err) {
      if (typingEl) typingEl.remove();
      window.appendMessage("ai", "抱歉，回复出了点问题：" + err.message);
    })
    .finally(function () {
      if (input) input.disabled = false;
      if (sendBtn) sendBtn.disabled = false;
      if (input) input.focus();
    });
};

window.appendMessage = function (role, text, isTyping, references) {
  references = references || [];
  isTyping = isTyping || false;

  var container = document.getElementById("chatMessages");
  if (!container) return null;

  var div = document.createElement("div");
  div.className = "chat-msg chat-msg-" + role;

  if (role === "ai") {
    var refsHTML = "";
    if (references.length > 0) {
      refsHTML =
        '<div class="chat-refs">相关原则：' +
        references.map(window.escHtml).join("、") +
        "</div>";
    }
    var bubbleClass = isTyping ? "chat-bubble chat-typing" : "chat-bubble";
    div.innerHTML =
      '<div class="' +
      bubbleClass +
      '">' +
      (isTyping
        ? window.escHtml(text)
        : window.escHtml(text).replace(/\n/g, "<br>")) +
      "</div>" +
      refsHTML;
  } else {
    div.innerHTML =
      '<div class="chat-bubble">' + window.escHtml(text) + "</div>";
  }

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
};
