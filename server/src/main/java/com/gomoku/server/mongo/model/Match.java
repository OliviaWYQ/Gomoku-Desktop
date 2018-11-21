package com.gomoku.server.mongo.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Document(collection = "history")
public class Match {

    @Id
    private String id;

    private String matchId;
    private String user1Id;
    private String user2Id;
    // deleted property: we can delete this, cause moves from client are encoded
    // private List<List<Integer>> moves;
    private List<Integer> encodedMoves;
    private int winFlag;

    public Match(String user1Id, String user2Id, List<Integer> encodedMoves, int winFlag) {
        this.user1Id = user1Id;
        this.user2Id = user2Id;
        this.encodedMoves = new ArrayList<>(encodedMoves);
        this.winFlag = winFlag;

        this.createId();
    }

    public void createId(){
        this.matchId = user1Id + '@' + user2Id + '@' + System.currentTimeMillis();
    }

    // deleted functions: seems we delete this, cause we can put en/decode in client
    /*
    public void encodeMoves(){
        encodedMoves = new ArrayList<>();
        for(List<Integer> pair: moves){
            encodedMoves.add(pair.get(0) | (pair.get(1)<<8));
        }
        moves = null;
    }

    public void decodeMoves(){
        moves = new ArrayList<>();
        for(Integer num: encodedMoves){
            moves.add(new ArrayList<Integer>(Arrays.asList(num&255, num>>8)));
        }
        encodedMoves = null;
    }

    public List<List<Integer>> getMoves() {
        return moves;
    }

    public void setMoves(List<List<Integer>> moves) {
        this.moves = moves;
    }
    */

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

    public List<Integer> getEncodedMoves() {
        return encodedMoves;
    }

    public void setEncodedMoves(List<Integer> encodedMoves) {
        this.encodedMoves = encodedMoves;
    }

    public int getWinFlagn() {
        return winFlag;
    }

    public void setWinFlag(int winFlag) {
        this.winFlag = winFlag;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
