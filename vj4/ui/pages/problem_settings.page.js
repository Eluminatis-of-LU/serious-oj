import { NamedPage } from 'vj/misc/PageLoader';
import UserSelectAutoComplete from 'vj/components/autocomplete/UserSelectAutoComplete';
import { ConfirmDialog, ActionDialog } from 'vj/components/dialog';
import request from 'vj/utils/request';
import i18n from 'vj/utils/i18n';
import _ from 'lodash';
import tpl from 'vj/utils/tpl';
import delay from 'vj/utils/delay';
import Notification from 'vj/components/notification';

async function handleCategoryClick(ev) {
  const $target = $(ev.currentTarget);
  const $txt = $('[name="category"]');
  console.log($target);
  console.log($txt);
  $txt.val(`${$txt.val()}, ${$target.data('category')}`);
}

const page = new NamedPage('problem_settings', async () => {
  $(document).on('click', '.category-a', handleCategoryClick);
  $(document).on('click', '[name="problem-sidebar__show-category"]', ev => {
    $(ev.currentTarget).hide();
    $('[name="problem-sidebar__categories"]').show();
  });
  const addUserSelector = UserSelectAutoComplete.getOrConstruct($('.dialog__body--add-user [name="user"]'));
  const addUserDialog = new ActionDialog({
    $body: $('.dialog__body--add-user > div'),
    onDispatch(action) {
      if (action === 'ok') {
        if (addUserSelector.value() === null) {
          addUserSelector.focus();
          return false;
        }
      }
      return true;
    },
  });
  addUserDialog.clear = function () {
    addUserSelector.clear();
    return this;
  };
  async function handleClickAddUser() {
    const action = await addUserDialog.clear().open();
    if (action !== 'ok') {
      return;
    }
    const user = addUserSelector.value();
    try {
      await request.post(`${window.location.pathname}/users`, {
        operation: '',
        uid: user._id,
      });
      console.log('add user success');
      window.location.reload();
    } catch (error) {
      Notification.error(error.message);
    }
  }
  function ensureAndGetSelectedUsers() {
    const users = _.map(
      $('.problem-shared-users tbody [type="checkbox"]:checked'),
      ch => $(ch).closest('tr').attr('data-uid'),
    );
    if (users.length === 0) {
      Notification.error(i18n('Please select at least one user to perform this operation.'));
      return null;
    }
    return users;
  }

  async function handleClickRemoveSelected() {
    const selectedUsers = ensureAndGetSelectedUsers();
    if (selectedUsers === null) {
      return;
    }
    const action = await new ConfirmDialog({
      $body: tpl`
        <div class="typo">
          <p>${i18n('Confirm removing the selected users access from this problem?')}</p>
        </div>`,
    }).open();
    if (action !== 'yes') {
      return;
    }
    try {
      await request.delete(`${window.location.pathname}/users`, {
        operation: '',
        uid: selectedUsers,
      });
      Notification.success(i18n('Selected users have been removed from the domain.'));
      await delay(2000);
      window.location.reload();
    } catch (error) {
      Notification.error(error.message);
    }
  }

  $('[name="add_user"]').click(() => handleClickAddUser());
  $('[name="remove_selected"]').click(() => handleClickRemoveSelected());
});

export default page;
