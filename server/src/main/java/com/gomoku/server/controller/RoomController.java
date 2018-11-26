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
import java.util.NoSuchElementException;
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

        // if .get() not found, it will throws a exception
        try{
            Room temp = roomRepository.findById(room.getRoomName()).get();
            return "Room name already existed.";
        }catch (NoSuchElementException e){
            roomRepository.save(room);
            return "Success";
        }
    }

    // Join a room and be a guest.
    @RequestMapping(value = "/join/{roomName}/{userName}")
    public @ResponseBody String joinRoom(@PathVariable("roomName") String roomName,
                                         @PathVariable("userName") String userName){

        // if .get() not found, it will throws a exception
        try{
            Room toJoin = roomRepository.findById(roomName).get();

            if (toJoin.getMaster().equals(userName)){
                return "You're master of the room.";
            }
            if (toJoin.getGuest() != null && toJoin.getGuest().equals(userName)){
                return "Success";
            } else if(toJoin.getGuest() == null || toJoin.getGuest().isEmpty()){
                try {
                    toJoin.setGuest(userName);
                    toJoin.setRoomStatus("Full");
                    roomRepository.save(toJoin);
                    if(roomRepository.findById(roomName).get().getGuest().equals(userName)){
                        return "Success";
                    }
                } catch (Exception e){
                    System.out.println("Failed!");
                    return e.getMessage();
                }
            }

            return "There is already a guest.";
        } catch (NoSuchElementException e){
            return "Room not found.";
        }


    }

    // Leave a room.
    @RequestMapping(value = "/leave/{roomName}/{userName}")
    public @ResponseBody String leaveRoom(@PathVariable("roomName") String roomName,
                                         @PathVariable("userName") String userName){
        // if .get() not found, it will throws a exception
        try{
            Room toLeave = roomRepository.findById(roomName).get();

            if (toLeave.getMaster().equals(userName)){
                return "You're master of the room.";
            }
            if (toLeave.getGuest() == null || toLeave.getGuest().isEmpty()){
                return "Success";
            } else if(toLeave.getGuest().equals(userName)){
                try {
                    toLeave.setGuest(null);
                    toLeave.setRoomStatus("Open");
                    roomRepository.save(toLeave);
                    if(roomRepository.findById(roomName).get().getGuest() == null){
                        return "Success";
                    }
                } catch (Exception e){
                    return e.getMessage();
                }
            }

            return "There is already a guest.";
        } catch (NoSuchElementException e){
            return "Room not found.";
        }
    }

    // Delete a room.
    @RequestMapping(value = "/delete/{roomName}/{userName}")
    public @ResponseBody String deleteRoom(@PathVariable("roomName") String roomName,
                                          @PathVariable("userName") String userName){
        // if .get() not found, it will throws a exception
        try{
            Room toDelete = roomRepository.findById(roomName).get();

            if (!toDelete.getMaster().equals(userName)){
                return "You're not a master.";
            }

            roomRepository.delete(toDelete);

            return "Success";
        } catch (NoSuchElementException e){
            return "Success";
        }
    }


//    // Guest ready.
//    @RequestMapping(value = "/ready/{roomName}/{userName}")
//    public @ResponseBody String readyToPlay(@PathVariable("roomName") String roomName,
//                                         @PathVariable("userName") String userName){
//        Room roomToUpdate = roomRepository.findById(roomName).get();
//        if (roomToUpdate == null) {
//            return "Room not found.";
//        }
//        if (roomToUpdate.getGuest() != userName) {
//            return "You cannot play in this room.";
//        }
//        if (!roomToUpdate.isReady()) {
//            try {
//                roomToUpdate.setReady(true);
//                roomRepository.save(roomToUpdate);
//                if(roomRepository.findById(userName).get().getGuest().equals(userName)){
//                    return "Success";
//                }
//            } catch (Exception e){
//                return e.getMessage();
//            }
//        }
//
//        return "Success";
//    }
//
//    // Guest unready.
//    @RequestMapping(value = "/unready/{roomName}/{userName}")
//    public @ResponseBody String unreadyToPlay(@PathVariable("roomName") String roomName,
//                                            @PathVariable("userName") String userName){
//        Room roomToUpdate = roomRepository.findById(roomName).get();
//        if (roomToUpdate == null) {
//            return "Room not found.";
//        }
//        if (roomToUpdate.getGuest() != userName) {
//            return "You cannot play in this room.";
//        }
//        if (roomToUpdate.isReady()) {
//            try {
//                roomToUpdate.setReady(false);
//                roomRepository.save(roomToUpdate);
//                if(roomRepository.findById(userName).get().getGuest().equals(userName)){
//                    return "Success";
//                }
//            } catch (Exception e){
//                return e.getMessage();
//            }
//        }
//
//        return "Success";
//    }

    // Search all rooms.
    @RequestMapping(value = "/all")
    public @ResponseBody List<Room> searchAllRoom(){
        Iterable<Room> itr = roomRepository.findAll();
        List<Room> rooms = new ArrayList<>();
        itr.forEach(e -> rooms.add(e));
        return rooms;
    }

    // Search a room by room name.
    @RequestMapping(value = "/{roomName}")
    public @ResponseBody Room searchRoomByRoomName(@PathVariable String roomName){
        return roomRepository.findById(roomName).get();
    }




}

