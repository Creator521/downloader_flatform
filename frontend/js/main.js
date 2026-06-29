// Mobile Menu Logic
function toggleMenu() {
    document.querySelector('.nav-links').classList.toggle('active');
}

// Paste Button Logic
async function handlePaste() {
    try {
        const text = await navigator.clipboard.readText();
        const input = document.getElementById('urlInput');
        input.value = text;
        input.focus();
    } catch (err) {
        console.error('Failed to read clipboard contents: ', err);
        alert('Could not paste from clipboard. Please paste manually.');
    }
}

// Download/Preview Logic
async function handleDownload(e) {
    e.preventDefault();
    const url = document.getElementById('urlInput').value;
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const error = document.getElementById('error');

    if (!url) return;

    // Basic URL validation
    try {
        const parsedUrl = new URL(url);
        if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
            error.innerText = 'Please enter a valid HTTP or HTTPS URL.';
            error.style.display = 'block';
            return;
        }
    } catch (e) {
        error.innerText = 'Please enter a valid URL (e.g., https://www.youtube.com/watch?v=...)';
        error.style.display = 'block';
        return;
    }

    // Reset UI
    loading.style.display = 'flex';
    result.style.display = 'none';
    error.style.display = 'none';
    if(document.getElementById('status-msg')) document.getElementById('status-msg').style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('url', url);

        const res = await fetch('/preview', {
            method: 'POST',
            body: formData
        });

        const rawText = await res.text();
        let data;
        try {
            data = JSON.parse(rawText);
        } catch (_) {
            throw new Error('Server error. Please try again later.');
        }

        if (!res.ok) throw new Error(data.detail || 'Failed to fetch video');

        // Update UI
        document.getElementById('thumb').src = data.thumbnail;
        document.getElementById('videoTitle').innerText = data.title;
        document.getElementById('uploader').innerText = data.uploader || 'Unknown';
        document.getElementById('views').innerText = data.view_count || 'N/A';
        document.getElementById('duration').innerText = data.duration || 'N/A';

        result.style.display = 'block';
    } catch (err) {
        error.innerText = err.message;
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

async function triggerDownload(format) {
    let status = document.getElementById('status-msg');
    if (!status) {
        status = document.createElement('div');
        status.id = 'status-msg';
        status.style.cssText = "text-align:center; padding: 15px; margin-bottom: 20px; border-radius: 12px; font-weight: 600; color: #047857; background: #d1fae5; border: 1px solid #6ee7b7;";
        document.getElementById('result').insertBefore(status, document.getElementById('result').firstChild);
    }
    status.innerText = "Starting download... please wait.";
    status.style.display = 'block';

    const url = document.getElementById('urlInput').value;
    if (!url) {
        status.style.display = 'none';
        return;
    }

    try {
        if (typeof window.gtag === 'function') {
            window.gtag('event', 'video_download', {
                'event_category': 'Engagement',
                'event_label': format,
                'url_downloaded': url
            });
        }

        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/download';
        
        const inputUrl = document.createElement('input');
        inputUrl.type = 'hidden';
        inputUrl.name = 'url';
        inputUrl.value = url;
        form.appendChild(inputUrl);

        const inputFormat = document.createElement('input');
        inputFormat.type = 'hidden';
        inputFormat.name = 'format';
        inputFormat.value = format;
        form.appendChild(inputFormat);

        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
        
        setTimeout(() => { 
            status.style.display = 'none'; 
        }, 4000);
    } catch (err) {
        alert("Error: " + err.message);
        status.style.display = 'none';
    }
}
