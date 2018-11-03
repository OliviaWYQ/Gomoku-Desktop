package com.gomoku.server.controller;

import com.gomoku.server.socket.model.Message;
import com.gomoku.server.socket.model.OutMessage;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import java.text.SimpleDateFormat;
import java.util.Date;

@Controller
public class GameController {
    @MessageMapping("/play/{gameid}")
    @SendTo("/gameinfo/{gameid}")
    public OutMessage send(final Message message, @DestinationVariable String gameid) throws Exception {
        System.out.println(gameid);
        return new OutMessage(message.getFrom(), message.getPosition(), 0);
    }
}
