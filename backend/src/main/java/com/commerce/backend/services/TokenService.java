package com.commerce.backend.services;

import com.commerce.backend.forms.EmailResetForm;
import com.commerce.backend.forms.PasswordForgotForm;
import com.commerce.backend.domain.User;

import java.security.Principal;

public interface TokenService {
    void createEmailResetToken(Principal principal, EmailResetForm emailResetForm, String requestUrl);

    void createEmailConfirmToken(User user, String requestUrl);

    void createPasswordResetToken(String email, String requestUrl);

    void validateEmail(String token);

    void validateEmailReset(String token);

    void validateForgotPasswordConfirm(String token);

    void validateForgotPassword(PasswordForgotForm passwordForgotForm);
}
