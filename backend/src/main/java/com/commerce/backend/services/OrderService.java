package com.commerce.backend.services;

import com.commerce.backend.domain.Order;

import java.security.Principal;
import java.util.List;

public interface OrderService {
    Integer getAllOrdersCount(Principal principal);

    List<Order> getAllOrders(Principal principal, Integer page, Integer pageSize);

    Order postOrder(Principal principal, Order order);
}
