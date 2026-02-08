import { NamedPage } from 'vj/misc/PageLoader';

const page = new NamedPage('contest_tempuser', () => {
  
  // Toggle password visibility
  window.togglePassword = function(userId) {
    const cell = document.getElementById('pwd-' + userId);
    const valueSpan = cell.querySelector('.password-value');
    const currentPassword = valueSpan.getAttribute('data-password');
    
    if (cell.classList.contains('password-hidden')) {
      valueSpan.textContent = currentPassword;
      cell.classList.remove('password-hidden');
    } else {
      valueSpan.textContent = '••••••••';
      cell.classList.add('password-hidden');
    }
  };
  
  // Regenerate password for a temp user
  window.regeneratePassword = function(userId) {
    if (!confirm($('body').attr('data-regenerate-confirm') || 'Are you sure you want to regenerate the password?')) {
      return;
    }
    
    // Find the form for this specific user
    const button = event.target;
    const form = $(button).closest('form')[0];
    const formData = new FormData(form);
    
    fetch(form.action, {
      method: 'POST',
      headers: {
        'Accept': 'application/json'
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const cell = document.getElementById('pwd-' + userId);
        const valueSpan = cell.querySelector('.password-value');
        valueSpan.setAttribute('data-password', data.password);
        valueSpan.textContent = data.password;
        cell.classList.remove('password-hidden');
        alert($('body').attr('data-regenerate-success') || 'Password regenerated successfully!');
      } else {
        alert($('body').attr('data-regenerate-error') || 'Error regenerating password');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert($('body').attr('data-regenerate-error') || 'Error regenerating password');
    });
  };
  
  // Bulk sync all unsynced temp users
  window.syncAll = function() {
    if (!confirm($('body').attr('data-sync-confirm') || 'Are you sure you want to sync all unsynced temp users?')) {
      return;
    }
    
    const form = document.getElementById('sync-all-form');
    const formData = new FormData(form);
    
    fetch(form.action, {
      method: 'POST',
      headers: {
        'Accept': 'application/json'
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        let msg = ($('body').attr('data-sync-success') || 'Successfully synced') + ' ' + 
                  data.synced_count + ' ' + 
                  ($('body').attr('data-sync-users') || 'temp users');
        if (data.errors && data.errors.length > 0) {
          msg += '\n\n' + ($('body').attr('data-sync-errors') || 'Errors:') + '\n' + data.errors.join('\n');
        }
        alert(msg);
        location.reload();
      } else {
        alert($('body').attr('data-sync-error') || 'Error syncing users');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert($('body').attr('data-sync-error') || 'Error syncing users');
    });
  };
  
  // Handle forms with custom HTTP methods (PATCH, DELETE)
  $('form[data-method]').on('submit', function(e) {
    e.preventDefault();
    
    const form = $(this);
    const method = form.attr('data-method');
    const formData = new FormData(this);
    
    fetch(form.attr('action'), {
      method: method,
      headers: {
        'Accept': 'application/json'
      },
      body: formData
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.error) {
        alert(data.error.message || ($('body').attr('data-operation-error') || 'Operation failed'));
      } else {
        // Success - reload the page to show updated data
        window.location.reload();
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert($('body').attr('data-operation-error') || 'Error performing operation');
    });
  });
  
});

export default page;
