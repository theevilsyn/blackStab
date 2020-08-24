package main

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"reflect"
	"strconv"
	"strings"
	"unsafe"
)

func BytesToString(b []byte) string {
	bh := (*reflect.SliceHeader)(unsafe.Pointer(&b))
	sh := reflect.StringHeader{bh.Data, bh.Len}
	return *(*string)(unsafe.Pointer(&sh))
}

// take an int and pad it with '\x00's
func padint(field int) string {
	data := strings.ReplaceAll(fmt.Sprintf("%-8v", field), " ", "\x00")
	return (data)
}

func clrscr() {
	cmd := exec.Command("clear")
	cmd.Stdout = os.Stdout
	cmd.Run()
}

func _exit(conn net.Conn) {
	fmt.Println("See You Again")
	send(conn, "-337")
	conn.Close()
	os.Exit(5)
}

func getresp(conn net.Conn) int {
	resp, err := strconv.Atoi(strings.ReplaceAll(recv(conn, 8), "\x00", ""))
	if err != nil {
		// fmt.Println("Error: ", err.Error())
		fmt.Println("Something Went Wrong, See you again!!")
		send(conn, "-337")
		conn.Close()
		os.Exit(5)
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
