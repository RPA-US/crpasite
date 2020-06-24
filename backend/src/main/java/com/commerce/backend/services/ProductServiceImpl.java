package com.commerce.backend.services;

import com.commerce.backend.repositories.ProductRepository;
import com.commerce.backend.domain.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@CacheConfig(cacheNames = "product")
public class ProductServiceImpl implements ProductService {


    private final ProductRepository productRepository;

    @Autowired
    public ProductServiceImpl(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Override
    @Cacheable(key = "#id")
    public Product findById(Long id) {
        Optional optional = productRepository.findById(id);
        return optional.isPresent() ? (Product) optional.get() : null;
    }
}
