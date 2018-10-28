package com.gomoku.server.mongo.repository;

import com.gomoku.server.mongo.model.User;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface UserRepository extends MongoRepository<User, String>{
    public User findOneByUserName(String userName);
}
