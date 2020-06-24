package com.commerce.backend.services;

import com.commerce.backend.repositories.ProductCategoryRepository;
import com.commerce.backend.domain.ProductCategory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
@CacheConfig(cacheNames = "product_category")
public class ProductCategoryServiceImpl implements ProductCategoryService {


    private final ProductCategoryRepository productCategoryRepository;

    @Autowired
    public ProductCategoryServiceImpl(ProductCategoryRepository productCategoryRepository) {
        this.productCategoryRepository = productCategoryRepository;
    }

    @Override
    @Cacheable(key = "#category")
    public ProductCategory findByName(String category) {
        return productCategoryRepository.findByName(category);
    }

    @Override
    @Cacheable(key = "#root.methodName")
    public List<ProductCategory> findAllByOrderByName() {
        return productCategoryRepository.findAllByOrderByName();
    }
}
