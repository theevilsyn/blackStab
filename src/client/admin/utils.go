package main

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
)

// take an int and pad it with '\x00's
func padint(field int) string {
	data := strings.ReplaceAll(fmt.Sprintf("%-8v", field), " ", "\x00")
	return (data)
}

func isBase64(str string) bool {
	var Base64 string
	Base64 = "^(?:[A-Za-z0-9+\\/]{4})*(?:[A-Za-z0-9+\\/]{2}==|[A-Za-z0-9+\\/]{3}=|[A-Za-z0-9+\\/]{4})$"
	rx := regexp.MustCompile(Base64)
	return rx.MatchString(str)
}

func isEmail(str string) bool {
	var email string
	email = "^(((([a-zA-Z]|\\d|[!#\\$%&'\\*\\+\\-\\/=\\?\\^_`{\\|}~]|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])+(\\.([a-zA-Z]|\\d|[!#\\$%&'\\*\\+\\-\\/=\\?\\^_`{\\|}~]|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])+)*)|((\\x22)((((\\x20|\\x09)*(\\x0d\\x0a))?(\\x20|\\x09)+)?(([\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x7f]|\\x21|[\\x23-\\x5b]|[\\x5d-\\x7e]|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])|(\\([\\x01-\\x09\\x0b\\x0c\\x0d-\\x7f]|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}]))))*(((\\x20|\\x09)*(\\x0d\\x0a))?(\\x20|\\x09)+)?(\\x22)))@((([a-zA-Z]|\\d|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])|(([a-zA-Z]|\\d|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])([a-zA-Z]|\\d|-|\\.|_|~|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])*([a-zA-Z]|\\d|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])))\\.)+(([a-zA-Z]|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])|(([a-zA-Z]|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])([a-zA-Z]|\\d|-|\\.|_|~|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])*([a-zA-Z]|[\\x{00A0}-\\x{D7FF}\\x{F900}-\\x{FDCF}\\x{FDF0}-\\x{FFEF}])))\\.?$"
	rx := regexp.MustCompile(email)
	return rx.MatchString(str)
}

func isAlphaNumeric(str string) bool {
	var alphan string
	alphan = "^[a-zA-Z0-9]+$"
	rx := regexp.MustCompile(alphan)
	return rx.MatchString(str)
}

func clrscr() {
	cmd := exec.Command("clear")
	cmd.Stdout = os.Stdout
	cmd.Run()
}

func _exit(conn net.Conn) {
	fmt.Println("See You Again ;-;")
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
		fmt.Println("Something Went wrong")
		conn.Close()
		os.Exit(-1)
	}
	data := string(buf[:len])
	return data
}
