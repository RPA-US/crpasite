package com.commerce.backend.repositories;

import com.commerce.backend.domain.EmailResetToken;
import com.commerce.backend.domain.User;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface EmailResetTokenRepository extends CrudRepository<EmailResetToken, Long> {
    EmailResetToken findByToken(String token);

    EmailResetToken findByUser(User user);
}
