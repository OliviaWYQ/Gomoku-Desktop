package com.gomoku.server.websocket;

import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.CopyOnWriteArraySet;

@Component
public class WebsocketHandler extends TextWebSocketHandler {

    //List<WebSocketSession> sessions = new CopyOnWriteArrayList();CopyOnWriteArraySet

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message)
            throws InterruptedException, IOException {

        //for(WebSocketSession webSocketSession : sessions) {
            //Map value = new Gson().fromJson(message.getPayload(), Map.class);
            for(int i=0; i<4; i++)
                session.sendMessage(new TextMessage("Hello!" + i));
            session.sendMessage(new TextMessage("end"));
        //}
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        super.afterConnectionEstablished(session);
    }
//        public void afterConnectionEstablished(WebSocketSession session) throws Exception {
//            //the messages will be broadcasted to all users.
//            //sessions.add(session);
//        }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        super.afterConnectionClosed(session, status);
    }
}