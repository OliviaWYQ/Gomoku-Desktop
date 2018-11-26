package com.gomoku.server.websocket;

import com.gomoku.server.mongo.repository.MatchRepository;
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
public class GameSocketHandler extends TextWebSocketHandler {

    static volatile private Map<String, GameStatus> rooms = new ConcurrentHashMap<>();

    final int START_SIGNAL = -1;
    final int GUEST_READY_SIGNAL = -2;
    final int GUEST_UNREADY_SIGNAL = -3;
    final int GUEST_LEAVE_SIGNAL = -4;
    final int MASTER_DELETE_SIGNAL = -5;
    final int END_SIGNAL = -6;
    final int BLACK_STONE_SIGNAL = -7;
    final int WHITE_STONE_SIGNAL = -8;

    final TextMessage START_SIGNAL_MESSAGE = new TextMessage(START_SIGNAL + "");
    final TextMessage GUEST_READY_SIGNALL_MESSAGE = new TextMessage(GUEST_READY_SIGNAL + "");
    final TextMessage GUEST_UNREADY_SIGNAL_MESSAGE = new TextMessage(GUEST_UNREADY_SIGNAL + "");
    final TextMessage GUEST_LEAVE_SIGNAL_MESSAGE = new TextMessage(GUEST_LEAVE_SIGNAL + "");
    final TextMessage MASTER_DELETE_SIGNAL_MESSAGE = new TextMessage(MASTER_DELETE_SIGNAL + "");
    final TextMessage END_SIGNAL_MESSAGE = new TextMessage(END_SIGNAL + "");

    final TextMessage BLACK_STONE_SIGNAL_MESSAGE = new TextMessage(BLACK_STONE_SIGNAL + "");
    final TextMessage WHITE_STONE_SIGNAL_MESSAGE = new TextMessage(WHITE_STONE_SIGNAL + "");

    @Autowired
    MatchRepository matchRepository;

