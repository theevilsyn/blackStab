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
	data := strings.ReplaceAll(fmt.Sprintf("%-8v", field), " ", "\x00")
	return (data)
}

func _exit(conn net.Conn) {
	fmt.Println("See You Again")
	send(conn, "-337")
	conn.Close()
	os.Exit(1337)
}

func getresp(conn net.Conn) int {
	resp, err := strconv.Atoi(strings.ReplaceAll(recv(conn, 8), "\x00", ""))
	if err != nil {
		// fmt.Println("Error: ", err.Error())
		fmt.Println("Something Went Wrong, See you again!!")
		_exit(conn)
	}
	return resp
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
