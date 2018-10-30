# Alpha Gomoku Game 

In this project, we plan to implement a Gomoku game software, which has two modes: game between two people and rivalry between Human and Artifactual Intelligence. The client and user interface will be implemented using Python and the server side will be implemented using Java. To develop further, some reinforcement learning algorithms will be applied in the application to enhance the wisdom of AI chess player. 

## Getting Start

### Prerequisites

Python 3.6 installed in client and Oracle JDK8 (java-8-oracle) with Maven installed in server.

### Installing

#### Python 3.6

To see which version of Python you have installed:
```
$ python --version
```
To install python3.6 on Ubuntu:
```
$ sudo apt-get update
$ sudo apt-get install python3.6
```

#### Oracle JDK 8

Oracle JDK 8 is the latest stable version of Java at time of writing. You can install it on Ubuntu using the following command:
```
$ sudo apt-get install oracle-java8-installer
```
You can verify your Java version:
```
$ javac -version
```
There can be multiple Java installations on one server. You can manage Java JDK version:
```
$ sudo update-alternatives --config java
```

##### Setting the JAVA_HOME Environment Variable:

Open .bashrc or /etc/profile to manage $PATH:
```
$ vi ~.bashrc
```
or
```
$ sudo vi /etc/profile
```
Add JAVA_HOME:
```
export JAVA_HOME="/usr/lib/jvm/java-8-oracle"
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVAHOME/lib/tools.jar
```
Make the changes in $PATH work:
```
$ source ~.bashrc
```
or
```
$ source /etc/profile
```

### Install Maven

Apache Maven is a software project management and comprehension tool. To install the latest Apache Maven:
```
$ sudo apt-get install maven
```

#### Setting MAVEN_HOME Environment Variable 

Open .bashrc or /etc/profile:
```
export MAVEN_HOME="/usr/share/maven"
export PATH=${PATH}:${MAVEN_HOME}/bin
```
To verify your installation:
```
$ mvn -version
```

## Running the tests

### Client:

Get to the client forder:
```
$ cd client/
```
Run Python program:
```
$ python ui.py
```
Enter the username, password and IPv4 of server, or sign up a new account.

### Server:

Get to the server forder and use Maven to compile and package Java program:
```
$ cd server/
$ mvn clean
$ mvn compile
$ mvn package
```
Run server:
```
java -jar <jarfilename>.jar
```

## Authors

* **Chengqi Dai (cd3046), Yiqian Wang (yw3225), Wenbo Song (ws2505), Zhongkai Sun (zs2341)**

## Acknowledgement
COMSW4156 - ADVANCED SOFTWARE ENGINEERING
* Prof. Gail Kaiser
* IA Siddharth P Ramakrishnan
				



