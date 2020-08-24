package main

import (
	"fmt"
	"math/rand"
	"net"
	"os"
	"strings"

	"github.com/common-nighthawk/go-figure"
)

func start(conn net.Conn) {
	fig := figure.NewColorFigure("Connecting to blackStab...", "pepper", "red", true)
	fig.Scroll(rand.Intn(3000-1000)+1000, 500, "right") // random 1~5 seconds waitime
	auth(conn)
	fig = figure.NewColorFigure("Welcome to blackStab Cloud", "smslant", "red", true)
	fig.Print()
	fmt.Println()
	var choice int
	fmt.Print(1, " Register\n", 2, " Login\n")
	fmt.Scan(&choice)
	if choice == 1 {
		register(conn)
	} else {
		login(conn)
	}
}

func menu(conn net.Conn) {
	var choice int
	fmt.Print(1, " Create VM\n", 2, " Modify an existing VM\n", 3, " Delete an existing VM\n", 4, " Print status of an existing VM\n", 5, " List all the VMs associated with this account\n", 6, " View the status of your free subscription\n", 7, " Remove your account and terminate all the VMs associated with this account\n", 8, " Exit the client\n")
	fmt.Scan(&choice)
	switch choice {
	case 1:
		createvm(conn)
	case 2:
		modifyvm(conn)
	case 3:
		deletevm(conn)
	case 4:
		vmstatus(conn)
	case 5:
		listmyvms(conn)
	case 6:
		viewsubscription(conn)
	case 7:
		deleteacc(conn)
	case 8:
		_exit(conn)
	default:
		menu(conn)
	}
}

func main() {

	// connect to this socket
	conn, err := net.Dial("tcp", "192.168.123.219:9999")
	if err != nil {
		fmt.Println(err.Error())
		if strings.Contains(err.Error(), "refused") {
			fmt.Println("Host not up")
			os.Exit(1)
		}
	}
	start(conn)
}
