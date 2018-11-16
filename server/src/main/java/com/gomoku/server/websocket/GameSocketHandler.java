package com.gomoku.server.websocket;

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
public class GameSocketHandler extends TextWebSocketHandler {

    // 5 x
    // 5 y
    // 2 player
    // 2 ensure
    // 3 winFlag
    // 8 move num
    // = 25

    // TODO: To verify the role of players.
    @Autowired
    RoomRepository roomRepository;

    static private Map<String, GameStatus> rooms = new ConcurrentHashMap<>();

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message)
            throws Exception {

        System.out.println("message: " + message.getPayload());

        // get handshake info
        String role = session.getHandshakeHeaders().get("role").get(0);
        String gameid = session.getHandshakeHeaders().get("gameid").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);

        if(rooms.containsKey(gameid)){

            // only master and guest can put stones
            if((role.equals("m")&&rooms.get(gameid).getMasterName().equals(userName)) ||
                    (role.equals("g")&&rooms.get(gameid).getGuestName().equals(userName))){

                // check whether the stone fit the role
                int player = rooms.get(gameid).getStone(role);
                // toSend store the info will be send to all players
                // including winFlag
                TextMessage toSend = rooms.get(gameid).move(player, message);

                // send to all players
                rooms.get(gameid).getGuest().sendMessage(toSend);
                rooms.get(gameid).getMaster().sendMessage(toSend);
                rooms.get(gameid).getAudience().forEach(s -> {
                    try {
                        s.sendMessage(toSend);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                });

            }else{
                throw new Exception("Invalid message.");
            }
        }else{
            throw new Exception("No room.");
        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        super.afterConnectionEstablished(session);

        // get handshake info
        String role = session.getHandshakeHeaders().get("role").get(0);
        String gameid = session.getHandshakeHeaders().get("gameid").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);
        int masterStone = Integer.parseInt(session.getHandshakeHeaders().get("masterStone").get(0));

        if(role.equals("m")){

            // if the room is not init yet
            if(!rooms.containsKey(gameid)) {

                // create a room, may throw invalid stone
                rooms.put(gameid, new GameStatus(masterStone));

                // set master info, name and session
                rooms.get(gameid).setMasterInfo(userName, session);

            // if the room exists
            }else if(rooms.get(gameid).getMaster()==null){
                rooms.get(gameid).setMasterInfo(userName, session);
            }else{
                throw new Exception("Already has a room.");
            }
            rooms.get(gameid).test();
            if(rooms.get(gameid).ready()){

                // testing info
                System.out.println("info: ready to start ......");

                rooms.get(gameid).start();
            }
        }else if(role.equals("g")){

            // if the room is not init yet
            if(!rooms.containsKey(gameid)) {

                // create a room, may throw invalid stone
                rooms.put(gameid, new GameStatus(masterStone));

                // set guest info, name and session
                rooms.get(gameid).setGuestInfo(userName, session);

            // if the room exists
            }else if(rooms.get(gameid).getGuest()==null){
                rooms.get(gameid).setGuestInfo(userName, session);
            }else{
                throw new Exception("The room already has a guest.");
            }

            // testing info
            rooms.get(gameid).test();

            if(rooms.get(gameid).ready()){

                // testing info
                System.out.println("info: ready to start ......");

                rooms.get(gameid).start();
            }
        }else if(role.equals("a")){
            if(!rooms.containsKey(gameid)){
                throw new Exception("No room.");
            }
            rooms.get(gameid).addAudience(session);

            // send past moves
            rooms.get(gameid).sendAllMoves(session);

            // testing info
            rooms.get(gameid).test();
        }

        rooms.keySet().forEach(ele->{System.out.println(ele);});

        // testing info
        System.out.println(rooms.get(gameid).getMaster());
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        super.afterConnectionClosed(session, status);
        // System.out.println("closing: "+session.getHandshakeHeaders().get("role"));
        String role = session.getHandshakeHeaders().get("role").get(0);
        String gameid = session.getHandshakeHeaders().get("gameid").get(0);
        if(role.equals("m")){

            // now: ignore the game
            // TODO: judge winner and upload game info
            rooms.remove(gameid);

        }else if(role.equals("g")){

            // now: ignore the game
            // TODO: judge winner and upload game info
            rooms.remove(gameid);
            //rooms.get(gameid).setGuest(null);

        }else if(role.equals("a")){
            rooms.get(gameid).getAudience().remove(session);
        }

        // testing info
        rooms.keySet().forEach(ele->{System.out.println(ele);});

    }
}