package com.gomoku.server;

import com.gomoku.server.controller.AuthController;
import com.gomoku.server.controller.MatchController;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.RequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.nio.charset.Charset;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringRunner.class)
@ContextConfiguration(classes=ServerApplication.class)
@WebMvcTest(MatchController.class)
public class MatchControllerTests {

    public static final MediaType APPLICATION_JSON_UTF8 = new MediaType(MediaType.APPLICATION_JSON.getType(), MediaType.APPLICATION_JSON.getSubtype(), Charset.forName("utf8"));
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private MatchController matchController;

    @Test
    public void testInsertMatch() throws Exception {
        //String json = "{\"userName\": \"123\",\"pass\": \"123\"}";
        RequestBuilder requestBuilder = MockMvcRequestBuilders
                .post("/match")
                .accept(MediaType.APPLICATION_JSON)
                .content("{\"user1Id\": \"123\",\"user2Id\": \"Guest\",\"moves\": [[1,1],[2,2]],\"user1win\": 1}")
                .contentType(APPLICATION_JSON_UTF8);

        MvcResult result = mockMvc.perform(requestBuilder).andReturn();

        MockHttpServletResponse response = result.getResponse();
        Assert.assertEquals(200, response.getStatus());
    }

    @Test
    public void testSearch() throws Exception {
        //String json = "{\"userName\": \"123\",\"pass\": \"123\"}";

        RequestBuilder requestBuilder = MockMvcRequestBuilders
                .post("/match")
                .accept(MediaType.APPLICATION_JSON)
                .content("{\"user1Id\": \"123\",\"user2Id\": \"Guest\",\"moves\": [[1,1],[2,2]],\"user1win\": 1}")
                .contentType(APPLICATION_JSON_UTF8);

        MvcResult result = mockMvc.perform(requestBuilder).andReturn();

        MockHttpServletResponse response = result.getResponse();
        Assert.assertEquals(200, response.getStatus());
    }

}
