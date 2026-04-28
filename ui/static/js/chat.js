const API_URL = "http://127.0.0.1:8000/chat";

async function sendMessage() {
    const input = document.getElementById("query-input");
    const container = document.getElementById("chat-container");
    const query = input.value.trim();
    if (!query) return;

    addMessage(query, "user");
    input.value = "";

    const loading = addMessage("...", "assistant");

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query, session_id: "default" })
        });
        const data = await res.json();
        loading.remove();
        if (data.detail) {
            addMessage("错误: " + data.detail, "assistant");
        } else {
            addMessage(data.answer || data.message, "assistant");
        }
    } catch (err) {
        loading.remove();
        addMessage("请求失败: " + err.message, "assistant");
    }
}

function addMessage(content, role) {
    const div = document.createElement("div");
    div.className = "message " + role;
    div.textContent = content;
    document.getElementById("chat-container").appendChild(div);
    return div;
}