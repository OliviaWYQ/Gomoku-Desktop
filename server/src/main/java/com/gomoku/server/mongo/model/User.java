package com.gomoku.server.mongo.model;

import org.mindrot.jbcrypt.BCrypt;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "user")
public class User{

    private String userName;
    private String pass;

    public String getUserName() {
        return userName;
    }

    public String getPass() {
        return pass;
    }

    public void encodePass(){
        pass = BCrypt.hashpw(this.pass, BCrypt.gensalt());
    }

    public boolean checkPass(String rawPass){
        return BCrypt.checkpw(rawPass, this.pass);
    }

}

