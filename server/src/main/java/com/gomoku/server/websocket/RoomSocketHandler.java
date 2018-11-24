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

    private WebSocketSession ws;

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message){
        System.out.println(message.getPayload());
        try {
            System.out.println("sent!");
            this.ws.sendMessage(new TextMessage(message.getPayload()+" from server"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        super.afterConnectionEstablished(session);
        this.ws = session;

    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        super.afterConnectionClosed(session, status);
        this.ws = null;
    }



}
