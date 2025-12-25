// API Configuration
const API_BASE_URL = 'http://localhost:8000';
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const selectedFile = document.getElementById('selectedFile');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeBtn = document.getElementById('removeBtn');
const submitBtn = document.getElementById('submitBtn');

const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const summarySection = document.getElementById('summarySection');
const errorSection = document.getElementById('errorSection');

const summaryContent = document.getElementById('summaryContent');
const pageCount = document.getElementById('pageCount');
const summaryFileName = document.getElementById('summaryFileName');
const copyBtn = document.getElementById('copyBtn');
const newSummaryBtn = document.getElementById('newSummaryBtn');
const retryBtn = document.getElementById('retryBtn');
const errorMessage = document.getElementById('errorMessage');

// State
let currentFile = null;

// Event Listeners
browseBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
removeBtn.addEventListener('click', clearFile);
submitBtn.addEventListener('click', handleSubmit);
copyBtn.addEventListener('click', handleCopy);
newSummaryBtn.addEventListener('click', resetToUpload);
retryBtn.addEventListener('click', resetToUpload);

// Drag and Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// File Handling
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showError('Please select a PDF file');
        return;
    }
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
        showError(`File size exceeds maximum allowed size of ${MAX_FILE_SIZE / (1024 * 1024)}MB`);
        return;
    }
    
    if (file.size === 0) {
        showError('The selected file is empty');
        return;
    }
    
    // Store file and update UI
    currentFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    selectedFile.style.display = 'flex';
    submitBtn.style.display = 'flex';
    dropZone.style.display = 'none';
}

function clearFile() {
    currentFile = null;
    fileInput.value = '';
    selectedFile.style.display = 'none';
    submitBtn.style.display = 'none';
    dropZone.style.display = 'block';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Submit Handler
async function handleSubmit() {
    if (!currentFile) return;
    
    // Show loading state
    showSection(loadingSection);
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', currentFile);
    
    try {
        // Upload and process PDF
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to process PDF');
        }
        
        const data = await response.json();
        
        // Display summary
        displaySummary(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An unexpected error occurred. Please try again.');
    }
}

// Display Summary
function displaySummary(data) {
    summaryContent.textContent = data.summary;
    pageCount.textContent = `📄 ${data.page_count} page${data.page_count !== 1 ? 's' : ''}`;
    summaryFileName.textContent = `📎 ${data.file_name}`;
    
    showSection(summarySection);
}

// Copy to Clipboard
async function handleCopy() {
    try {
        await navigator.clipboard.writeText(summaryContent.textContent);
        
        // Visual feedback
        const originalText = copyBtn.querySelector('span').textContent;
        copyBtn.querySelector('span').textContent = 'Copied!';
        
        setTimeout(() => {
            copyBtn.querySelector('span').textContent = originalText;
        }, 2000);
        
    } catch (error) {
        console.error('Failed to copy:', error);
        alert('Failed to copy to clipboard');
    }
}

// Error Handling
function showError(message) {
    errorMessage.textContent = message;
    showSection(errorSection);
}

// Section Management
function showSection(section) {
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'none';
    summarySection.style.display = 'none';
    errorSection.style.display = 'none';
    
    section.style.display = 'block';
}

function resetToUpload() {
    clearFile();
    showSection(uploadSection);
}

// Initialize
showSection(uploadSection);
