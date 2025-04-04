// General utility functions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Voice assistant AJAX
    const voiceForm = document.getElementById('voice-form');
    if (voiceForm) {
        voiceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(voiceForm);
            fetch('/voice-query/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
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
            .catch(error => console.error('Error:', error));
        });
    }
});