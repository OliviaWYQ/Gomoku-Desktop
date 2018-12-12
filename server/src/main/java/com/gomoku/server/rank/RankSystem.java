package com.gomoku.server.rank;

import com.gomoku.server.mongo.model.User;
import com.gomoku.server.mongo.repository.UserRepository;
import com.gomoku.server.redis.repository.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RankSystem {
    @Autowired
    UserRepository userRepository;

    public void updateInfo(String masterName, String guestName, int masterStone, int winFlag){
        User master = userRepository.findOneByUserName(masterName);
        User guest = userRepository.findOneByUserName(guestName);

        master.oneMoreMatch();
        guest.oneMoreMatch();

        if(winFlag != 3){
            int masterScore = master.getRankScore();
            int guestScore = guest.getRankScore();
            int gap;
            if (masterScore >= guestScore) {
                gap = getScore(masterScore, guestScore, masterStone==winFlag);
            } else {
                gap = getScore(guestScore, masterScore, masterStone!=winFlag);
            }
            if (masterStone == winFlag) {
                master.oneMoreWinMatch();
                master.setRankScore(masterScore + gap);
                guest.setRankScore(guestScore - gap);
            } else {
                guest.oneMoreWinMatch();
                master.setRankScore(masterScore - gap);
                guest.setRankScore(guestScore + gap);
            }
        }

        master.updateWinRate();
        guest.updateWinRate();

        userRepository.save(master);
        userRepository.save(guest);

    }

    private int getScore(int bigger, int smaller, boolean biggerWin){
        int gap = bigger - smaller;
        int score;
        if (! biggerWin){
            if (gap < 100) {
                score = 1 + gap / 10;
            } else if (gap<500) {
                score = 6 + gap / 20;
            } else if (gap<1000) {
                score = 36 + gap / 50;
            } else {
                score = 50;
            }
        } else {
            if (gap < 100) {
                score = 1 + gap / 10;
            } else if (gap < 200) {
                score = 11;
            } else if (gap < 500) {
                score = 14 - gap / 60;
            } else if (gap < 1000) {
                score = 11 - gap / 100;
            } else {
                return 1;
            }
        }

        return score;
    }
}
