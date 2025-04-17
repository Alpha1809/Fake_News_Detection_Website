/**
 * Main JavaScript file for the Fake News Detector application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Switch between text and URL input tabs
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs and content
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const target = this.getAttribute('data-target');
            document.getElementById(target).classList.add('active');
        });
    });
    
    // Form submission handling
    const textForm = document.getElementById('text-form');
    const urlForm = document.getElementById('url-form');
    const loader = document.querySelector('.loader');
    
    if (textForm) {
        textForm.addEventListener('submit', function(e) {
            e.preventDefault();
            loader.style.display = 'block';
            this.submit();
        });
    }
    
    if (urlForm) {
        urlForm.addEventListener('submit', function(e) {
            e.preventDefault();
            loader.style.display = 'block';
            this.submit();
        });
    }
    
    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-text');
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Show copied message
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        });
    });
    
    // Load trending news
    loadTrendingNews();
});

/**
 * Load trending news from the API
 */
function loadTrendingNews() {
    const newsContainer = document.getElementById('trending-news-container');
    if (!newsContainer) return;
    
    fetch('/trending-news')
        .then(response => response.json())
        .then(data => {
            if (data.articles && data.articles.length > 0) {
                let newsHTML = '';
                data.articles.forEach(article => {
                    newsHTML += `
                        <div class="news-card">
                            ${article.urlToImage ? `<img src="${article.urlToImage}" alt="${article.title}" class="news-image">` : ''}
                            <div class="news-content">
                                <span class="news-source">${article.source.name}</span>
                                <h3>${article.title}</h3>
                                <p class="news-description">${article.description || 'No description available.'}</p>
                                <a href="${article.url}" target="_blank" class="news-link">Read More</a>
                            </div>
                        </div>
                    `;
                });
                newsContainer.innerHTML = newsHTML;
            } else {
                newsContainer.innerHTML = '<p>No trending news available at the moment.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching trending news:', error);
            newsContainer.innerHTML = '<p>Failed to load trending news. Please try again later.</p>';
        });
}

/**
 * Draw gauge chart for confidence score
 * @param {string} elementId - The ID of the canvas element
 * @param {number} score - The confidence score (0-1)
 * @param {boolean} isFake - Whether the news is fake or real
 */
function drawGaugeChart(elementId, score, isFake) {
    const canvas = document.getElementById(elementId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height - 20;
    const radius = 80;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw background arc
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI, 0, false);
    ctx.lineWidth = 20;
    ctx.strokeStyle = '#e0e0e0';
    ctx.stroke();
    
    // Draw value arc
    const startAngle = Math.PI;
    const endAngle = Math.PI * (1 - score);
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle, true);
    ctx.lineWidth = 20;
    ctx.strokeStyle = isFake ? '#e74c3c' : '#2ecc71';
    ctx.stroke();
    
    // Draw center point
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI, false);
    ctx.fillStyle = '#333';
    ctx.fill();
    
    // Draw pointer
    const angle = Math.PI * (1 - score);
    const pointerLength = radius - 10;
    const pointerX = centerX + Math.cos(angle) * pointerLength;
    const pointerY = centerY + Math.sin(angle) * pointerLength;
    
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(pointerX, pointerY);
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#333';
    ctx.stroke();
    
    // Draw score text
    ctx.font = 'bold 24px Arial';
    ctx.fillStyle = '#333';
    ctx.textAlign = 'center';
    ctx.fillText(`${Math.round(score * 100)}%`, centerX, centerY + 50);
}