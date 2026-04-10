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
    loading.style.display = 'block';
    result.style.display = 'none';
    error.style.display = 'none';

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
    const status = document.getElementById('loading'); // Reuse loading div
    status.innerText = "Downloading...";
    status.style.display = 'block';

    try {
        const formData = new FormData();
        formData.append('url', document.getElementById('urlInput').value);
        formData.append('format', format); // Pass format

        const res = await fetch('/download', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            const rawText = await res.text();
            let errDetail = "Download failed. Please try again.";
            try {
                const errJson = JSON.parse(rawText);
                errDetail = errJson.detail || errDetail;
            } catch (_) {
                // Server ne JSON nahi diya (e.g. 500 Internal Server Error plain text)
                if (rawText && rawText.length < 200) errDetail = rawText;
            }
            throw new Error(errDetail);
        }

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        // Try to get filename from header or fallback
        const disposition = res.headers.get('Content-Disposition');
        let filename = 'video.mp4';
        if (disposition && disposition.indexOf('attachment') !== -1) {
            const utf8Regex = /filename\*=UTF-8''([^;\n]*)/i;
            const utf8Matches = utf8Regex.exec(disposition);
            if (utf8Matches && utf8Matches[1]) {
                filename = decodeURIComponent(utf8Matches[1].replace(/['"]/g, ''));
            } else {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '');
                }
            }
        }
        if (format === 'audio' && !filename.endsWith('.m4a') && !filename.endsWith('.mp3')) {
            filename = filename.replace(/\.[^/.]+$/, ".m4a");
        }

        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        
        // Track the download event in Google Analytics
        if (typeof window.gtag === 'function') {
            window.gtag('event', 'video_download', {
                'event_category': 'Engagement',
                'event_label': format,
                'file_name': filename,
                'url_downloaded': document.getElementById('urlInput') ? document.getElementById('urlInput').value : 'unknown'
            });
        }
        
        status.innerText = "Download Complete!";
        setTimeout(() => { status.style.display = 'none'; status.innerText = "Processing..."; }, 3000);
    } catch (err) {
        alert("Error: " + err.message);
        status.style.display = 'none';
    }
}
