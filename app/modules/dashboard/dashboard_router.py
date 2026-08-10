from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Document Intelligence Agent - Dashboard</title>
    <!-- Google Fonts Outfit & Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-primary: #0a0b10;
            --bg-secondary: #12131a;
            --bg-card: rgba(22, 24, 35, 0.7);
            --accent-primary: #6366f1;
            --accent-secondary: #06b6d4;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-glow: rgba(99, 102, 241, 0.15);
            --success: #10b981;
            --warning: #f59e0b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            overflow-x: hidden;
            min-height: 100vh;
        }

        h1, h2, h3, .brand {
            font-family: 'Outfit', sans-serif;
        }

        /* Layout Grid */
        .app-container {
            display: grid;
            grid-template-columns: 280px 1fr;
            min-height: 100vh;
        }

        /* Sidebar Styling */
        sidebar {
            background-color: var(--bg-secondary);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            padding: 2rem 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 3rem;
        }

        .logo-icon {
            font-size: 1.8rem;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 2px 8px rgba(99, 102, 241, 0.4));
        }

        .brand-name {
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #ffffff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .settings-section {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            flex-grow: 1;
        }

        .settings-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .input-group label {
            font-size: 0.85rem;
            font-weight: 500;
            color: #d1d5db;
        }

        select, input[type="text"] {
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            padding: 0.75rem;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.9rem;
            transition: all 0.2s ease;
            outline: none;
        }

        select:focus, input[type="text"]:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
            background-color: rgba(255, 255, 255, 0.05);
        }

        /* Main Content View */
        main {
            padding: 2.5rem;
            overflow-y: auto;
            max-height: 100vh;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
        }

        .header-title h2 {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .header-title p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        .api-badge {
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--success);
            padding: 0.5rem 1rem;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Dashboard Grid */
        .workspace {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            align-items: start;
        }

        .glass-card {
            background-color: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 1.75rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            transition: border 0.3s ease;
        }

        .glass-card:hover {
            border-color: rgba(99, 102, 241, 0.25);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Upload Area */
        .upload-zone {
            border: 2px dashed rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 3rem 1.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            background-color: rgba(255, 255, 255, 0.01);
        }

        .upload-zone:hover, .upload-zone.dragover {
            border-color: var(--accent-secondary);
            background-color: rgba(6, 182, 212, 0.03);
            box-shadow: inset 0 0 20px rgba(6, 182, 212, 0.05);
        }

        .upload-icon {
            font-size: 3rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }

        .upload-zone:hover .upload-icon {
            transform: translateY(-5px);
            color: var(--accent-secondary);
        }

        .upload-text {
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        .upload-subtext {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        #file-input {
            display: none;
        }

        /* Results / Output styling */
        .output-container {
            position: relative;
        }

        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 5rem 2rem;
            color: var(--text-muted);
            text-align: center;
        }

        .empty-state i {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            opacity: 0.3;
        }

        pre {
            background-color: #050508;
            padding: 1.25rem;
            border-radius: 10px;
            overflow-x: auto;
            max-height: 480px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.85rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: #10b981;
        }

        /* Progress Steps */
        .progress-steps {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            margin-top: 1.5rem;
        }

        .step-item {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            opacity: 0.4;
            transition: opacity 0.3s ease;
        }

        .step-item.active {
            opacity: 1;
        }

        .step-badge {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, 0.05);
            border: 1.5px solid var(--text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 700;
            flex-shrink: 0;
        }

        .step-item.completed .step-badge {
            background-color: var(--success);
            border-color: var(--success);
            color: white;
        }

        .step-item.active .step-badge {
            background-color: var(--accent-primary);
            border-color: var(--accent-primary);
            color: white;
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
        }

        .step-content h4 {
            font-size: 0.95rem;
            margin-bottom: 0.15rem;
        }

        .step-content p {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        /* Meta metrics grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 1rem;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 0.75rem 1rem;
            border-radius: 8px;
        }

        .metric-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }

        .metric-value {
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 0.15rem;
            color: #ffffff;
        }

        /* Tabs */
        .tabs-header {
            display: flex;
            gap: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 1rem;
        }

        .tab-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            padding: 0.75rem 1rem;
            font-family: inherit;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            position: relative;
            outline: none;
        }

        .tab-btn.active {
            color: #ffffff;
        }

        .tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--accent-primary);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Flowchart styling */
        .flowchart-svg {
            width: 100%;
            height: auto;
            max-height: 380px;
            margin-top: 1rem;
        }

        /* Quick Info Matrix */
        table.matrix {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
            margin-top: 1rem;
        }

        table.matrix th, table.matrix td {
            padding: 0.6rem;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        table.matrix th {
            color: var(--text-muted);
            font-weight: 600;
            background: rgba(255, 255, 255, 0.02);
        }

        /* Loader Animation */
        .loader {
            display: none;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(10, 11, 16, 0.85);
            z-index: 10;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(99, 102, 241, 0.1);
            border-top: 3px solid var(--accent-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

<div class="app-container">
    <!-- Sidebar -->
    <sidebar>
        <div>
            <div class="brand-logo">
                <i class="fa-solid fa-brain logo-icon"></i>
                <div class="brand-name">DocIntel Agent</div>
            </div>
            
            <div class="settings-section">
                <div class="input-group">
                    <div class="settings-title">Configuration</div>
                    <label for="schema-select">Target Schema</label>
                    <select id="schema-select">
                        <option value="invoice">Invoice</option>
                        <option value="receipt">Receipt</option>
                        <option value="bank_statement">Bank Statement</option>
                        <option value="purchase_order">Purchase Order</option>
                        <option value="form">Generic Form / Checkbox</option>
                    </select>
                </div>

                <div class="input-group">
                    <label for="engine-select">OCR Selection Model</label>
                    <select id="engine-select">
                        <option value="auto">Agent Decides (Auto)</option>
                        <option value="doctr">Force Mindee docTR</option>
                        <option value="rapidocr">Force RapidOCR ONNX</option>
                        <option value="easyocr">Force EasyOCR Fallback</option>
                    </select>
                </div>
            </div>
        </div>

        <div style="font-size: 0.75rem; color: var(--text-muted); text-align: center;">
            Document Intelligence Agent v1.0.0
        </div>
    </sidebar>

    <!-- Main Content -->
    <main>
        <header>
            <div class="header-title">
                <h2>AI Document Intelligence Processing</h2>
                <p>Upload document images or PDFs. The Agent analyzes layout, pre-processes skew, routes to optimal OCR, and structures validated JSON via Gemini.</p>
            </div>
            <div class="api-badge">
                <i class="fa-solid fa-circle-check"></i> Connected
            </div>
        </header>

        <div class="workspace">
            <!-- Left Panel (Control / Upload) -->
            <div class="glass-card" style="position: relative;">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fa-solid fa-file-arrow-up" style="color: var(--accent-secondary);"></i>
                        Upload Document
                    </div>
                </div>

                <div class="upload-zone" id="drop-zone">
                    <i class="fa-solid fa-cloud-arrow-up upload-icon"></i>
                    <div class="upload-text">Drag and drop file here</div>
                    <div class="upload-subtext">Supports PDF, PNG, JPG, JPEG (Max 15MB)</div>
                    <input type="file" id="file-input" accept=".pdf,.png,.jpg,.jpeg">
                </div>

                <!-- Custom visual flowchart built with styling -->
                <div class="tabs-header" style="margin-top: 1.5rem;">
                    <button class="tab-btn active" onclick="switchTab(event, 'agent-flow-tab')">Agent Workflow</button>
                    <button class="tab-btn" onclick="switchTab(event, 'matrix-tab')">Technology Matrix</button>
                </div>

                <div id="agent-flow-tab" class="tab-content active">
                    <div class="progress-steps" id="agent-steps">
                        <div class="step-item" id="step-classify">
                            <div class="step-badge">1</div>
                            <div class="step-content">
                                <h4>Classification & Preprocessing</h4>
                                <p id="desc-classify">Inspect layout structure, orientation, and deskew angle.</p>
                            </div>
                        </div>
                        <div class="step-item" id="step-ocr">
                            <div class="step-badge">2</div>
                            <div class="step-content">
                                <h4>Agent Routing Decision</h4>
                                <p id="desc-ocr">Extract text with PyMuPDF (digital bypass), docTR (lightweight), or EasyOCR/RapidOCR.</p>
                            </div>
                        </div>
                        <div class="step-item" id="step-struct">
                            <div class="step-badge">3</div>
                            <div class="step-content">
                                <h4>VLM/LLM Gemini Schema Mapping</h4>
                                <p id="desc-struct">Apply system prompt, map coordinates, and validate output JSON schema.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="matrix-tab" class="tab-content">
                    <table class="matrix">
                        <thead>
                            <tr>
                                <th>Engine</th>
                                <th>Tech Base</th>
                                <th>Primary Strength</th>
                                <th>Agent Routing Trigger</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>PyMuPDF</strong></td>
                                <td>C++ MuPDF Parser</td>
                                <td>100% Accuracy, Sub-ms speed</td>
                                <td>Searchable vector-text PDFs</td>
                            </tr>
                            <tr>
                                <td><strong>Mindee docTR</strong></td>
                                <td>MobileNetV3 (DBNet/CRNN)</td>
                                <td>Deep doc hierarchy, light RAM</td>
                                <td>Clean business forms & scanned docs</td>
                            </tr>
                            <tr>
                                <td><strong>RapidOCR</strong></td>
                                <td>ONNX Runtime</td>
                                <td>Sub-second CPU inference</td>
                                <td>Alternative fast fallback</td>
                            </tr>
                            <tr>
                                <td><strong>EasyOCR</strong></td>
                                <td>ResNet (PyTorch)</td>
                                <td>Handwriting, Scene text</td>
                                <td>Failed docTR/low confidence threshold</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Inner Loader overlay -->
                <div class="loader" id="process-loader" style="display: none;">
                    <div class="spinner"></div>
                    <div style="font-weight: 500;">Agent Executing Decision Nodes...</div>
                </div>
            </div>

            <!-- Right Panel (Output Display) -->
            <div class="glass-card output-container">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fa-solid fa-code" style="color: var(--accent-primary);"></i>
                        Structured Output JSON
                    </div>
                    <button class="tab-btn" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;" onclick="copyJSON()">
                        <i class="fa-solid fa-copy"></i> Copy
                    </button>
                </div>

                <div id="empty-output" class="empty-state">
                    <i class="fa-solid fa-laptop-code"></i>
                    <h3>Ready for Extraction</h3>
                    <p style="margin-top: 0.5rem; max-width: 280px; font-size: 0.85rem;">Upload a document and select schema rules from the sidebar to inspect routing metrics.</p>
                </div>

                <div id="output-block" style="display: none;">
                    <pre><code id="json-renderer"></code></pre>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">Agent Router Action</div>
                            <div class="metric-value" id="val-routing" style="color: var(--accent-secondary); font-size: 0.95rem;">-</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Total Pipeline Latency</div>
                            <div class="metric-value" id="val-latency">-</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Document Form Factor</div>
                            <div class="metric-value" id="val-doc-type">-</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Detected Skew Angles</div>
                            <div class="metric-value" id="val-skew">-</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</div>

<script>
    // Tab switching logic
    function switchTab(evt, tabId) {
        const contents = document.getElementsByClassName('tab-content');
        for (let i = 0; i < contents.length; i++) {
            contents[i].classList.remove('active');
        }
        
        const btns = evt.currentTarget.parentNode.getElementsByClassName('tab-btn');
        for (let i = 0; i < btns.length; i++) {
            btns[i].classList.remove('active');
        }
        
        document.getElementById(tabId).classList.add('active');
        evt.currentTarget.classList.add('active');
    }

    // Copy to clipboard
    function copyJSON() {
        const text = document.getElementById('json-renderer').innerText;
        if (text) {
            navigator.clipboard.writeText(text);
            alert('JSON copied to clipboard!');
        }
    }

    // Upload & Drag/drop handlers
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const emptyOutput = document.getElementById('empty-output');
    const outputBlock = document.getElementById('output-block');
    const loader = document.getElementById('process-loader');
    
    // Steps elements
    const stepClassify = document.getElementById('step-classify');
    const stepOcr = document.getElementById('step-ocr');
    const stepStruct = document.getElementById('step-struct');
    
    const descClassify = document.getElementById('desc-classify');
    const descOcr = document.getElementById('desc-ocr');
    const descStruct = document.getElementById('desc-struct');

    dropZone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) uploadFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if (fileInput.files.length) uploadFile(fileInput.files[0]);
    });

    function resetSteps() {
        [stepClassify, stepOcr, stepStruct].forEach(s => {
            s.classList.remove('active', 'completed');
        });
        descClassify.innerText = "Inspect layout structure, orientation, and deskew angle.";
        descOcr.innerText = "Extract text with PyMuPDF (digital bypass), docTR (lightweight), or EasyOCR/RapidOCR.";
        descStruct.innerText = "Apply system prompt, map coordinates, and validate output JSON schema.";
    }

    async function uploadFile(file) {
        resetSteps();
        
        // Show loader
        loader.style.display = 'flex';
        emptyOutput.style.display = 'flex';
        outputBlock.style.display = 'none';

        // Prepare request
        const schema = document.getElementById('schema-select').value;
        const engine = document.getElementById('engine-select').value;
        
        const formData = new FormData();
        formData.append('file', file);

        // Step 1: Preprocessing Active
        stepClassify.classList.add('active');
        descClassify.innerText = "Analyzing file geometry & selectable vectors...";

        try {
            const response = await fetch(`/api/v1/process?schema_type=${schema}&ocr_engine=${engine}`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP Error ${response.status}`);
            }

            const data = await response.json();
            
            // UI updates for successful processing
            stepClassify.classList.remove('active');
            stepClassify.classList.add('completed');
            descClassify.innerText = `File Classified: ${data.document_type}. Skew: ${data.preprocessing_details.skew_angles.map(a => a.toFixed(1) + '°').join(', ') || '0°'}`;

            // Step 2: OCR Active
            stepOcr.classList.add('active');
            descOcr.innerText = `OCR Routing completed. Selected: ${data.routing_decision}`;
            
            // Wait slightly for visual timing effect
            await new Promise(r => setTimeout(r, 600));
            stepOcr.classList.remove('active');
            stepOcr.classList.add('completed');

            // Step 3: Structuring Active
            stepStruct.classList.add('active');
            descStruct.innerText = "Gemini schema validation & matching complete.";
            stepStruct.classList.remove('active');
            stepStruct.classList.add('completed');

            // Display outputs
            emptyOutput.style.display = 'none';
            outputBlock.style.display = 'block';
            
            document.getElementById('json-renderer').innerText = JSON.stringify(data.structured_data, null, 2);
            document.getElementById('val-routing').innerText = data.routing_decision;
            document.getElementById('val-latency').innerText = `${data.latency_metrics.total_seconds}s`;
            document.getElementById('val-doc-type').innerText = data.document_type;
            
            const sks = data.preprocessing_details.skew_angles;
            document.getElementById('val-skew').innerText = sks.length ? sks.map(a => a.toFixed(1) + '°').join(', ') : '0°';

        } catch (error) {
            console.error(error);
            alert(`Process failed: ${error.message}`);
            stepClassify.classList.add('active');
            descClassify.innerText = "Extraction failed. Check network console.";
        } finally {
            loader.style.display = 'none';
        }
    }
</script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse, summary="Load Dashboard Web Interface")
async def read_dashboard():
    """
    Serves the stunning document processing agentic routing dashboard.
    """
    return DASHBOARD_HTML
