package com.gomoku.server.websocket.model;

import org.springframework.context.annotation.Bean;

import java.util.ArrayList;
import java.util.List;

public class GameLogic {

    final int SIZE = 15;
    final int FULL = 15*15;

    int stonesNum;
    int[][] board;
    boolean endFlag;
    int winFlag;
    List<Integer> moves;
    int round;

    public GameLogic() {
        board = new int[SIZE][SIZE];
        for(int i=0; i<SIZE; i++){
            for(int j=0; i<SIZE; i++){
                board[i][j] = 0;
            }
        }
        round = 1;
        endFlag = false;
        winFlag = 0;
        stonesNum = 0;
        moves = new ArrayList<>();
    }

    public boolean gameEnd(){
        return endFlag;
    }

    public int move(int player, int pos) throws Exception{

        // 0000 0000 # 0000 000[1-bit player] # [8-bit y] # [8-bit x]
        if(player != pos>>16)
            throw new Exception("Invalid position.");

        int x = pos & 255;
        int y = pos>>8 & 255;

        if(board[x][y] == 0){
            board[x][y] = player;
            stonesNum++;
            setWinFlag(x, y);
        }else{
            throw new Exception("Invalid move.");
        }
        return winFlag;
    }

    private void setWinFlag(int x, int y) throws Exception{
        int stone = board[x][y];
        if(stone==1 || stone==2){
            int l, r;
            int t, b;
            int lt, rb;
            int tb, rt;

            // TODO: game logic

            System.out.println("TODO !!!");
        }else{
            throw new Exception("Invalid stone.");
        }
    }

    public int getRound() {
        return round;
    }
}
