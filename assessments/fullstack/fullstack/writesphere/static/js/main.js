// WriteSphere JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Like functionality
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const url = `/interactions/like/${postId}/`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.classList.add('liked');
                    this.innerHTML = '<i class="fas fa-heart"></i> Liked';
                } else {
                    this.classList.remove('liked');
                    this.innerHTML = '<i class="far fa-heart"></i> Like';
                }
                
                // Update likes count
                const likesCount = document.querySelector(`.likes-count-${postId}`);
                if (likesCount) {
                    likesCount.textContent = data.likes_count;
                }
                
                // Show message
                showToast(data.message, data.liked ? 'success' : 'info');
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred. Please try again.', 'danger');
            });
        });
    });

    // Comment functionality
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const content = this.querySelector('textarea[name="content"]').value;
            const parentId = this.querySelector('input[name="parent_id"]')?.value || '';
            
            const url = `/interactions/comment/add/${postId}/`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `content=${encodeURIComponent(content)}&parent_id=${parentId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Add comment to the DOM
                    addCommentToDOM(data, parentId);
                    // Clear form
                    this.querySelector('textarea[name="content"]').value = '';
                    // Show success message
                    showToast('Comment added successfully!', 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred. Please try again.', 'danger');
            });
        });
    });

    // Search form auto-submit
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInputs = searchForm.querySelectorAll('input, select');
        searchInputs.forEach(input => {
            input.addEventListener('change', function() {
                searchForm.submit();
            });
        });
    }

    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = parseInt(textarea.getAttribute('maxlength'));
        const charCounter = document.createElement('small');
        charCounter.className = 'form-text text-muted';
        charCounter.textContent = `0 / ${maxLength} characters`;
        textarea.parentNode.appendChild(charCounter);
        
        textarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            charCounter.textContent = `${currentLength} / ${maxLength} characters`;
            
            if (currentLength >= maxLength * 0.9) {
                charCounter.classList.add('text-warning');
            } else {
                charCounter.classList.remove('text-warning');
            }
        });
    });
});

// Helper function to add comment to DOM
function addCommentToDOM(commentData, parentId) {
    const commentHtml = `
        <div class="comment mb-3" id="comment-${commentData.comment_id}">
            <div class="d-flex">
                <div class="flex-grow-1">
                    <div class="d-flex justify-content-between">
                        <h6 class="mb-1">${commentData.author}</h6>
                        <small class="text-muted">${commentData.created_at}</small>
                    </div>
                    <p class="mb-0">${commentData.content}</p>
                    <div class="mt-2">
                        <button class="btn btn-sm btn-outline-primary reply-btn" data-comment-id="${commentData.comment_id}">
                            Reply
                        </button>
                        ${commentData.is_reply ? '' : `
                            <button class="btn btn-sm btn-outline-secondary edit-btn" data-comment-id="${commentData.comment_id}">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-outline-danger delete-btn" data-comment-id="${commentData.comment_id}">
                                Delete
                            </button>
                        `}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    let container;
    if (parentId) {
        container = document.querySelector(`#comment-${parentId} .replies`);
        if (!container) {
            container = document.createElement('div');
            container.className = 'replies ms-4';
            document.querySelector(`#comment-${parentId}`).appendChild(container);
        }
    } else {
        container = document.querySelector('.comments-list');
    }
    
    if (container) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = commentHtml;
        container.appendChild(tempDiv.firstElementChild);
    }
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

// Helper function to show toast messages
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = toastHtml;
    const toastElement = tempDiv.firstElementChild;
    toastContainer.appendChild(toastElement);
    
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

// Image preview for file inputs
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.querySelector(`#${input.id}-preview`);
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = `${input.id}-preview`;
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        preview.style.maxHeight = '200px';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

// Auto-save draft functionality
let autoSaveTimer;
const contentTextarea = document.querySelector('textarea[name="content"]');
if (contentTextarea) {
    contentTextarea.addEventListener('input', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(function() {
            // Save draft to localStorage
            localStorage.setItem('post_draft', contentTextarea.value);
            showToast('Draft auto-saved', 'info');
        }, 30000); // Auto-save after 30 seconds of inactivity
    });
    
    // Load draft from localStorage if exists
    const savedDraft = localStorage.getItem('post_draft');
    if (savedDraft && !contentTextarea.value) {
        contentTextarea.value = savedDraft;
        showToast('Draft restored from auto-save', 'info');
    }
}
