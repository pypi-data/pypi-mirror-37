export const formQuestion = () =>
    `<td>
        <input type="radio" name="emaillist" class="checker" value="yes"> ${gettext('Yes')}
        <input type="radio" name="emaillist" class="checker" value="no"> ${gettext('No')}
    </td><td>
        ${gettext('I would like to receive information about news and updates to the service by email.')}
    </td>`
