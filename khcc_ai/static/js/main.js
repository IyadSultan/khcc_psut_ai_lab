// General utility functions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// CSRF token setup for AJAX requests
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Setup AJAX headers
function setupAjaxHeaders() {
    const csrftoken = getCSRFToken();
    return {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
    };
}