package com.commerce.backend.repositories;

import com.commerce.backend.domain.PasswordForgotToken;
import com.commerce.backend.domain.User;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PasswordForgotTokenRepository extends CrudRepository<PasswordForgotToken, Long> {
    PasswordForgotToken findByToken(String token);

    PasswordForgotToken findByUser(User user);
}
