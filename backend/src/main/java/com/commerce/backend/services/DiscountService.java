package com.commerce.backend.services;

import com.commerce.backend.domain.Cart;

import java.security.Principal;

public interface DiscountService {
    Cart applyDiscount(Principal principal, String code);
}
