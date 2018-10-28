package com.gomoku.server.mongo.repository;

import com.gomoku.server.mongo.model.Match;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.util.List;

public interface MatchRepository extends MongoRepository<Match, String>{

    List<Match> findByUser1Id(String user1Id);

    Match findOneByMatchId(String matchId);

    @Query("{'$or':[{'user1Id':?0},{'user2Id':?0}]}")
    int countByUser1IdOrUser2Id(String user1Id);

}
