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
// Download/Preview Logic
async function handleDownload(e) {
    e.preventDefault();
    const url = document.getElementById('urlInput').value;
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const error = document.getElementById('error');
    const submitBtn = document.querySelector('.download-btn');

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
    loading.scrollIntoView({ behavior: 'smooth', block: 'center' });
    result.style.display = 'none';
    error.style.display = 'none';
    if(document.getElementById('status-msg')) document.getElementById('status-msg').style.display = 'none';

    if (submitBtn) {
        submitBtn.classList.add('btn-loading');
    }

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
        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (err) {
        error.innerText = err.message;
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
        if (submitBtn) submitBtn.classList.remove('btn-loading');
    }
}

async function triggerDownload(format) {
    let targetBtn;
    let originalText;
    if (format === 'audio') {
        targetBtn = document.querySelector('.dl-audio');
    } else if (format === 'high_quality') {
        targetBtn = document.querySelector('.dl-hq');
    } else {
        targetBtn = document.querySelector('.dl-video');
    }

    if (targetBtn) {
        originalText = targetBtn.innerText;
        targetBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin-icon" style="animation: spin 1s infinite linear;">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.3"></circle>
                <path d="M12 2a10 10 0 0 1 10 10"></path>
            </svg> Starting...
        `;
        targetBtn.classList.add('btn-processing');
    } else {
        let status = document.getElementById('status-msg');
        if (!status) {
            status = document.createElement('div');
            status.id = 'status-msg';
            status.style.cssText = "text-align:center; padding: 15px; margin-bottom: 20px; border-radius: 12px; font-weight: 600; color: #047857; background: #d1fae5; border: 1px solid #6ee7b7;";
            document.getElementById('result').insertBefore(status, document.getElementById('result').firstChild);
        }
        status.innerText = "Starting download... please wait.";
        status.style.display = 'block';
    }

    const url = document.getElementById('urlInput').value;
    if (!url) {
        if (targetBtn) {
            targetBtn.classList.remove('btn-processing');
            targetBtn.innerText = originalText;
        }
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

        let iframe = document.getElementById('download_iframe');
        if (!iframe) {
            iframe = document.createElement('iframe');
            iframe.id = 'download_iframe';
            iframe.name = 'download_iframe';
            iframe.style.display = 'none';
            document.body.appendChild(iframe);
        }

        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/download';
        form.target = 'download_iframe';
        
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

        // Clear old cookies
        document.cookie = "download_ready=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "download_error=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

        document.body.appendChild(form);
        form.submit();
        setTimeout(() => document.body.removeChild(form), 100);
        
        if (targetBtn) {
            let msg = format === 'high_quality' ? 'Processing (up to 5 min)...' : 'Starting...';
            targetBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin-icon" style="animation: spin 1s infinite linear;">
                    <circle cx="12" cy="12" r="10" stroke-opacity="0.3"></circle>
                    <path d="M12 2a10 10 0 0 1 10 10"></path>
                </svg> ${msg}
            `;
        }
        
        let checkCookie = setInterval(() => {
            if (document.cookie.indexOf("download_ready=1") !== -1) {
                clearInterval(checkCookie);
                let status = document.getElementById('status-msg');
                if (status) status.style.display = 'none'; 
                if (targetBtn) {
                    targetBtn.classList.remove('btn-processing');
                    targetBtn.classList.add('btn-success');
                    targetBtn.innerHTML = `
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg> Download Started!
                    `;
                    setTimeout(() => {
                        targetBtn.classList.remove('btn-success');
                        targetBtn.innerText = originalText;
                    }, 4000);
                }
            } else if (document.cookie.indexOf("download_error=1") !== -1) {
                clearInterval(checkCookie);
                document.cookie = "download_error=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                if (targetBtn) {
                    targetBtn.classList.remove('btn-processing');
                    targetBtn.innerText = originalText;
                }
                let status = document.getElementById('status-msg');
                if (status) status.style.display = 'none';
                
                alert("Fast download is not available for this premium/music video because YouTube split the streams. Please use the 'Download 4K (Best Quality)' button instead, which will process and merge it for you.");
            }
        }, 1000);
    } catch (err) {
        alert("Error: " + err.message);
        if (targetBtn) {
            targetBtn.classList.remove('btn-processing');
            targetBtn.innerText = originalText;
        }
        let status = document.getElementById('status-msg');
        if (status) status.style.display = 'none';
    }
}
