document.addEventListener('DOMContentLoaded', function () {
    //
    // Password Creation Logic
    //
    const createProfileCheckbox = document.getElementById('create-profile');
    const passwordFields = document.getElementById('password-fields');
  
    if (createProfileCheckbox && passwordFields) {
      createProfileCheckbox.addEventListener('change', function () {
        if (createProfileCheckbox.checked) {
          passwordFields.style.display = 'block';
          passwordFields.setAttribute('aria-expanded', 'true');
        } else {
          passwordFields.style.display = 'none';
          passwordFields.setAttribute('aria-expanded', 'false');
        }
      });
    }

    /* Saved Address Selection Logic
     Find the <select id="id_saved_address"> that we built in checkout.html*/ 
    const savedSelect = document.getElementById('id_saved_address');
    if (savedSelect) {
      savedSelect.addEventListener('change', function () {
        // The <option> that’s currently selected
        const selOpt = this.options[this.selectedIndex];
  
        // If “Use a new address” (value = ""), clear all fields
        if (!selOpt.value) {
          document.getElementById('full_name').value = '';
          document.getElementById('phone_number').value = '';
          document.getElementById('street_address1').value = '';
          document.getElementById('street_address2').value = '';
          document.getElementById('town_or_city').value = '';
          document.getElementById('county').value = '';
          document.getElementById('eircode').value = '';
          document.getElementById('country').value = '';
          return;
        }
  
        // Otherwise, grab each data- attribute from the <option>
        const fullName   = selOpt.dataset.full_name    || '';
        const phoneNum   = selOpt.dataset.phone_number || '';
        const street1    = selOpt.dataset.street_address1 || '';
        const street2    = selOpt.dataset.street_address2 || '';
        const townOrCity = selOpt.dataset.town_or_city || '';
        const county     = selOpt.dataset.county       || '';
        const eircode    = selOpt.dataset.eircode      || '';
        const country    = selOpt.dataset.country      || '';
  
        // Copy them into the inputs by their IDs:
        document.getElementById('full_name').value       = fullName;
        document.getElementById('phone_number').value    = phoneNum;
        document.getElementById('street_address1').value = street1;
        document.getElementById('street_address2').value = street2;
        document.getElementById('town_or_city').value    = townOrCity;
        document.getElementById('county').value          = county;
        document.getElementById('eircode').value         = eircode;
        document.getElementById('country').value         = country;
        document.getElementById('billing_email').value = window.currentUserEmail;
    });
    }
});
  