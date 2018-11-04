package com.gomoku.server.websocket;

import com.gomoku.server.websocket.model.GameStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.CopyOnWriteArraySet;

@Component
public class WebsocketHandler extends TextWebSocketHandler {

    //List<WebSocketSession> sessions = new CopyOnWriteArrayList();CopyOnWriteArraySet
    static private Map<String, GameStatus> rooms = new ConcurrentHashMap<>();
//
//    public WebsocketHandler() {
//        rooms = new ConcurrentHashMap<>();
//    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message)
            throws Exception {

        System.out.println("message: " + message.getPayload());

        String role = session.getHandshakeHeaders().get("role").get(0);
        String gameid = session.getHandshakeHeaders().get("gameid").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);
        if(rooms.containsKey(gameid)){

            // append every move in memory, send the history to new users
            //rooms.get(gameid).appendHistory(message);
            int player = rooms.get(gameid).getStone(role);

            String move = rooms.get(gameid).move(player, Integer.parseInt(message.getPayload()));
            TextMessage toSend = new TextMessage(move);

            if((role.equals("m")&&rooms.get(gameid).getMasterName().equals(userName)) ||
                    (role.equals("g")&&rooms.get(gameid).getGuestName().equals(userName))){

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
        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        super.afterConnectionEstablished(session);
        //session.getHandshakeHeaders();
        String role = session.getHandshakeHeaders().get("role").get(0);
        String gameid = session.getHandshakeHeaders().get("gameid").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);
        int masterStone = Integer.parseInt(session.getHandshakeHeaders().get("masterStone").get(0));
        if(role.equals("m")){
            if(!rooms.containsKey(gameid)) {

                // may throw invalid stone
                rooms.put(gameid, new GameStatus(masterStone));

                rooms.get(gameid).setMasterInfo(userName, session);
            }else if(rooms.get(gameid).getMaster()==null){
                rooms.get(gameid).setMasterInfo(userName, session);
            }else{
                throw new Exception("Already has a room.");
            }
            rooms.get(gameid).test();
            if(rooms.get(gameid).ready()){
                System.out.println("info: ready to start ......");
                rooms.get(gameid).start();
            }
        }else if(role.equals("g")){
            if(!rooms.containsKey(gameid)) {

                // may throw invalid stone
                rooms.put(gameid, new GameStatus(masterStone));

                rooms.get(gameid).setGuestInfo(userName, session);
            }else if(rooms.get(gameid).getGuest()==null){
                rooms.get(gameid).setGuestInfo(userName, session);
            }else{
                throw new Exception("The room already has a guest.");
            }
            rooms.get(gameid).test();
            if(rooms.get(gameid).ready()){
                System.out.println("info: ready to start ......");
                rooms.get(gameid).start();
            }
        }else if(role.equals("a")){
            if(!rooms.containsKey(gameid)){
                throw new Exception("No room.");
            }
            rooms.get(gameid).addAudience(session);
            rooms.get(gameid).test();
        }

        rooms.keySet().forEach(ele->{System.out.println(ele);});
        System.out.println(rooms.get(gameid).getMaster());
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        super.afterConnectionClosed(session, status);
        // System.out.println("closing: "+session.getHandshakeHeaders().get("role"));
        String role = session.getHandshakeHeaders().get("role").get(0);
        String gameid = session.getHandshakeHeaders().get("gameid").get(0);
        if(role.equals("m")){
            // TODO: judge winner and upload game info
            rooms.remove(gameid);
        }else if(role.equals("g")){
            // TODO: judge winner and upload game info
            rooms.get(gameid).setGuest(null);
        }else if(role.equals("a")){
            rooms.get(gameid).getAudience().remove(session);
        }
        rooms.keySet().forEach(ele->{System.out.println(ele);});

    }
}