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
        if(roomRepository.findById(room.getRoomName())==null){
            roomRepository.save(room);
            return "Success";
        }else{
            return "User already created a room";
        }
    }

    // Join a room and be an audience.
    @RequestMapping(value = "/join/{roomName}/{userName}")
    public @ResponseBody String joinRoom(@PathVariable("roomName") String roomName,
                                         @PathVariable("userName") String userName){
        Room toJoin = roomRepository.findById(roomName).get();
        if(toJoin==null){
            return "Room not exists.";
        }
        if(toJoin.getMaster()==userName || toJoin.getGuest()==userName || toJoin.getAudience().contains(userName)){
            return "Already in room.";
        }else{
            if(toJoin.joinRoom(userName)){
                roomRepository.save(toJoin);
                return "Success";
            }else{
                return "failed";
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
//        Iterable<Room> itr = roomRepository.findAll();
//        List<Room> rooms = new ArrayList<>();
//        itr.forEach(e -> rooms.add(e));
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
        if(toModify.getMaster()==userName){
            return "Is master.";
        }else if(toModify.getGuest()==userName){
            return "Is guest.";
        }else if(toModify.getAudience().contains(userName)){
            try{
                toModify.getAudience().remove(userName);
                toModify.setGuest(userName);
                roomRepository.save(toModify);
                return "Success.";
            }catch (Exception e){
                toModify.getAudience().add(userName);
                toModify.setGuest(null);
                return "Failed.";
            }
        }else{
            return "Be audience first.";
        }
    }

    // TODO: Become an audience, from a guest.

    // TODO: Leave a room.
}

