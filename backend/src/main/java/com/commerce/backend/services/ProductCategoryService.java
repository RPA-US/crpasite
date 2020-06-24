package com.commerce.backend.services;

import com.commerce.backend.domain.ProductCategory;

import java.util.List;

public interface ProductCategoryService {
    ProductCategory findByName(String category);

    List<ProductCategory> findAllByOrderByName();
}
