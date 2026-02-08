import { NamedPage } from 'vj/misc/PageLoader';

const page = new NamedPage('contest_tempuser', () => {
  
  // Copy password to clipboard
  window.copyPassword = function(button) {
    const password = button.getAttribute('data-password');
    const feedback = button.nextElementSibling;
    
    // Try using modern Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(password).then(() => {
        showCopyFeedback(feedback);
      }).catch(err => {
        // Fallback if Clipboard API fails
        fallbackCopyToClipboard(password, feedback);
      });
    } else {
      // Fallback for older browsers
      fallbackCopyToClipboard(password, feedback);
    }
  };
  
  function showCopyFeedback(feedback) {
    feedback.classList.add('show');
    setTimeout(() => {
      feedback.classList.remove('show');
    }, 2000);
  }
  
  function fallbackCopyToClipboard(text, feedback) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      showCopyFeedback(feedback);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
    document.body.removeChild(textArea);
  }
  
  // Attach click handlers to copy buttons
  document.querySelectorAll('.copy-password-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      copyPassword(this);
    });
  });
  
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
        // Update the password display
        const passwordCell = document.querySelector('#pwd-' + userId);
        if (passwordCell) {
          passwordCell.textContent = data.password;
        }
        // Update copy button data
        const copyBtn = passwordCell.parentElement.querySelector('.copy-password-btn');
        if (copyBtn) {
          copyBtn.setAttribute('data-password', data.password);
        }
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
  
  // Bulk sync all temp users (always updates for safety)
  window.syncAll = function() {
    if (!confirm($('body').attr('data-sync-confirm') || 'Are you sure you want to sync all temp users? This will update all user accounts.')) {
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
