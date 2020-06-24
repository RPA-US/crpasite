package com.commerce.backend.repositories;

import com.commerce.backend.domain.Discount;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DiscountRepository extends CrudRepository<Discount, Long> {
    Discount findByCode(String code);
}
