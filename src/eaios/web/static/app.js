const messages = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const sendButton = document.getElementById("send");

function addMessage(text, kind) {
  const div = document.createElement("div");
  div.className = "message " + kind;
  div.textContent = text;  // plain text only: never run answer content as code
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";
  sendButton.disabled = true;

  try {
    const response = await fetch("/v1/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await response.json();

    if (response.ok) {
      addMessage(data.answer, "assistant");
    } else if (response.status === 422) {
      addMessage("Your question could not be accepted. Check that it is not empty or too long.", "error");
    } else {
      addMessage(data.detail || "Something went wrong. Please try again.", "error");
    }
  } catch {
    addMessage("Could not reach the server. Please try again.", "error");
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
});