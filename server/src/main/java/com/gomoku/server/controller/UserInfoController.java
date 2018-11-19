package com.gomoku.server.controller;

import com.gomoku.server.mongo.model.User;
import com.gomoku.server.mongo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class UserInfoController {

    @Autowired
    UserRepository userRepository;

    @RequestMapping(value = "/byid/{userName}")
    public @ResponseBody User searchMatches(@PathVariable String userName){
        //match.setId();
        //matchRepository.save(match);
        User user = userRepository.findOneByUserName(userName);
        user.beforeSend();
        return user;
        //return matchRepository.findByUser1Id(userId);
    }

    public User getUserInfoByName(String userName){
        User toSend = userRepository.findOneByUserName(userName);
        toSend.beforeSend();
        return toSend;
    }
}
