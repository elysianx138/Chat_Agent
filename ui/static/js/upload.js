const API_BASE = 'http://127.0.0.1:8000';

const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const message = document.getElementById('message');
const fileList = document.getElementById('file-list');
const refreshBtn = document.getElementById('refresh-btn');

uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        showMessage('请选择文件', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        
        if (res.ok) {
            showMessage('上传成功！', 'success');
            fileInput.value = '';
            loadFileList();
        } else {
            showMessage(data.detail || '上传失败', 'error');
        }
    } catch (err) {
        showMessage('请求失败，请检查后端服务', 'error');
    }
});

refreshBtn.addEventListener('click', loadFileList);

async function loadFileList() {
    try {
        const res = await fetch(`${API_BASE}/list`);
        const data = await res.json();
        
        fileList.innerHTML = '';
        const docs = data.documents || [];
        
        if (docs.length === 0) {
            fileList.innerHTML = '<li class="empty">暂无上传文件</li>';
            return;
        }

        docs.forEach(doc => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="file-name">${doc.filename}</span>
                <button class="delete-btn" data-filename="${doc.filename}">删除</button>
            `;
            fileList.appendChild(li);
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const filename = e.target.dataset.filename;
                await deleteFile(filename);
            });
        });
    } catch (err) {
        fileList.innerHTML = '<li class="empty">加载失败</li>';
    }
}

async function deleteFile(filename) {
    if (!confirm(`确定删除 ${filename}？`)) return;

    try {
        const res = await fetch(`${API_BASE}/documents/${filename}`, {
            method: 'DELETE'
        });
        if (res.ok) {
            showMessage('删除成功', 'success');
            loadFileList();
        } else {
            showMessage('删除失败', 'error');
        }
    } catch (err) {
        showMessage('请求失败', 'error');
    }
}

function showMessage(text, type) {
    message.textContent = text;
    message.className = type;
}

loadFileList();