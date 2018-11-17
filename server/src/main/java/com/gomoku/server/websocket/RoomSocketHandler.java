package com.gomoku.server.websocket;

import com.gomoku.server.redis.model.Room;
import com.gomoku.server.redis.repository.RoomRepository;
import com.gomoku.server.websocket.model.GameStatus;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class RoomSocketHandler extends TextWebSocketHandler {


    // TODO: To verify the role of players.
    @Autowired
    RoomRepository roomRepository;

    final String JOIN_PREFIX = "J";
    final String LEAVE_PREFIX = "L";
    final String DELETE_SIGNAL = "D";
    final String START_SIGNAL = "S";

    static private Map<String, GameStatus> rooms = new ConcurrentHashMap<>();

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message){

        System.out.println("message: " + message.getPayload());

        // get handshake info
        String role = session.getHandshakeHeaders().get("role").get(0);
        String roomName = session.getHandshakeHeaders().get("roomName").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);

        String command = message.getPayload();

        Room room = roomRepository.findById(roomName).get();

        if(command.equals("join")){
            if(room.getGuest() == null) {
                room.setGuest(userName);
                roomRepository.save(room);
                try{
                    if(roomRepository.findById(roomName).get().getGuest().equals(userName)){
                        TextMessage toSend = new TextMessage(JOIN_PREFIX + userName);
                        session.sendMessage(toSend);
                        rooms.get(roomName).getMaster().sendMessage(toSend);
                    }
                } catch (Exception e){
                    System.out.println(e.getMessage());
                }
            }

        }else if(command.equals("leave")){
            if (!room.isPlaying() && room.getGuest().equals(userName)){
                room.setGuest(null);

                roomRepository.save(room);
                try{
                    TextMessage toSend = new TextMessage(LEAVE_PREFIX + userName);
                    session.sendMessage(toSend);
                    rooms.get(roomName).getMaster().sendMessage(toSend);

                } catch (Exception e){
                    System.out.println(e.getMessage());
                }

            }
        }else if(command.equals("delete")){
            if (!room.isPlaying() && room.getMaster().equals(userName)){
                roomRepository.delete(room);
                try{
                    TextMessage toSend = new TextMessage(DELETE_SIGNAL);
                    session.sendMessage(toSend);
                    rooms.get(roomName).getMaster().sendMessage(toSend);

                } catch (Exception e){
                    System.out.println(e.getMessage());
                }
            }
        }else if(command.equals("start")){

            if(room.getMaster().equals(userName) && (room.getGuest() != null)){
                room.setPlaying(true);
                try{

                    TextMessage toSend = new TextMessage(START_SIGNAL);
                    session.sendMessage(toSend);
                    rooms.get(roomName).getGuest().sendMessage(toSend);

                } catch (Exception e){
                    System.out.println(e.getMessage());
                }
            }

        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        super.afterConnectionEstablished(session);

        // get handshake info
        String role = session.getHandshakeHeaders().get("role").get(0);
        String roomName = session.getHandshakeHeaders().get("roomName").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);
        int masterStone = Integer.parseInt(session.getHandshakeHeaders().get("masterStone").get(0));

        if(role.equals("m")){

            // if the room is not init yet
            if(!rooms.containsKey(roomName)) {

                // create a room, may throw invalid stone
                rooms.put(roomName, new GameStatus(masterStone));

                // set master info, name and session
                rooms.get(roomName).setMasterInfo(userName, session);

                // if the room exists
            }else if(rooms.get(roomName).getMaster()==null){
                rooms.get(roomName).setMasterInfo(userName, session);
            }else{
                throw new Exception("Already has a room.");
            }
            rooms.get(roomName).test();



        }else if(role.equals("g")){

            // if the room is not init yet
            if(!rooms.containsKey(roomName)) {

                // create a room, may throw invalid stone
                rooms.put(roomName, new GameStatus(masterStone));

                // set guest info, name and session
                rooms.get(roomName).setGuestInfo(userName, session);

                // if the room exists
            }else if(rooms.get(roomName).getGuest()==null){
                rooms.get(roomName).setGuestInfo(userName, session);
            }else{
                throw new Exception("The room already has a guest.");
            }

            // testing info
            rooms.get(roomName).test();

            // start game
//            if(rooms.get(roomName).ready()){
//
//                // testing info
//                System.out.println("info: ready to start ......");
//
//                rooms.get(roomName).start();
//            }

        }else if(role.equals("a")){
            if(!rooms.containsKey(roomName)){
                throw new Exception("No room.");
            }
            rooms.get(roomName).addAudience(session);

            // send past moves
            rooms.get(roomName).sendAllMoves(session);

            // testing info
            rooms.get(roomName).test();
        }

        rooms.keySet().forEach(ele->{System.out.println(ele);});

        // testing info
        System.out.println(rooms.get(roomName).getMaster());
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        super.afterConnectionClosed(session, status);
        // System.out.println("closing: "+session.getHandshakeHeaders().get("role"));
        String role = session.getHandshakeHeaders().get("role").get(0);
        String roomName = session.getHandshakeHeaders().get("roomName").get(0);
        if(role.equals("m")){

            // now: ignore the game
            // TODO: judge winner and upload game info
            rooms.remove(roomName);

        }else if(role.equals("g")){

            // now: ignore the game
            // TODO: judge winner and upload game info
            rooms.remove(roomName);
            //rooms.get(roomName).setGuest(null);

        }else if(role.equals("a")){
            rooms.get(roomName).getAudience().remove(session);
        }

        // testing info
        rooms.keySet().forEach(ele->{System.out.println(ele);});

    }



}
