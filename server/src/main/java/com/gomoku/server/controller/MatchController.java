package com.gomoku.server.controller;

import com.gomoku.server.mongo.model.Match;
import com.gomoku.server.mongo.repository.MatchRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/match")
public class MatchController {

    @Autowired
    MatchRepository matchRepository;

    @RequestMapping(method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE)
        public @ResponseBody void creatMatch(@RequestBody Match match){
            match.setId();
            matchRepository.save(match);
    }

    @RequestMapping(value = "/byuser/{userId}")
    public @ResponseBody List<Match> searchMatches(@PathVariable String userId){
        //match.setId();
        //matchRepository.save(match);
        return matchRepository.findByUser1Id(userId);
    }

    @RequestMapping(value = "/byid/{matchId}")
    public @ResponseBody Match searchMatch(@PathVariable String matchId){
        //match.setId();
        //matchRepository.save(match);
        return matchRepository.findOneByMatchId(matchId);
    }

//    @RequestMapping(value = "/info/{userId}")
//    public @ResponseBody Match searchMatch(@PathVariable String matchId){
//        //match.setId();
//        //matchRepository.save(match);
//        return matchRepository.findOneByMatchId(matchId);
//    }


}
