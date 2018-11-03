package com.gomoku.server.socket.model;

public class OutMessage {
    private String from;
    private Integer position;
    private Integer winFlag;

    public OutMessage(String from, Integer position, Integer winFlag) {
        this.from = from;
        this.position = position;
        this.winFlag = winFlag;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public Integer getPosition() {
        return position;
    }

    public void setPosition(Integer position) {
        this.position = position;
    }

    public Integer getWinFlag() {
        return winFlag;
    }

    public void setWinFlag(Integer winFlag) {
        this.winFlag = winFlag;
    }
}
