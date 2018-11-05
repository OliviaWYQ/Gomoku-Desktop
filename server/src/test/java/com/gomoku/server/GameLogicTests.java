package com.gomoku.server;

import com.gomoku.server.websocket.model.GameLogic;
import org.junit.Assert;
import org.junit.Test;


public class GameLogicTests {

    @Test
    public void gameLogicNoWinTest(){
        GameLogic gl = new GameLogic();
        int[] x = new int[5];
        for(int i=0; i<5; i++){
            x[i] = i;
        }
        int[] y = new int[5];
        for(int i=4; i>=0; i--){
            y[i] = i<<8;
        }
        try {
            Assert.assertEquals(0, gl.move(1, 1, 14, 14));
            Assert.assertEquals(0, gl.move(2, 2, 2, 2));
            Assert.assertEquals(0, gl.move(1, 1, 13, 13));
            Assert.assertEquals(0, gl.move(2, 2, 4, 2));
            Assert.assertEquals(0, gl.move(1, 1, 12, 12));
            Assert.assertEquals(0, gl.move(2, 2, 6, 2));
            Assert.assertEquals(0, gl.move(1, 1, 11, 11));
            Assert.assertEquals(0, gl.move(2, 2, 10, 10));
            Assert.assertEquals(0, gl.move(1, 1, 9, 9));
            Assert.assertEquals(0, gl.move(2, 2, 6, 5));
        }catch (Exception e){
            Assert.assertEquals(1,2);
        }
    }

    @Test
    public void gameLogicWinTest(){
        GameLogic gl = new GameLogic();
        int[] x = new int[5];
        for(int i=0; i<5; i++){
            x[i] = i;
        }
        int[] y = new int[5];
        for(int i=4; i>=0; i--){
            y[i] = i<<8;
        }
        try {
            Assert.assertEquals(0, gl.move(1, 1, 14, 14));
            Assert.assertEquals(0, gl.move(2, 2, 2, 2));
            Assert.assertEquals(0, gl.move(1, 1, 13, 13));
            Assert.assertEquals(0, gl.move(2, 2, 4, 2));
            Assert.assertEquals(0, gl.move(1, 1, 12, 12));
            Assert.assertEquals(0, gl.move(2, 2, 6, 2));
            Assert.assertEquals(0, gl.move(1, 1, 11, 11));
            Assert.assertEquals(0, gl.move(2, 2, 10, 9));
            Assert.assertEquals(1, gl.move(1, 1, 10, 10));
        }catch (Exception e){
            Assert.assertEquals(1,2);
        }
    }

    @Test
    public void InvalidPositionExceptionTest(){
        GameLogic gl = new GameLogic();
        int[] x = new int[5];
        for(int i=0; i<5; i++){
            x[i] = i;
        }
        int[] y = new int[5];
        for(int i=4; i>=0; i--){
            y[i] = i<<8;
        }
        try {
            Assert.assertEquals(0, gl.move(1, 1, 14, 14));
            Assert.assertEquals(0, gl.move(1, 2, 2, 2));
        }catch (Exception e){
            Assert.assertEquals(e.getMessage(),"Invalid position.");
        }
    }

    @Test
    public void InvalidMoveExceptionTest(){
        GameLogic gl = new GameLogic();
        int[] x = new int[5];
        for(int i=0; i<5; i++){
            x[i] = i;
        }
        int[] y = new int[5];
        for(int i=4; i>=0; i--){
            y[i] = i<<8;
        }
        try {
            Assert.assertEquals(0, gl.move(1, 1, 14, 14));
            Assert.assertEquals(0, gl.move(2, 2, 14, 14));
        }catch (Exception e){
            Assert.assertEquals(e.getMessage(),"Invalid move.");
        }
    }

}
