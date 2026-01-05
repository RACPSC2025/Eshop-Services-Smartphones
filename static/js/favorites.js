function toggleFavorite(btn, productId) {
    fetch(`/products/favorite/toggle/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 403) {
            window.location.href = '/users/auth/';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status) {
            const icon = btn.querySelector('.material-icons');
            if (data.status === 'added') {
                icon.textContent = 'favorite';
                btn.classList.add('text-red-500');
                showToast('¡Agregado a favoritos!');
            } else {
                icon.textContent = 'favorite_border';
                btn.classList.remove('text-red-500');
                showToast('Eliminado de favoritos');
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

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

function showToast(message) {
    // Implementar si hay un sistema de toasts, si no, alert simple o ignorar
    console.log(message);
}
