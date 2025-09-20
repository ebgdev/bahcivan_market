function toggleLinkFields(linkType) {
    const categoryField = document.querySelector('.field-category');
    const productField = document.querySelector('.field-product');
    const urlField = document.querySelector('.field-custom_url');

    // Hide all fields first
    if (categoryField) categoryField.style.display = 'none';
    if (productField) productField.style.display = 'none';
    if (urlField) urlField.style.display = 'none';

    // Show the relevant field based on selection
    if (linkType === 'category' && categoryField) {
        categoryField.style.display = 'block';
    } else if (linkType === 'product' && productField) {
        productField.style.display = 'block';
    } else if (linkType === 'url' && urlField) {
        urlField.style.display = 'block';
    }
}

function loadToBanner(bannerId) {
    if (confirm('Are you sure you want to load this banner?')) {
        fetch('/admin/load-banner/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                'banner_id': bannerId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Banner loaded successfully!');
                location.reload();
            } else {
                alert('Error loading banner: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while loading the banner.');
        });
    }
}

// Initialize field visibility when page loads
document.addEventListener('DOMContentLoaded', function() {
    const linkTypeField = document.querySelector('#id_link_type');
    if (linkTypeField) {
        toggleLinkFields(linkTypeField.value);
        linkTypeField.addEventListener('change', function() {
            toggleLinkFields(this.value);
        });
    }
});