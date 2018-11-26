package com.gomoku.server.controller;

import com.gomoku.server.mongo.model.User;
import com.gomoku.server.mongo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class AuthController {

    @Autowired
    UserRepository userRepository;

    @RequestMapping(path = "/auth/login",method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE)
    public @ResponseBody String login(@RequestBody User user){
        if(user.getUserName()==null || user.getPass()==null){
            return "Wrong request format";
        }
        User userToLog = userRepository.findOneByUserName(user.getUserName());
        if(userToLog == null)
            return "User not exists";
        return userToLog.checkPass(user.getPass())?"Success": "Wrong passsword";
    }

    @RequestMapping(path = "/auth/signup",method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE)
    public @ResponseBody String signup(@RequestBody User user){
        if(user.getUserName()==null || user.getPass()==null){
            return "Wrong request format";
        }
        User userToLog = userRepository.findOneByUserName(user.getUserName());
        System.out.println(user.getUserName());
        if(userToLog != null)
            return "User name already exists";

        // init rank score, win rate
        // and encode the password
        user.beforeSave();
        userRepository.save(user);
        return "Success";
    }
}
