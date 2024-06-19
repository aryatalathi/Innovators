document.addEventListener('DOMContentLoaded', function() {
    // Event listener for interviewForm submission
    document.getElementById('interviewForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData();
        formData.append('company', document.getElementById('company').value);
        formData.append('post', document.getElementById('post').value);
        const viewMode = document.getElementById('viewMode').value;
        formData.append('viewMode', viewMode);
        // Append the file to the FormData object
        const resumeFile = document.getElementById('resume').files[0];
        formData.append('resume', resumeFile);

        fetch('/generate_interview', {
                method: 'POST',
                body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Redirect based on selected viewMode
            if (viewMode === '1') {
                window.location.href = data.redirect_one_by_one;
            } else {
                window.location.href = data.redirect_full_list;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
