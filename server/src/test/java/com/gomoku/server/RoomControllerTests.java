package com.gomoku.server;

import com.gomoku.server.controller.AuthController;
import com.gomoku.server.controller.RoomController;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.RequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.nio.charset.Charset;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes=ServerApplication.class)
@WebMvcTest(RoomController.class)
public class RoomControllerTests {

    public static final MediaType APPLICATION_JSON_UTF8 = new MediaType(MediaType.APPLICATION_JSON.getType(), MediaType.APPLICATION_JSON.getSubtype(), Charset.forName("utf8"));
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private RoomController roomController;

    @Test
    public void testCreate() throws Exception {
        String json = "{\"roomName\": \"123-456\"}";

        RequestBuilder requestBuilder = MockMvcRequestBuilders
                .post("/room")
                .accept(MediaType.APPLICATION_JSON).content(json)
                .contentType(APPLICATION_JSON_UTF8);

        MvcResult result = mockMvc.perform(requestBuilder).andReturn();

        MockHttpServletResponse response = result.getResponse();
        Assert.assertEquals(200, response.getStatus());
    }

    @Test
    public void testJoin() throws Exception {

        RequestBuilder requestBuilder = MockMvcRequestBuilders
                .get("/room/join/123-456/789");

        MvcResult result = mockMvc.perform(requestBuilder).andReturn();

        MockHttpServletResponse response = result.getResponse();
        Assert.assertEquals(200, response.getStatus());
    }

    @Test
    public void testSearchAll() throws Exception {

        RequestBuilder requestBuilder = MockMvcRequestBuilders
                .get("/room/all");

        MvcResult result = mockMvc.perform(requestBuilder).andReturn();

        MockHttpServletResponse response = result.getResponse();
        Assert.assertEquals(200, response.getStatus());
    }

    @Test
    public void testSearchByRoomName() throws Exception {

        RequestBuilder requestBuilder = MockMvcRequestBuilders
                .get("/room/123-456");

        MvcResult result = mockMvc.perform(requestBuilder).andReturn();

        MockHttpServletResponse response = result.getResponse();
        Assert.assertEquals(200, response.getStatus());
    }

}