document.getElementById('interviewForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const company = document.getElementById('company').value;
    const post = document.getElementById('post').value;
    const includeAnswers = document.getElementById('includeAnswers').checked;

    fetch('/generate_interview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            company: company,
            post: post,
            includeAnswers: includeAnswers
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.response;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

