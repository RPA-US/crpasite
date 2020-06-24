package com.commerce.backend.validator;

import com.commerce.backend.forms.PasswordForgotForm;
import com.commerce.backend.forms.PasswordResetForm;
import com.commerce.backend.forms.UserForm;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class PasswordMatchesValidator
        implements ConstraintValidator<PasswordMatches, Object> {

    @Override
    public void initialize(PasswordMatches constraintAnnotation) {
    }

    @Override
    public boolean isValid(Object obj, ConstraintValidatorContext context) {
        if (obj instanceof UserForm) {
            UserForm user = (UserForm) obj;
            return user.getPassword().equals(user.getPasswordRepeat());
        } else if (obj instanceof PasswordResetForm) {
            PasswordResetForm passwordResetForm = (PasswordResetForm) obj;
            return passwordResetForm.getNewPassword().equals(passwordResetForm.getNewPasswordConfirm());
        } else if (obj instanceof PasswordForgotForm) {
            PasswordForgotForm passwordForgotForm = (PasswordForgotForm) obj;
            return passwordForgotForm.getNewPassword().equals(passwordForgotForm.getNewPasswordConfirm());
        }

        return false;

    }
}