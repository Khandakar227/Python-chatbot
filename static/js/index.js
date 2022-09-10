/**
 * @type {HTMLFormElement}
 */
const form = document.getElementById("msg-box");
/**
 * @type {HTMLInputElement}
 */
const messageInput = document.getElementById("msg-input");
const messagesBox = document.querySelector('[data-name="messages"]');
const notifier = document.getElementById("notifier");
console.dir(messagesBox.children[0]);
form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);
  
  messagesBox.appendChild(createMessageElement(data.message, "user"));
  // remove input value
  messageInput.value = "";
  // Send message
  const message = encodeURIComponent(data.message);

  const res = await fetch(`/api/chat?message=${message}`);

  if (!res.ok) {
    notifier.textContent = "An error occured...";
    return;
  }
  /**
   * @type {string}
   */
  responseText = await res.text();
  messagesBox.appendChild(createMessageElement(responseText));
  messagesBox.scrollTo(0, messagesBox.scrollHeight);

  console.log(data);
});
/**
 * @param {string} textMessage
 * @param {string} sender
 */
function createMessageElement(textMessage, sender = "bot") {
  const message = document.createElement("div");
  const img = document.createElement("img");
  const text = document.createElement("p");

  message.className = "message shadow rounded";
  message.dataset["sender"] = sender;

  img.src =
    sender == "bot" ? "/static/assets/bot-avatar.jpg" : "/static/assets/user-avatar.jpeg";
  img.alt = sender == "bot" ? "bot" : "user";
  img.className = "avatar";

  text.textContent = textMessage;

  if (sender == "bot") {
    message.appendChild(img);
    message.appendChild(text);
  } else {
    message.appendChild(text);
    message.appendChild(img);
  }
  return message;
}
