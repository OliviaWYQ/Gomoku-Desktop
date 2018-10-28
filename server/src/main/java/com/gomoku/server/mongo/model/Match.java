package com.gomoku.server.mongo.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Document(collection = "history")
public class Match {

    private String matchId;
    private String user1Id;
    private String user2Id;
    private List<Integer> moves;
    private boolean user1win;

    public void setId(){
        this.matchId = user1Id + '@' + user2Id + '@' + System.currentTimeMillis();
    }

    public String getMatchId() {
        return matchId;
    }

    public void setMatchId(String matchId) {
        this.matchId = matchId;
    }

    public String getUser1Id() {
        return user1Id;
    }

    public void setUser1Id(String user1Id) {
        this.user1Id = user1Id;
    }

    public String getUser2Id() {
        return user2Id;
    }

    public void setUser2Id(String user2Id) {
        this.user2Id = user2Id;
    }

    public List<Integer> getMoves() {
        return moves;
    }

    public void setMoves(List<Integer> moves) {
        this.moves = moves;
    }

    public boolean isUser1win() {
        return user1win;
    }

    public void setUser1win(boolean user1win) {
        this.user1win = user1win;
    }

}
