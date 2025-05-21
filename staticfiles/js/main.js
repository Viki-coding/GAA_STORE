document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap toasts
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(toastElement => {
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    });

    // AJAX Add-to-Bag Functionality
    document.querySelectorAll('.add-to-bag-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault(); // Prevent the default form submission

            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the bag count in the navbar
                    const bagCount = document.getElementById('bag-count');
                    if (bagCount) {
                        bagCount.textContent = data.bag_count;
                    }

                    // Show a toast notification
                    const toastContainer = document.getElementById('toast-container');
                    const toast = document.createElement('div');
                    toast.className = 'toast custom-toast';
                    toast.innerHTML = `
                        <div class="toast-header bg-success text-white">
                            <strong class="mr-auto">Success</strong>
                            <button type="button" class="ml-2 mb-1 close text-white" data-dismiss="toast" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="toast-body">
                            ${data.message}
                        </div>
                    `;
                    toastContainer.appendChild(toast);
                    new bootstrap.Toast(toast).show();
                } else {
                    alert(data.message); // Fallback for errors
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});