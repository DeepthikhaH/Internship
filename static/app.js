import { Controller, Application } from "@hotwired/stimulus";

class ChatController extends Controller {
  static targets = ["messages", "input", "mode"];
  static values = { endpoint: String };

  connect() {
    this.history = [];
    this.inputTarget.focus();
  }

  handleKeydown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      this.send(event);
    }
  }

  suggest(event) {
    this.inputTarget.value = event.params.prompt;
    this.send(event);
  }

  async send(event) {
    event.preventDefault();
    const message = this.inputTarget.value.trim();
    if (!message || this.sending) return;

    this.sending = true;
    this.appendMessage("user", message);
    this.inputTarget.value = "";
    this.showTyping();

    try {
      const response = await fetch(this.endpointValue, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history: this.history }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Request failed");
      this.history.push({ role: "user", content: message }, { role: "assistant", content: data.reply });
      this.modeTarget.textContent = data.mode === "model" ? "MODEL CONNECTED" : "LOCAL ENGINE";
      this.removeTyping();
      this.appendMessage("assistant", data.reply);
    } catch (error) {
      this.removeTyping();
      this.appendMessage("assistant", `I couldn't reach the backend. ${error.message}`);
    } finally {
      this.sending = false;
      this.inputTarget.focus();
    }
  }

  reset(event) {
    event.preventDefault();
    this.history = [];
    this.messagesTarget.innerHTML = `<article class="message message-assistant welcome-message"><div class="avatar">N</div><div class="message-content"><span class="message-label">NOVA · JUST NOW</span><p>Fresh page, clear mind. What should we explore?</p></div></article>`;
    this.inputTarget.focus();
  }

  appendMessage(role, text) {
    const article = document.createElement("article");
    article.className = `message message-${role}`;
    article.innerHTML = `<div class="avatar">${role === "assistant" ? "N" : "Y"}</div><div class="message-content"><span class="message-label">${role === "assistant" ? "NOVA" : "YOU"} · NOW</span><p></p></div>`;
    article.querySelector("p").textContent = text;
    this.messagesTarget.appendChild(article);
    this.messagesTarget.scrollTop = this.messagesTarget.scrollHeight;
  }

  showTyping() {
    const typing = document.createElement("div");
    typing.className = "typing";
    typing.dataset.typing = "true";
    typing.innerHTML = "<span></span><span></span><span></span>";
    this.messagesTarget.appendChild(typing);
    this.messagesTarget.scrollTop = this.messagesTarget.scrollHeight;
  }

  removeTyping() {
    this.messagesTarget.querySelector("[data-typing]")?.remove();
  }
}

Application.start().register("chat", ChatController);
