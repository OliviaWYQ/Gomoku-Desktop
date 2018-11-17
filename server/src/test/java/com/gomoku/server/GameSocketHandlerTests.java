package com.gomoku.server;

import com.gomoku.server.controller.AuthController;
import com.gomoku.server.websocket.GameSocketHandler;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpHeaders;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.util.MultiValueMap;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.web.socket.*;
import org.springframework.web.socket.client.WebSocketClient;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutionException;
//import org.springframework.web.socket.client.jetty.JettyWebSocketClient;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes=ServerApplication.class)
@SpringBootTest(classes = {ServerApplication.class}, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class GameSocketHandlerTests {

    @Value("${local.server.port}")
    int port;

    private WebSocketClient wsc = new StandardWebSocketClient();

    @MockBean
    private GameSocketHandler gameSocketHandler;

    private WebSocketHandler testHandler = new WebSocketHandler() {

        @Override
        public void afterConnectionEstablished(WebSocketSession session) throws Exception {

        }

        @Override
        public void handleMessage(WebSocketSession session, WebSocketMessage<?> message) throws Exception {
            messageMemory = message.getPayload().toString();
            messageCounter++;
        }

        @Override
        public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {

        }

        @Override
        public void afterConnectionClosed(WebSocketSession session, CloseStatus closeStatus) throws Exception {

        }

        @Override
        public boolean supportsPartialMessages() {
            return false;
        }
    };

    private String messageMemory;

    private int messageCounter = 1;

    @Test
    public void testWebSocket() throws Exception {

        URI socketUri = new URI("ws://localhost:"+port+"/playing");

        HttpHeaders masterHeader = new HttpHeaders();
        masterHeader.add("role", "m");
        masterHeader.add("roomName", "123#456");
        masterHeader.add("userName", "123");
        masterHeader.add("masterStone", "1");

        WebSocketSession masterSession = wsc.doHandshake(testHandler, new WebSocketHttpHeaders(masterHeader), socketUri).get();

        HttpHeaders guestHeader = new HttpHeaders();
        guestHeader.add("role", "g");
        guestHeader.add("roomName", "123#456");
        guestHeader.add("userName", "456");
        guestHeader.add("masterStone", "1");

        WebSocketSession guestSession = wsc.doHandshake(testHandler, new WebSocketHttpHeaders(guestHeader), socketUri).get();

        Assert.assertEquals(masterHeader, masterSession.getHandshakeHeaders());
        Assert.assertEquals(guestHeader, guestSession.getHandshakeHeaders());

        guestSession.sendMessage(new TextMessage("-2"));
        Thread.sleep(100);
        masterSession.sendMessage(new TextMessage("-1"));
        Thread.sleep(100);
        masterSession.sendMessage(new TextMessage(new byte[]{'2','5','6'}));
        Thread.sleep(100);
        Assert.assertEquals("256", messageMemory);
        guestSession.sendMessage(new TextMessage(new byte[]{'5','2','9'}));
        Thread.sleep(100);
        Assert.assertEquals("529", messageMemory);
        masterSession.sendMessage(new TextMessage(new byte[]{'1','2','8','1'}));
        Thread.sleep(100);
        Assert.assertEquals("1281", messageMemory);
        guestSession.sendMessage(new TextMessage(new byte[]{'1','5','7','0'}));
        Thread.sleep(100);
        Assert.assertEquals("1570", messageMemory);
        masterSession.sendMessage(new TextMessage(new byte[]{'2','3','0','6'}));
        Thread.sleep(100);
        Assert.assertEquals("2306", messageMemory);
        guestSession.sendMessage(new TextMessage(new byte[]{'2','6','2','8'}));
        Thread.sleep(100);
        Assert.assertEquals("2628", messageMemory);
        masterSession.sendMessage(new TextMessage(new byte[]{'3','3','3','1'}));
        Thread.sleep(100);
        Assert.assertEquals("3331", messageMemory);
        guestSession.sendMessage(new TextMessage(new byte[]{'3','7','2','0'}));
        Thread.sleep(100);
        Assert.assertEquals("3720", messageMemory);
        masterSession.sendMessage(new TextMessage(new byte[]{'4','3','5','6'}));
        Thread.sleep(100);
        Assert.assertEquals("266500", messageMemory);
        Thread.sleep(500);
        Assert.assertEquals(11, messageCounter/2);

        guestSession.close();
        masterSession.close();

    }

}
