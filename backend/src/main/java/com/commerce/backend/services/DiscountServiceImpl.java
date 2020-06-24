package com.commerce.backend.services;

import com.commerce.backend.repositories.CartRepository;
import com.commerce.backend.repositories.DiscountRepository;
import com.commerce.backend.repositories.UserRepository;
import com.commerce.backend.domain.Cart;
import com.commerce.backend.domain.Discount;
import com.commerce.backend.domain.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.security.Principal;

@Service
public class DiscountServiceImpl implements DiscountService {

    private final DiscountRepository discountRepository;
    private final UserRepository userRepository;
    private final PriceService priceService;
    private final CartRepository cartRepository;

    @Autowired
    public DiscountServiceImpl(DiscountRepository discountRepository, UserRepository userRepository,
                               PriceService priceService, CartRepository cartRepository) {
        this.discountRepository = discountRepository;
        this.userRepository = userRepository;
        this.priceService = priceService;
        this.cartRepository = cartRepository;
    }


    @Override
    public Cart applyDiscount(Principal principal, String code) {
        Discount discount = discountRepository.findByCode(code);
        if (discount == null) {
            throw new IllegalStateException("Discount code not found");
        }
        User user = userRepository.findByEmail(principal.getName());
        if (user == null) {
            throw new IllegalArgumentException("User not found");
        } else if (user.getCart() == null) {
            throw new IllegalArgumentException("Cart not found");
        }

        Cart cart = user.getCart();
        cart.setCartDiscount(discount);
        cart = priceService.calculatePrice(cart);
        cartRepository.save(cart);
        return cart;
    }
}
