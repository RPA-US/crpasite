package com.commerce.backend.services;


import com.commerce.backend.forms.PasswordResetForm;
import com.commerce.backend.forms.UserForm;
import com.commerce.backend.domain.User;

import java.security.Principal;

public interface UserService {

    /* Public */
    User register(UserForm userForm);

    /* Secured */
    User getUser(Principal principal);

    User updateUser(Principal principal, User user);

    void resetPassword(Principal principal, PasswordResetForm passwordResetForm);

    Boolean getVerificationStatus(Principal principal);
}
