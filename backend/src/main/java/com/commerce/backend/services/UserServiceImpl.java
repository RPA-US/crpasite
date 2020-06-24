package com.commerce.backend.services;

import com.commerce.backend.repositories.UserRepository;
import com.commerce.backend.forms.PasswordResetForm;
import com.commerce.backend.forms.UserForm;
import com.commerce.backend.domain.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.security.Principal;

@Service
public class UserServiceImpl implements UserService {


    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public UserServiceImpl(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public User register(UserForm userForm) {
        if (userRepository.existsByEmail(userForm.getEmail())) {
            throw new IllegalStateException("An account already exists with this email");
        }

        User user = new User();
        user.setEmail(userForm.getEmail());
        user.setPassword(passwordEncoder.encode(userForm.getPassword()));
        user.setEmailVerified(0);
        userRepository.save(user);
        return user;
    }


    @Override
    public User getUser(Principal principal) {
        return getUserFromPrinciple(principal);
    }

    @Override
    public User updateUser(Principal principal, User user) {
        User dbUser = getUserFromPrinciple(principal);
        dbUser.setFirstName(user.getFirstName());
        dbUser.setLastName(user.getLastName());
        dbUser.setAddress(user.getAddress());
        dbUser.setAddress2(user.getAddress2());
        dbUser.setCity(user.getCity());
        dbUser.setState(user.getState());
        dbUser.setZip(user.getZip());
        dbUser.setCountry(user.getCountry());
        dbUser.setPhone(user.getPhone());

        System.out.println(dbUser);
        userRepository.save(dbUser);
        return dbUser;
    }

    @Override
    public void resetPassword(Principal principal, PasswordResetForm passwordResetForm) {
        User user = getUserFromPrinciple(principal);
        if (!passwordEncoder.matches(passwordResetForm.getOldPassword(), user.getPassword())) {
            throw new IllegalArgumentException("Invalid password");
        }

        if (passwordEncoder.matches(passwordResetForm.getNewPassword(), user.getPassword())) {
            //throw new IllegalCallerException("Same password"); do not reveal user's password
            //just skip setting the new password since it is the same as the old one.
            return;
        }

        user.setPassword(passwordEncoder.encode(passwordResetForm.getNewPassword()));
        userRepository.save(user);
    }

    @Override
    public Boolean getVerificationStatus(Principal principal) {
        User user = getUserFromPrinciple(principal);
        return user.getEmailVerified() == 1;
    }

    private User getUserFromPrinciple(Principal principal) {
        if (principal == null || principal.getName() == null) {
            throw new IllegalArgumentException("Invalid access");
        }
        User user = userRepository.findByEmail(principal.getName());
        if (user == null) {
            throw new IllegalArgumentException("User not found");
        }
        return user;
    }
}
