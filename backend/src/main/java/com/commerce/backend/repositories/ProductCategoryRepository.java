package com.commerce.backend.repositories;

import com.commerce.backend.domain.ProductCategory;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface ProductCategoryRepository extends CrudRepository<ProductCategory, Long> {
    ProductCategory findByName(String category);

    List<ProductCategory> findAllByOrderByName();
}
