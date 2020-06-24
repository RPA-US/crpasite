package com.commerce.backend.repositories;

import com.commerce.backend.domain.Order;
import com.commerce.backend.domain.User;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OrderRepository extends PagingAndSortingRepository<Order, Long> {
    List<Order> findAllByUserOrderByDateDesc(User user, Pageable pageable);

    Integer countAllByUser(User user);
}
