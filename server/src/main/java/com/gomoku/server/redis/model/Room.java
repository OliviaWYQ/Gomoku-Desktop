package com.gomoku.server.redis.model;

import com.gomoku.server.mongo.model.User;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

import java.io.Serializable;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@RedisHash("Room")
public class Room implements Serializable{
    @Id
    private String roomName;

    private String master;
    private String guest;

    private boolean ready;
    private String roomStatus;

    private boolean playing;

    public Room(String roomName, String master){
        this.roomName = roomName;
        this.master = master;

        this.playing = false;
        this.guest = null;
    }

    public Room(){
        this.roomName = null;
        this.master = null;

        this.playing = false;
        this.guest = null;
    }

    public boolean isValid(){
        if(this.master == null || this.roomName == null || this.master.isEmpty() || this.roomName.isEmpty()){
            return false;
        }
        this.guest = null;
        this.playing = false;
        this.ready = false;
        this.roomStatus = "Open";
        return true;
    }

    public String getRoomName() {
        return roomName;
    }

    public void setRoomName(String roomName) {
        this.roomName = roomName;
    }

    public String getMaster() {
        return master;
    }

    public void setMaster(String master) {
        this.master = master;
    }

    public String getGuest() {
        return guest;
    }

    public void setGuest(String guest) {
        this.guest = guest;
    }

    public boolean isReady() {
        return ready;
    }

    public void setReady(boolean ready) {
        this.ready = ready;
    }

    public String getRoomStatus() {
        return roomStatus;
    }

    public void setRoomStatus(String roomStatus) {
        this.roomStatus = roomStatus;
    }

    public boolean isPlaying() {
        return playing;
    }

    public void setPlaying(boolean playing) {
        this.playing = playing;
    }
}
