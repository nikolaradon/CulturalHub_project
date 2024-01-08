// comment.js

document.addEventListener("DOMContentLoaded", function () {
    if (document.body.classList.contains('comment-page')) {
        document.getElementById('add-comment-button').addEventListener('click', function () {
            const commentText = prompt('Enter your comment:');
            if (commentText) {
                fetch('/api/add-comment', {
                    method: 'POST',
                    body: JSON.stringify({ text: commentText }),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                })
                .catch(error => console.error('Error:', error));
            }
        });
    }


    const commentForm = document.getElementById('comment-form');
    const commentsContainer = document.getElementById('comments-container');

    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(commentForm);

            fetch(commentForm.action, {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const commentText = data.comment_text;
                        const newComment = document.createElement('p');
                        newComment.innerHTML = `${data.username} - Now - ${commentText}`;
                        commentsContainer.appendChild(newComment);

                        commentForm.reset();
                    } else {
                        console.error(data.errors);
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }
});
