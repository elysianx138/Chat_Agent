const API_URL = '/chat';
const UPLOAD_URL = '/upload';
const LIST_URL = '/list';
const DELETE_URL = '/delete';
let sessionId = 'default';

const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typing');
const welcome = document.getElementById('welcome');

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

function showTyping() {
    if (welcome) {
        welcome.style.display = 'none';
    }
    typingIndicator.classList.add('active');
    messagesContainer.appendChild(typingIndicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTyping() {
    typingIndicator.classList.remove('active');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function insertSkill(skill) {
    userInput.value = skill + ' ';
    userInput.focus();
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
}

window.insertSkill = insertSkill;

async function sendMessage() {
    const content = userInput.value.trim();
    if (!content) return;

    userInput.value = '';
    userInput.style.height = 'auto';

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
        <div class="avatar user">U</div>
        <div class="bubble">${escapeHtml(content)}</div>
    `;
    messagesContainer.appendChild(messageDiv);

    sendBtn.disabled = true;
    showTyping();

    try {
        const response = await fetch(window.location.origin + API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: content,
                session_id: sessionId
            }),
        });

        const raw = await response.text();
        let data = null;
        try {
            data = raw ? JSON.parse(raw) : {};
        } catch (parseErr) {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${raw.slice(0, 200)}`);
            }
            throw new Error(`Invalid JSON response: ${raw.slice(0, 200)}`);
        }

        if (!response.ok) {
            const detail = data?.detail || data?.message || `HTTP ${response.status}`;
            throw new Error(detail);
        }

        hideTyping();

        if (data.answer) {
            const aiMessageDiv = document.createElement('div');
            aiMessageDiv.className = 'message ai';
            aiMessageDiv.innerHTML = `
                <div class="avatar ai">AI</div>
                <div class="bubble"></div>
            `;
            aiMessageDiv.querySelector('.bubble').innerHTML = marked.parse(data.answer);
            messagesContainer.appendChild(aiMessageDiv);
        } else {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'message ai';
            errorDiv.innerHTML = `
                <div class="avatar ai">AI</div>
                <div class="bubble">No answer returned by backend.</div>
            `;
            messagesContainer.appendChild(errorDiv);
        }

        sessionId = data.session_id || sessionId;
    } catch (error) {
        hideTyping();
        const errorMsgDiv = document.createElement('div');
        errorMsgDiv.className = 'message ai';
        const safeMsg = escapeHtml(error?.message || 'unknown error');
        errorMsgDiv.innerHTML = `
            <div class="avatar ai">AI</div>
            <div class="bubble">请求失败：${safeMsg}</div>
        `;
        messagesContainer.appendChild(errorMsgDiv);
        console.error('Error:', error);
    }

    sendBtn.disabled = false;
    userInput.focus();
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

marked.setOptions({
    breaks: true,
    gfm: true
});

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    document.querySelector(`.tab-btn[onclick="switchTab('${tab}')"]`).classList.add('active');
    document.getElementById(tab).classList.add('active');

    if (tab === 'knowledge') {
        loadDocuments();
    }
}

async function uploadFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const uploadBtn = document.querySelector('.upload-btn');
    const uploadText = document.getElementById('uploadText');
    uploadBtn.disabled = true;
    uploadText.innerHTML = '<span class="loading-spinner"></span> 涓婁紶涓?..';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(window.location.origin + UPLOAD_URL, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            loadDocuments();
        } else {
            alert('涓婁紶澶辫触');
        }
    } catch (error) {
        alert('涓婁紶澶辫触: ' + error.message);
    }

    uploadBtn.disabled = false;
    uploadText.textContent = '涓婁紶 Markdown';
    event.target.value = '';
}

async function loadDocuments() {
    try {
        const response = await fetch(window.location.origin + LIST_URL);
        const data = await response.json();
        renderDocuments(data.documents || []);
    } catch (error) {
        console.error('Failed to load documents:', error);
    }
}

function renderDocuments(documents) {
    const kbList = document.getElementById('kbList');
    
    if (documents.length === 0) {
        kbList.innerHTML = `
            <div class="kb-empty">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p>鏆傛棤鏂囨。锛岃涓婁紶 Markdown 鏂囦欢</p>
            </div>
        `;
        return;
    }

    kbList.innerHTML = documents.map(doc => `
        <div class="kb-card">
            <div class="kb-card-name">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                ${doc.filename}
            </div>
            <div class="kb-card-time">鏇存柊鏃堕棿: ${formatDate(doc.updated_at)}</div>
            <div class="kb-card-actions">
                <button class="kb-action-btn delete" onclick="deleteDocument('${doc.filename}')">鍒犻櫎</button>
            </div>
        </div>
    `).join('');
}

function formatDate(dateStr) {
    if (!dateStr) return '鏈煡';
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

async function deleteDocument(filename) {
    if (!confirm(`纭畾瑕佸垹闄?"${filename}" 鍚楋紵`)) return;

    try {
        const response = await fetch(`${window.location.origin}${DELETE_URL}/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadDocuments();
        } else {
            alert('鍒犻櫎澶辫触');
        }
    } catch (error) {
        alert('鍒犻櫎澶辫触: ' + error.message);
    }
}

window.handleKeyDown = handleKeyDown;
window.sendMessage = sendMessage;
window.switchTab = switchTab;
window.uploadFile = uploadFile;
window.deleteDocument = deleteDocument;
window.loadDocuments = loadDocuments;
