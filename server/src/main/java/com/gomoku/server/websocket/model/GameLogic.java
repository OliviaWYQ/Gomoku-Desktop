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

    // step no for 2 players
    // {player==1, player==2}
    int[] step = {0, 0};

    // TODO: control flag and control signals
    // if the message is negative, the message is a control signal
    // (we use the symbol bit to present the control flag)
    // or, it is a position message
    final int X_OFFSET = 0;
    final int X_LENGTH = 4;
    final int X_MASK = 0b1111;

    final int Y_OFFSET = X_OFFSET + X_LENGTH;
    final int Y_LENGTH = 4;
    final int Y_MASK = 0b1111;

    // player could be 1 or 2
    final int PLAYER_FLAG_OFFSET = Y_OFFSET + Y_LENGTH;
    final int PLAYER_FLAG_LENGTH = 2;
    final int PLAYER_FLAG_MASK = 0b11;


    final int STEP_NO_OFFSET = PLAYER_FLAG_OFFSET + PLAYER_FLAG_LENGTH;
    final int STEP_NO_LENGTH = 8;
    final int STEP_NO_MASK = 0b1111_1111;

    final int WIN_FLAG_OFFSET = STEP_NO_OFFSET + STEP_NO_LENGTH;
    final int WIN_FLAG_LENGTH = 3;
    final int WIN_FLAG_MASK = 0b11;

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

    public int move(int player, int pos) throws Exception {

        if (player != next || player != ((pos >> PLAYER_FLAG_OFFSET) & PLAYER_FLAG_MASK)) {
            throw new Exception("Wrong stone.");
        } else if(((pos >> STEP_NO_OFFSET) & STEP_NO_MASK) != step[player - 1]) {
            throw new Exception("Wrong step #.");
        }

        int x = pos & X_MASK;
        int y = (pos >> Y_OFFSET) & Y_MASK;

        if (board[x][y] == 0){
            board[x][y] = player;
            step[player - 1]++;

            next = next == 1 ? 2 : 1;

            stonesNum++;
            setWinFlag(x, y);
        } else {
            throw new Exception("Invalid move.");
        }

        // test
        System.out.println("win flag: " + winFlag);
        return pos + (winFlag << WIN_FLAG_OFFSET);
    }

    // Judge win or not
    private void setWinFlag(int x, int y) throws Exception{
        int stone = board[x][y];
        if (stone == 1 || stone == 2){
            int l = 0, r = 0;
            int t = 0, b = 0;
            int lt = 0, rb = 0;
            int lb = 0, rt = 0;

            // game logic
            // System.out.println("TODO !!!");
            // xxxxx
            for(int i = 1; i <= x && i <= 4; i++){
                if (board[x-i][y] == stone){
                    l++;
                } else {
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


    // Test cases
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

            System.out.println(gl.move(1, 0b00000000_01_0000_0000));
            System.out.println(gl.move(2, 0b00000000_10_0001_0001));

            System.out.println(gl.move(1, 0b00000001_01_0000_0001));
            System.out.println(gl.move(2, 0b00000001_10_0010_0010));

            System.out.println(gl.move(1, 0b00000010_01_0000_0010));
            System.out.println(gl.move(2, 0b00000010_10_0100_0100));

            System.out.println(gl.move(1, 0b00000011_01_0000_0011));
            System.out.println(gl.move(2, 0b00000011_10_1000_1000));

            System.out.println(gl.move(1, 0b00000100_01_0000_0100));
            System.out.println(gl.move(2, 0b00000100_10_1100_1100));

        }catch (Exception e){
            System.out.println(e);
        }

        System.out.println((1<<31)-0b1000_0000_0000_0000_0000_0000_0000_0000);
    }
}
