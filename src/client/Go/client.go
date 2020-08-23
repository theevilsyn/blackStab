package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

// take an int and pad it with '\x00's
func padint(field int) string {
	dataa := strings.ReplaceAll(fmt.Sprintf("%-8v", field), " ", "\x00")
	return (dataa)
}

func _exit(conn net.Conn) {
	fmt.Println("See You Again")
	send(conn, "-337")
	conn.Close()
	os.Exit(1337)
}

func send(conn net.Conn, data string) {
	conn.Write([]byte(data))
}

func recv(conn net.Conn, len int) string {
	buf := make([]byte, len)
	len, err := conn.Read(buf)
	if err != nil {
		fmt.Println("Error: ", err.Error())
	}
	data := string(buf[:len])
	return data
}

func register(conn net.Conn) {
	var email string
	var username string
	var password string
	fmt.Print("Enter Email: ")
	fmt.Scan(&email)
	fmt.Print("Enter Username: ")
	fmt.Scan(&username)
	fmt.Print("Enter Password: ")
	fmt.Scan(&password)
	sender := padint(1) + padint(len(email)) + email + padint(len(username)) + username + padint(len(password)) + password
	send(conn, sender)
	resp, err := strconv.Atoi(recv(conn, 8))
	if err != nil {
		fmt.Println("Error: ", err.Error())
	}
	if resp == 0 {
		print("Registration Successful")
	} else if resp == 1 {
		fmt.Println("Email Already Taken")
		_exit(conn)
	} else if resp == 2 {
		fmt.Println("Password is not greater than 12 :/")
		_exit(conn)
	} else {
		print("Something Went Wrong")
		_exit(conn)
	}
}

func login(conn net.Conn) {
	var email string
	var password string
	fmt.Print("Enter Email: ")
	fmt.Scan(&email)
	fmt.Print("Enter Password: ")
	fmt.Scan(&password)
	sender := padint(2) + padint(len(email)) + email + padint(len(password)) + password
	send(conn, sender)
	resp, err := strconv.Atoi(recv(conn, 8))
	if err != nil {
		fmt.Println("Error: ", err.Error())
	}
	if resp == 0 {
		print("Successfully Logged In")
		// menu(conn)
	} else if resp == 1 {
		fmt.Println("User Not Found")
		_exit(conn)
	} else if resp == 2 {
		fmt.Println("Password Incorrect")
		_exit(conn)
	} else {
		print("Something Went Wrong")
		_exit(conn)
	}

}

func start(conn net.Conn) {
	var choice int
	fmt.Print(1, " Register\n", 2, " Login\n")
	fmt.Scan(&choice)
	if choice == 1 {
		fmt.Println("You chose to register")
		register(conn)
	} else {
		fmt.Println("You chose to login")
	}
}

func main() {

	// connect to this socket
	conn, _ := net.Dial("tcp", "127.0.0.1:11111")
	start(conn)
	// conn.Write([]byte(makefield(11)))
	// fmt.Print(s)
	// time.Sleep(5 * time.Second)
}
