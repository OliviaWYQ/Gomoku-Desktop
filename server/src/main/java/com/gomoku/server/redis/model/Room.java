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

    final static String ROOM_DEFAULT_STATUS = "Open";
    final static String ROOM_FULL_STATUS = "Full";
    final static String ROOM_PLAYING_STATUS = "Playing";

    private boolean playing;

    public Room(String roomName, String master){
        this.roomName = roomName;
        this.master = master;

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
        this.roomStatus = ROOM_DEFAULT_STATUS;
        return true;
    }

    public boolean isPlaying() {
        return playing;
    }

    public void setPlaying(boolean playing) {
        this.playing = playing;
    }

    public String getRoomName() {
        return roomName;
    }

    public String getMaster() {
        return master;
    }

    public String getGuest() {
        return guest;
    }

    public synchronized void setGuest(String guest) {
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

    public static String getDefaultStatus() {
        return ROOM_DEFAULT_STATUS;
    }

    public static String getFullStatus() {
        return ROOM_FULL_STATUS;
    }

    public static String getPlayingStatus() {
        return ROOM_PLAYING_STATUS;
    }
}
