package com.ml_springboot.demo_ml_springboot.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.ml_springboot.demo_ml_springboot.entity.User;

@Repository
public interface UserRepository extends JpaRepository<User,Long>{
        Optional<User> findByEmail(String email);

}
