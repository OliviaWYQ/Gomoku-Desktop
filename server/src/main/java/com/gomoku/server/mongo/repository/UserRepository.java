package com.gomoku.server.mongo.repository;

import com.gomoku.server.mongo.model.User;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.util.List;

public interface UserRepository extends MongoRepository<User, String>{
    public User findOneByUserName(String userName);

    public List<User> findTop3ByOrderByRankScoreDesc();

    public long countByRankScoreGreaterThan(int rankScore);
}
