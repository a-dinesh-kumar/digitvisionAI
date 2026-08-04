/**
 * DigitVision AI - Master Client Application Script
 * Full Stack Interactive Canvas, File Upload, Inference API & LocalStorage History
 */

document.addEventListener('DOMContentLoaded', () => {

    // Initialize AOS Animations
    if (typeof AOS !== 'undefined') {
        AOS.init({ duration: 800, once: true });
    }

    // =========================================================================
    // 1. THEME MANAGER (Dark / Light Mode)
    // =========================================================================
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlElem = document.documentElement;

    const savedTheme = localStorage.getItem('digitvision_theme') || localStorage.getItem('mnist_theme') || 'light';
    setTheme(savedTheme);

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = htmlElem.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    function setTheme(theme) {
        htmlElem.setAttribute('data-bs-theme', theme);
        localStorage.setItem('digitvision_theme', theme);
        if (theme === 'dark') {
            themeIcon.className = 'bi bi-sun-fill text-warning';
        } else {
            themeIcon.className = 'bi bi-moon-stars-fill text-dark';
        }
    }

    // =========================================================================
    // 2. CANVAS MANAGER (320x320 Drawing Studio)
    // =========================================================================
    const canvas = document.getElementById('digitCanvas');
    const ctx = canvas.getContext('2d');
    const brushSizeInput = document.getElementById('brushSize');
    const brushSizeVal = document.getElementById('brushSizeVal');
    const clearCanvasBtn = document.getElementById('clearCanvasBtn');
    const undoBtn = document.getElementById('undoBtn');
    const downloadCanvasBtn = document.getElementById('downloadCanvasBtn');
    const predictCanvasBtn = document.getElementById('predictCanvasBtn');

    let isDrawing = false;
    let canvasHistory = [];
    const maxHistory = 20;

    // Initialize Canvas Background (Solid Black)
    function initCanvas() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        saveCanvasState();
    }
    initCanvas();

    function saveCanvasState() {
        if (canvasHistory.length >= maxHistory) {
            canvasHistory.shift();
        }
        canvasHistory.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    }

    function undoStroke() {
        if (canvasHistory.length > 1) {
            canvasHistory.pop(); // Remove current state
            const previousState = canvasHistory[canvasHistory.length - 1];
            ctx.putImageData(previousState, 0, 0);
        } else if (canvasHistory.length === 1) {
            initCanvas();
        }
    }

    // Brush Size Event
    brushSizeInput.addEventListener('input', (e) => {
        brushSizeVal.textContent = `${e.target.value}px`;
    });

    // Get Mouse or Touch Position relative to Canvas
    function getCanvasCoordinates(e) {
        const rect = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return {
            x: (clientX - rect.left) * (canvas.width / rect.width),
            y: (clientY - rect.top) * (canvas.height / rect.height)
        };
    }

    function startDrawing(e) {
        e.preventDefault();
        isDrawing = true;
        const pos = getCanvasCoordinates(e);
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
    }

    function draw(e) {
        if (!isDrawing) return;
        e.preventDefault();
        const pos = getCanvasCoordinates(e);

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = brushSizeInput.value;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
    }

    function stopDrawing(e) {
        if (isDrawing) {
            isDrawing = false;
            ctx.closePath();
            saveCanvasState();
        }
    }

    // Mouse Listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);

    // Touch Listeners
    canvas.addEventListener('touchstart', startDrawing);
    canvas.addEventListener('touchmove', draw);
    canvas.addEventListener('touchend', stopDrawing);

    // Toolbar Buttons
    clearCanvasBtn.addEventListener('click', initCanvas);
    undoBtn.addEventListener('click', undoStroke);
    downloadCanvasBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = `digitvision_drawing_${Date.now()}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    });

    // =========================================================================
    // 3. FILE UPLOAD MANAGER
    // =========================================================================
    const canvasTabBtn = document.getElementById('canvas-tab');
    const uploadTabBtn = document.getElementById('upload-tab');
    const canvasPane = document.getElementById('canvas-pane');
    const uploadPane = document.getElementById('upload-pane');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const dropZonePrompt = document.getElementById('dropZonePrompt');
    const browseFileBtn = document.getElementById('browseFileBtn');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const previewImg = document.getElementById('previewImg');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const replaceFileBtn = document.getElementById('replaceFileBtn');
    const removeFileBtn = document.getElementById('removeFileBtn');
    const predictUploadBtn = document.getElementById('predictUploadBtn');

    let selectedFile = null;

    function activateInputTab(tabName) {
        if (tabName === 'upload') {
            canvasTabBtn?.classList.remove('active');
            uploadTabBtn?.classList.add('active');
            canvasPane?.classList.remove('show', 'active');
            uploadPane?.classList.add('show', 'active');
        } else {
            uploadTabBtn?.classList.remove('active');
            canvasTabBtn?.classList.add('active');
            uploadPane?.classList.remove('show', 'active');
            canvasPane?.classList.add('show', 'active');
        }
    }

    // Trigger File Input Browser Dialog when clicking dropZone prompt or browse button
    dropZone.addEventListener('click', (e) => {
        // If clicking on replace button or remove button, do not trigger dropzone click
        if (e.target.closest('#replaceFileBtn') || e.target.closest('#removeFileBtn')) {
            return;
        }
        fileInput.click();
    });

    if (browseFileBtn) {
        browseFileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            activateInputTab('upload');
            fileInput.click();
        });
    }

    if (uploadTabBtn) {
        uploadTabBtn.addEventListener('click', (e) => {
            activateInputTab('upload');
        });
    }

    if (canvasTabBtn) {
        canvasTabBtn.addEventListener('click', (e) => {
            activateInputTab('canvas');
        });
    }

    // Drag & Drop events
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-over');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleSelectedFile(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    function handleSelectedFile(file) {
        const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            alert('Invalid file type! Please upload a PNG, JPG, or JPEG image.');
            return;
        }

        if (file.size > 5 * 1024 * 1024) { // 5MB
            alert('File size exceeds maximum limit of 5MB.');
            return;
        }

        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = `${(file.size / 1024).toFixed(1)} KB`;

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            dropZonePrompt.classList.add('d-none');
            imagePreviewContainer.classList.remove('d-none');
            predictUploadBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    replaceFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUploadZone();
    });

    function resetUploadZone() {
        selectedFile = null;
        fileInput.value = '';
        previewImg.src = '';
        dropZonePrompt.classList.remove('d-none');
        imagePreviewContainer.classList.add('d-none');
        predictUploadBtn.disabled = true;
    }

    // =========================================================================
    // 4. API PREDICTION INTEGRATION
    // =========================================================================
    const resultEmptyState = document.getElementById('resultEmptyState');
    const resultSpinnerState = document.getElementById('resultSpinnerState');
    const resultActiveState = document.getElementById('resultActiveState');
    const predictedDigitDisplay = document.getElementById('predictedDigitDisplay');
    const predictedConfidenceVal = document.getElementById('predictedConfidenceVal');
    const confidenceProgressBar = document.getElementById('confidenceProgressBar');
    const confidenceBarText = document.getElementById('confidenceBarText');
    const lowConfidenceAlert = document.getElementById('lowConfidenceAlert');
    const probabilityDistribution = document.getElementById('probabilityDistribution');
    const latencyBadge = document.getElementById('latencyBadge');
    const latencyVal = document.getElementById('latencyVal');

    // Predict Canvas Action
    predictCanvasBtn.addEventListener('click', async () => {
        const base64Data = canvas.toDataURL('image/png');
        showLoadingState();

        try {
            const response = await fetch('/predict-canvas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: base64Data })
            });

            const data = await response.json();
            if (response.ok) {
                renderPredictionResult(data, 'Canvas', base64Data);
            } else {
                alert(`Error: ${data.error || 'Failed to predict canvas digit.'}`);
                showEmptyState();
            }
        } catch (err) {
            console.error(err);
            alert('Server error occurred during prediction request.');
            showEmptyState();
        }
    });

    // Predict Upload Action
    predictUploadBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);
        showLoadingState();

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                renderPredictionResult(data, 'Upload', previewImg.src);
            } else {
                alert(`Error: ${data.error || 'Failed to predict uploaded image.'}`);
                showEmptyState();
            }
        } catch (err) {
            console.error(err);
            alert('Server error occurred during prediction request.');
            showEmptyState();
        }
    });

    function showLoadingState() {
        resultEmptyState.classList.add('d-none');
        resultActiveState.classList.add('d-none');
        resultSpinnerState.classList.remove('d-none');
        latencyBadge.classList.add('d-none');
    }

    function showEmptyState() {
        resultSpinnerState.classList.add('d-none');
        resultActiveState.classList.add('d-none');
        resultEmptyState.classList.remove('d-none');
    }

    function renderPredictionResult(data, sourceTag, thumbnailData) {
        resultSpinnerState.classList.add('d-none');
        resultEmptyState.classList.add('d-none');
        resultActiveState.classList.remove('d-none');

        const digit = data.prediction;
        const confidence = data.confidence;
        const probs = data.probabilities || {};

        // Display main prediction metrics
        predictedDigitDisplay.textContent = digit;
        predictedConfidenceVal.textContent = `${confidence.toFixed(2)}%`;
        confidenceBarText.textContent = `${confidence.toFixed(2)}%`;
        confidenceProgressBar.style.width = `${confidence}%`;

        // Check Low Confidence Threshold (< 70%)
        if (confidence < 70.0) {
            lowConfidenceAlert.classList.remove('d-none');
        } else {
            lowConfidenceAlert.classList.add('d-none');
        }

        // Show Latency Badge
        if (data.execution_time_ms) {
            latencyVal.textContent = data.execution_time_ms;
            latencyBadge.classList.remove('d-none');
        }

        // Render Probability Breakdown
        probabilityDistribution.innerHTML = '';
        for (let i = 0; i <= 9; i++) {
            const probVal = probs[i] !== undefined ? probs[i] : 0.0;
            const isTopClass = (i === digit);

            const row = document.createElement('div');
            row.className = `prob-row d-flex align-items-center gap-2 mb-2 ${isTopClass ? 'fw-bold text-primary' : 'text-secondary'}`;
            row.innerHTML = `
                <span class="font-monospace text-center" style="width: 20px;">${i}</span>
                <div class="prob-bar-bg flex-grow-1">
                    <div class="prob-bar-fill ${isTopClass ? 'active-top' : ''}" style="width: ${probVal}%;"></div>
                </div>
                <span class="font-monospace text-end" style="width: 55px;">${probVal.toFixed(1)}%</span>
            `;
            probabilityDistribution.appendChild(row);
        }

        // Save Record to LocalStorage History
        saveHistoryItem({
            id: Date.now(),
            thumbnail: thumbnailData,
            prediction: digit,
            confidence: confidence,
            source: sourceTag,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
        });
    }

    // =========================================================================
    // 5. LOCALSTORAGE PREDICTION HISTORY MANAGER
    // =========================================================================
    const historyTableBody = document.getElementById('historyTableBody');
    const historyEmptyMsg = document.getElementById('historyEmptyMsg');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');

    loadHistory();

    function getHistory() {
        return JSON.parse(localStorage.getItem('digitvision_history') || localStorage.getItem('mnist_history') || '[]');
    }

    function saveHistoryItem(item) {
        let history = getHistory();
        history.unshift(item); // Insert at beginning
        if (history.length > 10) {
            history = history.slice(0, 10); // Keep max 10
        }
        localStorage.setItem('digitvision_history', JSON.stringify(history));
        loadHistory();
    }

    function deleteHistoryItem(id) {
        let history = getHistory().filter(item => item.id !== id);
        localStorage.setItem('digitvision_history', JSON.stringify(history));
        loadHistory();
    }

    clearHistoryBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all prediction history?')) {
            localStorage.removeItem('digitvision_history');
            localStorage.removeItem('mnist_history');
            loadHistory();
        }
    });

    function loadHistory() {
        const history = getHistory();
        historyTableBody.innerHTML = '';

        if (history.length === 0) {
            historyEmptyMsg.classList.remove('d-none');
            return;
        }

        historyEmptyMsg.classList.add('d-none');

        history.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4">
                    <img src="${item.thumbnail}" alt="Thumb" class="rounded border shadow-sm" style="width: 36px; height: 36px; object-fit: cover;">
                </td>
                <td class="fw-bold fs-5 text-gradient">${item.prediction}</td>
                <td>
                    <span class="badge ${item.confidence >= 70 ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'} font-monospace">
                        ${item.confidence.toFixed(1)}%
                    </span>
                </td>
                <td>
                    <span class="badge ${item.source === 'Canvas' ? 'bg-primary-subtle text-primary' : 'bg-info-subtle text-info'} rounded-pill">
                        ${item.source}
                    </span>
                </td>
                <td class="text-secondary small font-monospace">${item.timestamp}</td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-danger border-0 rounded-circle delete-hist-btn" data-id="${item.id}" title="Delete Record">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            historyTableBody.appendChild(tr);
        });

        // Attach Delete Click Listeners
        document.querySelectorAll('.delete-hist-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.currentTarget.getAttribute('data-id'));
                deleteHistoryItem(id);
            });
        });
    }

});
