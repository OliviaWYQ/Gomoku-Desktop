package com.gomoku.server.mongo.model;

import org.mindrot.jbcrypt.BCrypt;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "user")
public class User{

    @Id
    private String userName;
    private String pass;

    private int rankScore;
    private int winMatchNum;
    private int totalMatchNum;

    public void beforeSave(){
        this.rankScore = 1000;
        this.winMatchNum = 0;
        this.totalMatchNum = 0;

        this.encodePass();
    }

    public void beforeSend(){
        this.pass = null;
    }

    public String getUserName() {
        return userName;
    }

    public String getPass() {
        return pass;
    }

    public void encodePass(){
        pass = BCrypt.hashpw(this.pass, BCrypt.gensalt());
    }

    public boolean checkPass(String rawPass){
        return BCrypt.checkpw(rawPass, this.pass);
    }

    public int getRankScore() {
        return rankScore;
    }

    public void setRankScore(int rankScore) {
        this.rankScore = rankScore;
    }

    public int getWinMatchNum() {
        return winMatchNum;
    }

    public void setWinMatchNum(int winMatchNum) {
        this.winMatchNum = winMatchNum;
    }

    public int getTotalMatchNum() {
        return totalMatchNum;
    }

    public void setTotalMatchNum(int totalMatchNum) {
        this.totalMatchNum = totalMatchNum;
    }
}

