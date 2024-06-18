// document.getElementById('interviewForm').addEventListener('submit', function(event) {
//     event.preventDefault();

//     const company = document.getElementById('company').value;
//     const post = document.getElementById('post').value;
//     const includeAnswers = document.getElementById('includeAnswers').checked;

//     fetch('/generate_interview', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             company: company,
//             post: post,
//             includeAnswers: includeAnswers
//         }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('output').innerText = data.response;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// });

// document.addEventListener('DOMContentLoaded', function() {
//     // Event listener for interviewForm submission
//     document.getElementById('interviewForm').addEventListener('submit', function(event) {
//         event.preventDefault();

//         const company = document.getElementById('company').value;
//         const post = document.getElementById('post').value;

//         fetch('/generate_interview', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 company: company,
//                 post: post,
//                 includeAnswers: false  // Adjust this based on your logic
//             }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             const viewMode = prompt("Enter '1' to view questions one by one or '2' to view the full list:");
//             if (viewMode === '1') {
//                 window.location.href = data.redirect_one_by_one;
//             } else {
//                 window.location.href = data.redirect_full_list;
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//     });

//     // Optional: Event listener for includeAnswers checkbox (if still needed)
//     const includeAnswersCheckbox = document.getElementById('includeAnswers');
//     if (includeAnswersCheckbox) {
//         includeAnswersCheckbox.addEventListener('change', function() {
//             const includeAnswers = this.checked;
//             // Handle checkbox state change logic here
//         });
//     }
// });


document.addEventListener('DOMContentLoaded', function() {
    // Event listener for interviewForm submission
    document.getElementById('interviewForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const company = document.getElementById('company').value;
        const post = document.getElementById('post').value;
        const viewMode = document.getElementById('viewMode').value;

        fetch('/generate_interview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                company: company,
                post: post,
                includeAnswers: false,  // Adjust this based on your logic
                viewMode: viewMode  // Include viewMode in the request body
            }),
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

