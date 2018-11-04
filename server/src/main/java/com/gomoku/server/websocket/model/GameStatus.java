package com.gomoku.server.websocket.model;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class GameStatus {
    private WebSocketSession master;
    private WebSocketSession guest;
    private Set<WebSocketSession> audience;

    private String masterName;
    private String guestName;

    private int masterStone;
    private int guestStone;

    private GameLogic gameLogic;

    private List<TextMessage> historyMoves;

    public void addAudience(WebSocketSession audienceSession){
        if(master != audienceSession || guest != audienceSession){
            audience.add(audienceSession);
        }
    }

    public String move(int player, int pos) throws Exception {
        int winFlag = this.gameLogic.move(player, pos);
        return (winFlag<<24 | pos) + "";
    }

    private void appendHistory(TextMessage move){
        this.historyMoves.add(move);
    }
    public void setMasterInfo(String masterName, WebSocketSession masterSession){
        this.masterName = masterName;
        this.master = masterSession;
    }

    public int getStone(String role) throws Exception{
        if(role.equals("m")){
            return this.masterStone;
        }else if(role.equals("g")){
            return this.guestStone;
        }else{
            throw new Exception("Invalid role.");
        }
    }

    public void setGuestInfo(String guestName, WebSocketSession guestSession){
        this.guestName = guestName;
        this.guest = guestSession;
    }

    public int nextMove(){
        return this.gameLogic.getRound();
    }

    public GameStatus(int masterStone) throws Exception{
        this.gameLogic = new GameLogic();
        this.audience = new HashSet<>();
        this.historyMoves = new ArrayList<>();
        if(masterStone == 1){
            this.masterStone = 1;
            this.guestStone = 2;
        }else if(masterStone == 2){
            this.masterStone = 2;
            this.guestStone = 1;
        }else{
            throw new Exception("Invalid stones setting.");
        }
    }

    public void test(){
        System.out.println(this.masterName+" $ "+this.guestName+" $ ");
        audience.forEach(ele->{System.out.println(ele);});
    }

    public boolean ready(){
        return (this.master!=null && this.guest!=null && this.masterName!=null && this.guestName!=null);
    }

    public void start() throws IOException {
        this.master.sendMessage(new TextMessage("masterstart"));
        this.guest.sendMessage(new TextMessage("gueststart"));
    }

    public WebSocketSession getMaster() {
        return master;
    }

    public void setMaster(WebSocketSession master) {
        this.master = master;
    }

    public WebSocketSession getGuest() {
        return guest;
    }

    public void setGuest(WebSocketSession guest) {
        this.guest = guest;
    }

    public Set<WebSocketSession> getAudience() {
        return audience;
    }

    public void setAudience(Set<WebSocketSession> audience) {
        this.audience = audience;
    }

    public String getMasterName() {
        return masterName;
    }

    public void setMasterName(String masterName) {
        this.masterName = masterName;
    }

    public String getGuestName() {
        return guestName;
    }

    public void setGuestName(String guestName) {
        this.guestName = guestName;
    }

    public GameLogic getGameLogic() {
        return gameLogic;
    }

    public void setGameLogic(GameLogic gameLogic) {
        this.gameLogic = gameLogic;
    }

    public int getMasterStone() {
        return masterStone;
    }

    public void setMasterStone(int masterStone) {
        this.masterStone = masterStone;
    }

    public int getGuestStone() {
        return guestStone;
    }

    public void setGuestStone(int guestStone) {
        this.guestStone = guestStone;
    }
}