    @Autowired
    RoomRepository roomRepository;

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message){

        System.out.println("message: " + message.getPayload());

        // get handshake info
        String role = session.getHandshakeHeaders().get("role").get(0);
        String roomName = session.getHandshakeHeaders().get("roomName").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);

        if(rooms.containsKey(roomName)){

            // only master and guest can put stones
            // and send control signals
            if((role.equals("m")&&rooms.get(roomName).getMasterName().equals(userName)) ||
                    (role.equals("g")&&rooms.get(roomName).getGuestName().equals(userName))){

                // contains control signals and position info
                if (message.getPayload().charAt(0) == 'J'){
                    if(role.equals("g")){
                        try {

                            // test info
                            System.out.println("guest name: " + rooms.get(roomName).getGuestName());

                            rooms.get(roomName).getMaster().sendMessage(message);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    return;

                }
                int infoByInt = Integer.parseInt(message.getPayload());
                if (infoByInt < 0){

                    GameStatus toControl = rooms.get(roomName);

                    // control signal
                    switch (infoByInt) {
                        case START_SIGNAL:
                            // start
                            Room toStart = roomRepository.findById(roomName).get();

                            toStart.setRoomStatus("Playing");
                            roomRepository.save(toStart);

                            gameStart(roomName);
                            break;
                        case GUEST_READY_SIGNAL:
                            // guest ready
                            rooms.get(roomName).setGuestReady(true);
                            try {
                                rooms.get(roomName).getMaster().sendMessage(GUEST_READY_SIGNALL_MESSAGE);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                            break;
                        case GUEST_UNREADY_SIGNAL:
                            // guest unready
                            rooms.get(roomName).setGuestReady(false);
                            try {
                                rooms.get(roomName).getMaster().sendMessage(GUEST_UNREADY_SIGNAL_MESSAGE);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                            break;
                        case GUEST_LEAVE_SIGNAL:
                            // guest leave
                            rooms.get(roomName).setGuestReady(false);
                            rooms.get(roomName).setGuest(null);
                            rooms.get(roomName).setGuestName(null);
                            try {
                                rooms.get(roomName).getMaster().sendMessage(GUEST_LEAVE_SIGNAL_MESSAGE);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                            break;
                        case MASTER_DELETE_SIGNAL:
                            // master delete
                            try {
                                rooms.get(roomName).getMaster().sendMessage(MASTER_DELETE_SIGNAL_MESSAGE);
                                rooms.get(roomName).getGuest().sendMessage(MASTER_DELETE_SIGNAL_MESSAGE);
                                rooms.remove(roomName);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                            break;
                        case BLACK_STONE_SIGNAL:
                            try {
                                rooms.get(roomName).setStones(true);
                                rooms.get(roomName).getGuest().sendMessage(BLACK_STONE_SIGNAL_MESSAGE);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                            break;
                        case WHITE_STONE_SIGNAL:
                            try {
                                rooms.get(roomName).setStones(false);
                                rooms.get(roomName).getGuest().sendMessage(WHITE_STONE_SIGNAL_MESSAGE);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                            break;
                        default:
                            // TODO: send a certain step to the use
                            break;
                    }
                } else {
                    // moving signal
                    // check whether the stone fit the role
                    try{
                        int player = rooms.get(roomName).getStone(role);
                        // toSend store the info will be send to all players
                        // including winFlag
                        TextMessage toSend = rooms.get(roomName).move(player, infoByInt);

                        System.out.println("From GameSocketHandler: " + toSend.getPayload());

                        // send moving signal (with win flag) to all players
                        rooms.get(roomName).getGuest().sendMessage(toSend);
                        rooms.get(roomName).getMaster().sendMessage(toSend);
                        rooms.get(roomName).getAudience().forEach(s -> {
                            try {
                                s.sendMessage(toSend);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        });
                        if(rooms.get(roomName).getWinFlag() != 0){
                            System.out.println("save!");
                            matchRepository.save(rooms.get(roomName).summaryMatch());
                        }
                    } catch (Exception e){
                        System.out.println(e.getMessage());
                    }
                }

            }else{
                System.out.println("Invalid message.");
            }
        }else{
            System.out.println("Command cannot be processed.");
        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session){
        try{
            super.afterConnectionEstablished(session);
        } catch (Exception e){
            System.out.println(e.getMessage());
            return;
        }

        // get handshake info
        String role = session.getHandshakeHeaders().get("role").get(0);
        String roomName = session.getHandshakeHeaders().get("roomName").get(0);
        String userName = session.getHandshakeHeaders().get("userName").get(0);
        int masterStone = Integer.parseInt(session.getHandshakeHeaders().get("masterStone").get(0));

        if(role.equals("m")){

            // create a room and set master info, name and session
            // may throw invalid stone
            try {
                rooms.put(roomName, new GameStatus(masterStone, userName, session));
            } catch (Exception e){
                System.out.println(e.getMessage());
                return;
            }

            rooms.get(roomName).test();

            // start game
            // Important: now, sending start signal is the task of RoomSocketHandler
            // gameStart(roomName);

        }else if(role.equals("g")){
            while(!rooms.containsKey(roomName)){
                try{
                    Thread.sleep(200);
                } catch (Exception e){
                    System.out.println(e.getMessage());
                }
            }
            if(rooms.get(roomName).getGuest()==null){
                rooms.get(roomName).setGuestInfo(userName, session);
            }else{
                System.out.println("The room already has a guest.");
            }

            // testing info
            rooms.get(roomName).test();

            // start game
            // Important: now, sending start signal is the task of RoomSocketHandler
            // gameStart(roomName);

        }else if(role.equals("a")){
            if(!rooms.containsKey(roomName)){
                System.out.println("No room.");
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
        System.out.println("socket closed.");
        // System.out.println("closing: "+session.getHandshakeHeaders().get("role"));
        String userName = session.getHandshakeHeaders().get("userName").get(0);
        String role = session.getHandshakeHeaders().get("role").get(0);
        String roomName = session.getHandshakeHeaders().get("roomName").get(0);
        if(role.equals("m")){

            // now: ignore the game
            // TODO: judge winner and upload game info
            // TODO: send end signal
            Room toModify = roomRepository.findById(roomName).get();
            if (toModify != null){
                rooms.get(roomName).getGuest().sendMessage(END_SIGNAL_MESSAGE);
                rooms.get(roomName).getAudience().forEach(audienceSession -> {
                    try {
                        audienceSession.sendMessage(END_SIGNAL_MESSAGE);
                    } catch (Exception e){
                        System.out.println(e.getMessage());
                    }
                });

                rooms.remove(roomName);

                roomRepository.delete(toModify);
            }

        }else if(role.equals("g")){

            // now: ignore the game
            // TODO: judge winner and upload game info
            // TODO: send end signal
            //rooms.remove(roomName);
            Room toModify = roomRepository.findById(roomName).get();
            if (toModify != null) {
                if (toModify.getRoomStatus().equals("Playing")) {
                    rooms.get(roomName).getGuest().sendMessage(END_SIGNAL_MESSAGE);
                    rooms.get(roomName).getAudience().forEach(audienceSession -> {
                        try {
                            audienceSession.sendMessage(END_SIGNAL_MESSAGE);
                        } catch (Exception e) {
                            System.out.println(e.getMessage());
                        }
                    });
                    rooms.remove(roomName);

                    roomRepository.delete(toModify);
                } else {
                    rooms.get(roomName).setGuest(null);
                }
            }

        }else if(role.equals("a")){
            rooms.get(roomName).getAudience().remove(session);
        }

        // testing info
        rooms.keySet().forEach(ele->{System.out.println(ele);});

    }

    // to strt game after two players are ready
    // Important: now, sending start signal is the task of RoomSocketHandler
    private void gameStart(String roomName){
        if(rooms.get(roomName).ready()){

            // testing info
            System.out.println("Info: roomName: " + roomName + ", ready to start ......");
            try{

                rooms.get(roomName).getMaster().sendMessage(START_SIGNAL_MESSAGE);
                rooms.get(roomName).getGuest().sendMessage(START_SIGNAL_MESSAGE);

            } catch (Exception e){
                System.out.print(e.getMessage());
            }
        }
    }
}