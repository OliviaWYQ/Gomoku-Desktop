package com.gomoku.server.controller;

import com.gomoku.server.mongo.model.Match;
import com.gomoku.server.mongo.repository.MatchRepository;
import com.gomoku.server.redis.model.Room;
import com.gomoku.server.redis.repository.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

@Controller
@RequestMapping("/room")
public class RoomController {

    @Autowired
    RoomRepository roomRepository;

    // Create a new room.
    @RequestMapping(method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE)
    public @ResponseBody String creatRoom(@RequestBody Room room){
        if(!room.isValid()){
            return "Failed, invalid message format.";
        }
        if(roomRepository.findById(room.getRoomName())==null){
            roomRepository.save(room);
            return "Success";
        }else{
            return "User already created a room.";
        }
    }

    // Join a room and be an audience.
    @RequestMapping(value = "/join/{roomName}/{userName}")
    public @ResponseBody String joinRoom(@PathVariable("roomName") String roomName,
                                         @PathVariable("userName") String userName){
        Room toJoin = roomRepository.findById(roomName).get();
        if (toJoin==null){
            return "Room not exists.";
        }
        if (toJoin.getMaster().equals(userName) || toJoin.getGuest().equals(userName) || toJoin.getAudience().contains(userName)){
            return "Already in room.";
        } else {
            try {
                if(toJoin.joinRoom(userName)){
                    roomRepository.save(toJoin);
                    return "Success";
                }else{
                    return "Failed, try again.";
                }
            } catch (Exception e){
                return e.getMessage();
            }
        }
    }

    // Search all rooms.
    @RequestMapping(value = "/all")
    public @ResponseBody List<Room> searchAllRoom(){
        Iterable<Room> itr = roomRepository.findAll();
        List<Room> rooms = new ArrayList<>();
        itr.forEach(e -> rooms.add(e));
        return rooms;
    }

    // Search a room bu room name.
    @RequestMapping(value = "/{roomName}")
    public @ResponseBody Room searchRoomByRoomName(@PathVariable String roomName){
        return roomRepository.findById(roomName).get();
    }

    // Try to become a guest, from an audience.
    @RequestMapping(value = "/beguest/{roomName}/{userName}")
    public @ResponseBody String becomeGuest(@PathVariable("roomName") String roomName,
                                         @PathVariable("userName") String userName){
        Room toModify = roomRepository.findById(roomName).get();
        if(toModify==null){
            return "Room not exists.";
        }
        if(toModify.getMaster().equals(userName)){
            return "Failed, you're a master.";
        }else if(toModify.getGuest().equals(userName)){
            return "Success";
        }else if(toModify.getAudience().contains(userName)){
            try{
                toModify.getAudience().remove(userName);
                toModify.setGuest(userName);
                roomRepository.save(toModify);
                return "Success";
            }catch (Exception e){
                toModify.getAudience().add(userName);
                toModify.setGuest(null);
                return "Failed, try again.";
            }
        }else{
            return "You're not in the room.";
        }
    }

    // Become an audience, from a guest.
    @RequestMapping(value = "/beaudience/{roomName}/{userName}")
    public @ResponseBody String becomeAudince(@PathVariable("roomName") String roomName,
                                            @PathVariable("userName") String userName){
        Room toModify = roomRepository.findById(roomName).get();
        if(toModify==null){
            return "Room not exists.";
        }
        if(toModify.getMaster().equals(userName)){
            return "Failed, you're a master.";
        }else if(toModify.getGuest().equals(userName)){
            try{
                toModify.getAudience().add(userName);
                toModify.setGuest(null);
                roomRepository.save(toModify);
                return "Success";
            }catch (Exception e){
                toModify.getAudience().remove(userName);
                toModify.setGuest(userName);
                return "Failed, try again.";
            }
        }else if(toModify.getAudience().contains(userName)){
            return "Success";
        }else{
            return "You're not in the room.";
        }
    }


    // TODO: Leave a room.
    @RequestMapping(value = "/leave/{roomName}/{userName}")
    public @ResponseBody String leaveRoom(@PathVariable("roomName") String roomName,
                                              @PathVariable("userName") String userName){
        Room toLeave = roomRepository.findById(roomName).get();
        if(toLeave==null){
            return "Room not exists.";
        }
        if(toLeave.getMaster().equals(userName)){
            // Delete the room
            if (toLeave.isPlaying()){
                return "Failed, is playing.";
            }else{
                roomRepository.delete(toLeave);
                return "Success";
            }

        }else if(toLeave.getGuest().equals(userName)){
            try{
                toLeave.getAudience().add(userName);
                toLeave.setGuest(null);
                //roomRepository.save(toLeave);
                roomRepository.delete(toLeave);
                return "Success";
            }catch (Exception e){
                toLeave.getAudience().remove(userName);
                toLeave.setGuest(userName);
                return "Failed, try again.";
            }
        }else if(toLeave.getAudience().contains(userName)){
            return "Success";
        }else{
            return "You're not in the room.";
        }
    }
}

