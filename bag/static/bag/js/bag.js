// Enable/disable the gift message textarea based on the checkbox
document.addEventListener('DOMContentLoaded', function () {
    const giftCheckbox = document.getElementById('giftCheckbox');
    const giftMessage = document.getElementById('giftMessage');

    if (giftCheckbox) {
        giftCheckbox.addEventListener('change', function () {
            giftMessage.disabled = !this.checked;
        });
    }
});