package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
)

func createvm(conn net.Conn) {
	var vmname string
	var vmtag string
	var image int
	var winchoice int
	funcname := "createVM"
	fmt.Print("Enter Vm Name: ")
	fmt.Scan(&vmname)
	fmt.Print("Enter VM Tag: ")
	fmt.Scan(&vmtag)
	fmt.Print("Please Select the Operating System for your VM\n\tAvailable Options:\n\t\t0: Archlinux\n\t\t1: Ubuntu 16.04\n\t\t2: Ubuntu 18.04\n\t\t3: CentOS 7\n\t\t4: Oracle Linux 6\n\t\t5: OpenSUSE by SUSE\n\t\t6: Windows Server 2019 LTSC\n")
	fmt.Scan(&image)
	if image > 6 {
		fmt.Println("Please select a valid operating system next time")
		menu(conn)
	} else if image == 6 {
		fmt.Println("This is to inform you that you are about to waste $150 cloud credits on --windows VM-- ")
		fmt.Print("\n\t1. Continue\n\t2. Use your mind.\n")
		fmt.Scan(&winchoice)
		switch winchoice {

		case 1:
			fmt.Println("No one can change You!!¯\\_(ツ)_/¯")
		case 2:
			fmt.Println("Good Choice!! f4lc0n appreciates you :P")
			menu(conn)
		default:
			fmt.Println("I'll take that as a yes, good choice")
			menu(conn)
		}

	}
	sender := padint(0) + padint(len(funcname)) + funcname + padint(len(vmname)) + vmname + padint(len(vmtag)) + vmtag + padint(image)
	fmt.Println(sender)
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println("Successfully created the VM")
	} else if resp == 1 {
		fmt.Println("VM with the requested tag is already present")
		menu(conn)
	} else if resp == 2 {
		fmt.Println("Funds not sufficient to spawn a VM")
		menu(conn)
	} else {
		fmt.Println("Something went wrong")
		_exit(conn)
	}

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
	resp := getresp(conn)
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
	resp, err := strconv.Atoi(strings.ReplaceAll(recv(conn, 8), "\x00", ""))
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
