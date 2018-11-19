package com.gomoku.server.rank;

import com.gomoku.server.mongo.model.User;
import com.gomoku.server.mongo.repository.UserRepository;
import com.gomoku.server.redis.repository.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;

public class RankSystem {
    @Autowired
    UserRepository userRepository;

    @Autowired
    RoomRepository roomRepository;

    public void calculate(String user1Name, String user2Name){
        User user1 = userRepository.findOneByUserName(user1Name);
        User user2 = userRepository.findOneByUserName(user2Name);


    }
}
