window.API = {
  reviewStream: function (imageFile, dimensions, onEvent) {
    var form = new FormData();
    form.append("image", imageFile);
    form.append("dimensions", JSON.stringify(dimensions));

    return fetch("/api/review/stream", { method: "POST", body: form }).then(
      function (resp) {
        if (!resp.ok) {
          return resp.json().then(function (err) {
            throw new Error(err.detail || "请求失败 (" + resp.status + ")");
          });
        }
        var reader = resp.body.getReader();
        var decoder = new TextDecoder();
        var buf = "";
        var pending = [];

        function flushPending() {
          while (pending.length > 0) {
            var data = pending.shift();
            onEvent(data);
          }
        }

        function pump() {
          return reader.read().then(function (r) {
            if (r.done) { flushPending(); return; }
            buf += decoder.decode(r.value, { stream: true });
            var lines = buf.split("\n");
            buf = lines.pop();
            for (var i = 0; i < lines.length; i++) {
              var line = lines[i];
              if (line.startsWith("data: ")) {
                try {
                  var data = JSON.parse(line.slice(6));
                  // Status/done/error events fire immediately
                  if (data.step || data.overall_score !== undefined || (data.message && data.message.indexOf("失败") !== -1)) {
                    onEvent(data);
                  } else if (data.text !== undefined) {
                    // Text chunks go through rAF for smooth rendering
                    pending.push(data);
                  }
                } catch (e) {}
              }
            }
            requestAnimationFrame(flushPending);
            return pump();
          });
        }
        return pump();
      }
    );
  },

  review: function (imageFile, dimensions) {
    var form = new FormData();
    form.append("image", imageFile);
    form.append("dimensions", JSON.stringify(dimensions));

    return fetch("/api/review", { method: "POST", body: form }).then(
      function (resp) {
        var contentType = resp.headers.get("content-type") || "";
        if (!resp.ok) {
          // Try to get JSON error detail
          if (contentType.indexOf("application/json") !== -1) {
            return resp.json().then(function (err) {
              throw new Error(err.detail || "请求失败 (" + resp.status + ")");
            });
          }
          // Non-JSON error — likely Nginx error page or network issue
          return resp.text().then(function (text) {
            throw new Error(
              "服务器返回了意外的响应 (HTTP " +
                resp.status +
                ")。请稍后重试。"
            );
          });
        }
        if (contentType.indexOf("application/json") === -1) {
          return resp.text().then(function (text) {
            throw new Error(
              "API 返回了非 JSON 数据。开头: " + text.substring(0, 80)
            );
          });
        }
        return resp.json();
      }
    );
  },

  chat: function (sessionId, message) {
    return fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message: message }),
    }).then(function (resp) {
      var contentType = resp.headers.get("content-type") || "";
      if (!resp.ok) {
        if (contentType.indexOf("application/json") !== -1) {
          return resp.json().then(function (err) {
            throw new Error(err.detail || "请求失败 (" + resp.status + ")");
          });
        }
        return resp.text().then(function (text) {
          throw new Error("服务器错误 (HTTP " + resp.status + ")。请稍后重试。");
        });
      }
      return resp.json();
    });
  },
};
