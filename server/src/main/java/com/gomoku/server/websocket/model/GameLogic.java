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

    int next;

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

        next = 1;
    }

    public boolean gameEnd(){
        return endFlag;
    }

    public int move(int player, int pos) throws Exception{

        // 0000 0000 # 0000 000[1-bit player] # [8-bit y] # [8-bit x]
        if(player != next || player != pos>>16)
            throw new Exception("Wrong stone.");

        int x = pos & 255;
        int y = pos>>8 & 255;

        if(board[x][y] == 0){
            board[x][y] = player;

            next = next==1?2:1;

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
            int l = 0, r = 0;
            int t = 0, b = 0;
            int lt = 0, rb = 0;
            int lb = 0, rt = 0;

            // TODO: game logic
            //System.out.println("TODO !!!");
            //xxxxx
            for(int i=1; i<=x&&i<=4; i++){
                if(board[x-i][y] == stone){
                    l++;
                }else{
                    break;
                }
            }
            for(int i=1; i<SIZE-x&&i<=4; i++){
                if(board[x+i][y] == stone){
                    r++;
                }else{
                    break;
                }
            }
            if(l+r>=4) {
                winFlag = stone;
                return;
            }
            // x
            // x
            // x
            // x
            // x
            for(int i=1; i<=y&&i<=4; i++){
                if(board[x][y-i] == stone){
                    b++;
                }else{
                    break;
                }
            }
            for(int i=1; i<SIZE-y&&i<=4; i++){
                if(board[x][y+i] == stone){
                    t++;
                }else{
                    break;
                }
            }
            if(b+t>=4) {
                winFlag = stone;
                return;
            }
            // x
            //   x
            //     x
            //       x
            //         x
            for(int i=1; i<=Math.min(x, y)&&i<=4; i++){
                if(board[x-i][y-i] == stone){
                    lt++;
                }else{
                    break;
                }
            }
            for(int i=1; i<SIZE-Math.max(x, y)&&i<=4; i++){
                if(board[x+i][y+i] == stone){
                    rb++;
                }else{
                    break;
                }
            }
            if(lt+rb>=4) {
                winFlag = stone;
                return;
            }
            //         x
            //       x
            //     x
            //   x
            // x
            for(int i=1; i<=Math.min(y, SIZE-x-1)&&i<=4; i++){
                if(board[x+i][y-i] == stone){
                    rt++;
                }else{
                    break;
                }
            }
            for(int i=1; i<=Math.min(x, SIZE-y-1)&&i<=4; i++){
                if(board[x-i][y+i] == stone){
                    lb++;
                }else{
                    break;
                }
            }
            if(lb+rt>=4) {
                winFlag = stone;
                return;
            }

            if(stonesNum == FULL)
                winFlag = 3;

        }else{
            throw new Exception("Invalid stone.");
        }
    }

    public int getRound() {
        return round;
    }

    public int move(int player, int p, int x, int y) throws Exception{

        // 0000 0000 # 0000 000[1-bit player] # [8-bit y] # [8-bit x]
        if(player != next || player != p)
            throw new Exception("Invalid position.");

        //int x = pos & 255;
        //int y = pos>>8 & 255;

        if(board[x][y] == 0){
            board[x][y] = player;
            next = next==1?2:1;
            stonesNum++;
            setWinFlag(x, y);
        }else{
            throw new Exception("Invalid move.");
        }
        return winFlag;
    }

    public static void main(String[] args){
        GameLogic gl = new GameLogic();
        try{
            int[] x = new int[5];
            for(int i=0; i<5; i++){
                x[i] = i;
            }
            int[] y = new int[5];
            for(int i=4; i>=0; i--){
                y[i] = i<<8;
            }

            System.out.println(gl.move(1, 1, 14, 14));System.out.println(gl.move(2, 2, 2, 2));
            System.out.println(gl.move(1, 1, 13, 13));System.out.println(gl.move(2, 2, 4, 2));
            System.out.println(gl.move(1, 1, 12, 12));System.out.println(gl.move(2, 2, 6, 2));
            System.out.println(gl.move(1, 1, 11, 11));System.out.println(gl.move(2, 2, 10, 10));
            System.out.println(gl.move(1, 1, 9, 9));System.out.println(gl.move(2, 2, 6, 5));

        }catch (Exception e){
            System.out.println(e);
        }
    }
}
