const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("userInput");

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = sender === "user" ? "user-msg" : "bot-msg";
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function askBot(question) {
  addMessage(question, "user");

  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  const data = await res.json();
  addMessage(data.answer, "bot");
}

function sendMessage() {
  const question = inputEl.value.trim();
  if (!question) return;
  inputEl.value = "";
  askBot(question);
}

function quickAsk(question) {
  askBot(question);
}
