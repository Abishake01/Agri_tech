// main.js
document.addEventListener('DOMContentLoaded', function() {
    const voiceForm = document.getElementById('voice-form');
    if (voiceForm) {
        voiceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(voiceForm);
            const query = formData.get('query');
            
            fetch('/voice-query/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    query: query
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    // Update response display
                    const responseDiv = document.createElement('div');
                    responseDiv.className = 'mt-4 p-3 bg-light rounded';
                    responseDiv.innerHTML = `<h5>Response:</h5><p class="lead">${data.response}</p>`;
                    
                    const existingResponse = voiceForm.nextElementSibling;
                    if (existingResponse && existingResponse.classList.contains('bg-light')) {
                        existingResponse.replaceWith(responseDiv);
                    } else {
                        voiceForm.after(responseDiv);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error processing your request. Please try again.');
            });
        });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Voice recognition setup
    // Voice recognition setup
const startBtn = document.getElementById('start-recording');
if (startBtn) {
    // Check for browser support (modern syntax)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        startBtn.disabled = true;
        startBtn.title = "Voice input not supported in your browser";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US'; // Set language explicitly
    
    startBtn.addEventListener('click', function() {
        try {
            startBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Listening...';
            startBtn.disabled = true;
            recognition.start();
            
            // Set timeout for cases where recognition doesn't start
            setTimeout(() => {
                if (startBtn.innerHTML.includes('Listening')) {
                    recognition.stop();
                    startBtn.innerHTML = '<i class="bi bi-mic"></i> Voice Input';
                    startBtn.disabled = false;
                    alert('Voice recognition timed out. Please try again.');
                }
            }, 5000);
        } catch (error) {
            console.error('Recognition start error:', error);
            startBtn.innerHTML = '<i class="bi bi-mic"></i> Voice Input';
            startBtn.disabled = false;
            alert('Could not start voice recognition: ' + error.message);
        }
    });
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('id_query').value = transcript;
        startBtn.innerHTML = '<i class="bi bi-mic"></i> Voice Input';
        startBtn.disabled = false;
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        startBtn.innerHTML = '<i class="bi bi-mic"></i> Voice Input';
        startBtn.disabled = false;
        
        let errorMessage = 'Voice recognition error: ';
        switch(event.error) {
            case 'network':
                errorMessage += 'Network connectivity issue. Please check your internet connection.';
                break;
            case 'not-allowed':
                errorMessage += 'Microphone access was denied. Please allow microphone access.';
                break;
            case 'service-not-allowed':
                errorMessage += 'Speech recognition service not allowed.';
                break;
            default:
                errorMessage += event.error;
        }
        
        alert(errorMessage);
    };
    
    recognition.onend = function() {
        if (startBtn.innerHTML.includes('Listening')) {
            startBtn.innerHTML = '<i class="bi bi-mic"></i> Voice Input';
            startBtn.disabled = false;
        }
    };
}
});