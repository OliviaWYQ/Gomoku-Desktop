package com.gomoku.server.redis.repository;

import com.gomoku.server.redis.model.Room;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RoomRepository extends CrudRepository<Room, String> {
//    void save(Room room);
//    List<Room> findAll();
//    Room findById(String id);
//    void update(Room room);
//    void delete(String id);
    Iterable<Room> findAll();
    Room save(Room room);
    //Room findById(String userName);
}
