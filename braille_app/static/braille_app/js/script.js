class BrailleAutocorrectApp {
    constructor() {
        this.suggestionsCount = 0;
        this.totalResponseTime = 0;
        this.requestCount = 0;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateStats();
    }

    setupEventListeners() {
        const brailleInput = document.getElementById('brailleInput');
        const convertBtn = document.getElementById('convertBtn');
        const clearBtn = document.getElementById('clearBtn');

        // Real-time suggestions on input
        brailleInput.addEventListener('input', (e) => {
            this.handleInput(e.target.value);
        });

        // Convert button
        convertBtn.addEventListener('click', () => {
            this.convertText();
        });

        // Clear button
        clearBtn.addEventListener('click', () => {
            this.clearInput();
        });

        // Handle enter key for conversion
        brailleInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.convertText();
            }
        });
    }

    async handleInput(input) {
        if (!input.trim()) {
            this.clearSuggestions();
            return;
        }

        const words = input.trim().split(/\s+/);
        const lastWord = words[words.length - 1];

        if (lastWord.length > 0) {
            await this.getSuggestions(lastWord);
        }
    }

    async getSuggestions(word) {
        const startTime = performance.now();
        
        try {
            const response = await fetch('/suggestions/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ input: word })
            });

            const data = await response.json();
            const endTime = performance.now();
            
            this.updateResponseTime(endTime - startTime);

            if (data.suggestions) {
                this.displaySuggestions(data.suggestions);
                this.suggestionsCount += data.suggestions.length;
                this.updateStats();
            }
        } catch (error) {
            console.error('Error getting suggestions:', error);
            this.showError('Failed to get suggestions. Please try again.');
        }
    }

    async convertText() {
        const input = document.getElementById('brailleInput').value.trim();
        
        if (!input) {
            this.showError('Please enter some text to convert.');
            return;
        }

        const convertBtn = document.getElementById('convertBtn');
        const originalText = convertBtn.innerHTML;
        convertBtn.innerHTML = '<span class="loading-spinner"></span> Converting...';
        convertBtn.disabled = true;

        try {
            const response = await fetch('/convert/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ input: input })
            });

            const data = await response.json();

            if (data.converted_text) {
                this.displayConvertedText(data.converted_text);
            } else {
                this.showError('Failed to convert text. Please check your input.');
            }
        } catch (error) {
            console.error('Error converting text:', error);
            this.showError('Failed to convert text. Please try again.');
        } finally {
            convertBtn.innerHTML = originalText;
            convertBtn.disabled = false;
        }
    }

    displaySuggestions(suggestions) {
        const suggestionsContainer = document.getElementById('suggestions');
        
        if (!suggestions || suggestions.length === 0) {
            suggestionsContainer.innerHTML = '<div class="text-muted text-center">No suggestions found</div>';
            return;
        }

        let html = '';
        suggestions.forEach((suggestion, index) => {
            const confidencePercent = Math.round(suggestion.confidence * 100);
            html += `
                <div class="suggestion-item" tabindex="0" data-word="${suggestion.word}">
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="suggestion-word">${suggestion.word}</span>
                        <span class="suggestion-confidence">${confidencePercent}%</span>
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                    </div>
                    ${suggestion.distance > 0 ? `<small class="text-muted">Distance: ${suggestion.distance}</small>` : ''}
                </div>
            `;
        });

        suggestionsContainer.innerHTML = html;

        // Add click listeners to suggestions
        document.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                this.selectSuggestion(item.dataset.word);
            });

            item.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.selectSuggestion(item.dataset.word);
                }
            });
        });
    }

    selectSuggestion(word) {
        const brailleInput = document.getElementById('brailleInput');
        const currentValue = brailleInput.value.trim();
        const words = currentValue.split(/\s+/);
        
        if (words.length > 0) {
            words[words.length - 1] = word;
            brailleInput.value = words.join(' ') + ' ';
        } else {
            brailleInput.value = word + ' ';
        }

        brailleInput.focus();
        this.clearSuggestions();
    }

    displayConvertedText(text) {
        const convertedTextDiv = document.getElementById('convertedText');
        const convertedContent = document.getElementById('convertedContent');
        
        convertedContent.textContent = text;
        convertedTextDiv.style.display = 'block';
        
        // Scroll to converted text
        convertedTextDiv.scrollIntoView({ behavior: 'smooth' });
    }

    clearSuggestions() {
        const suggestionsContainer = document.getElementById('suggestions');
        suggestionsContainer.innerHTML = '<div class="text-muted text-center">Start typing to see suggestions...</div>';
    }

    clearInput() {
        document.getElementById('brailleInput').value = '';
        document.getElementById('convertedText').style.display = 'none';
        this.clearSuggestions();
        document.getElementById('brailleInput').focus();
    }

    updateResponseTime(time) {
        this.totalResponseTime += time;
        this.requestCount++;
        
        const avgTime = Math.round(this.totalResponseTime / this.requestCount);
        document.getElementById('responseTime').textContent = avgTime + 'ms';
    }

    updateStats() {
        // Update suggestions count
        document.getElementById('suggestionsCount').textContent = this.suggestionsCount;
        
        // Calculate accuracy rate (simplified)
        const accuracyRate = this.requestCount > 0 ? Math.round((this.suggestionsCount / this.requestCount) * 100) : 0;
        document.getElementById('accuracyRate').textContent = accuracyRate + '%';
    }

    showError(message) {
        // Create and show error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        const container = document.querySelector('.container');
        container.insertBefore(errorDiv, container.firstChild);
        
        // Remove after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BrailleAutocorrectApp();
});
