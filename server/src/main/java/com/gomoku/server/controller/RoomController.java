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

    @RequestMapping(method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE)
    public @ResponseBody String creatRoom(@RequestBody Room room){
        if(roomRepository.findById(room.getRoomName())==null){
            roomRepository.save(room);
            return "Success";
        }else{
            return "User already created a room";
        }
    }

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

    @RequestMapping(value = "/all")
    public @ResponseBody List<Room> searchAllRoom(){
        Iterable<Room> itr = roomRepository.findAll();
        List<Room> rooms = new ArrayList<>();
        itr.forEach(e -> rooms.add(e));
        return rooms;
    }

    @RequestMapping(value = "/{roomName}")
    public @ResponseBody Room searchRoomByRoomName(@PathVariable String roomName){
//        Iterable<Room> itr = roomRepository.findAll();
//        List<Room> rooms = new ArrayList<>();
//        itr.forEach(e -> rooms.add(e));
        return roomRepository.findById(roomName).get();
    }
}

