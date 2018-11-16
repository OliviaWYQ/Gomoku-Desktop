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
    private Set<String> audience;
    private boolean playing;
    private String gameNo;

    public void Room(String roomName, String master){
        this.roomName = roomName;
        this.master = master;
        this.audience = new HashSet<>();

        this.playing = false;
        this.guest = null;
    }

    public boolean isValid(){
        if(master == null || roomName == null || master.isEmpty() || roomName.isEmpty()){
            return false;
        }
        if(audience == null){
            audience = new HashSet<>();
        }
        guest = null;
        playing = false;
        return true;
    }

    public boolean joinRoom(String audience){
        try{
            this.audience.add(audience);
            return true;
        }catch (Exception e){
            //System.out.println(e);
            return false;
        }
    }

    public boolean audienceTryPlay(String guest){
        if(this.playing==false && this.guest==null && this.audience.contains(guest)){
            try{
                this.audience.remove(guest);
                this.guest = guest;
                return true;
            }catch (Exception e){
                this.guest = null;
                this.audience.add(guest);
                return false;
            }
        }else{
            return false;
        }
    }

    public boolean guestTryWatch(String guest){
        if(this.guest.equals(guest)){
            try{
                this.audience.add(guest);
                this.guest = null;
                return true;
            }catch (Exception e){
                this.audience.remove(guest);
                this.guest = guest;
                return false;
            }
        }else{
            return false;
        }
    }

    public boolean leave(String userName){
        if(this.master.equals(userName)){
            return false;
        }else if(this.guest.equals(userName)){
            if(this.playing){
                // TODO: master win?
                return false;
            }else{
                this.guest = null;
                return true;
            }
        }else if(this.audience.contains(userName)){
            try{
                this.audience.remove(userName);
                return true;
            }catch (Exception e){
                this.audience.add(userName);
                return false;
            }
        }
        return false;
    }

    public boolean isPlaying() {
        return playing;
    }

    public void setPlaying(boolean playing) {
        this.playing = playing;
    }

    public String getGameNo() {
        return gameNo;
    }

    public void setGameNo(String gameNo) {
        this.gameNo = gameNo;
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

    public synchronized void setGuest(String guest) {
        this.guest = guest;
    }

    public Set<String> getAudience() {

        if(this.audience==null)
            this.audience = new HashSet<>();
        return audience;
    }

    public void setAudience(Set<String> audience) {
        this.audience = audience;
    }
}
