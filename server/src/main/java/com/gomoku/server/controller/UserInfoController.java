package com.gomoku.server.controller;

import com.gomoku.server.auth.LoginRequired;
import com.gomoku.server.mongo.model.User;
import com.gomoku.server.mongo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
@RequestMapping("/rank")
public class UserInfoController {

    @Autowired
    UserRepository userRepository;

    @LoginRequired
    @RequestMapping(value = "/all")
    public @ResponseBody Object topThree(){
//        Sort sort = new Sort(Sort.Direction.DESC, "rankScore");
//        Query query = new Query();
//        return userRepository.find(query.with(sort).limit(3));
        List<User> result = userRepository.findTop3ByOrderByRankScoreDesc();
        result.forEach(user -> {
            user.beforeSend();
        });
        return result;
    }

    @LoginRequired
    @RequestMapping(value = "/byscore/{score}")
    public @ResponseBody Object rankById(@PathVariable int score){
        return 1 + userRepository.countByRankScoreGreaterThan(score);
    }

    @LoginRequired
    @RequestMapping(value = "/byusername/{userName}")
    public @ResponseBody Object getInfoByUserName(@PathVariable String userName){
        User user = userRepository.findOneByUserName(userName);
        user.beforeSend();
        return user;
    }

}
