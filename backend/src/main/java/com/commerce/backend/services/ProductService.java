package com.commerce.backend.services;

import com.commerce.backend.domain.Product;

public interface ProductService {
    Product findById(Long id);
}
