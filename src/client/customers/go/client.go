package main

import (
	"flag"
	"fmt"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"

	"github.com/common-nighthawk/go-figure"
)

func start(mode int, banner bool, ip string, port int) { // mode 1 register 2 login 3 userselect
	var choice int
	conn, err := net.Dial("tcp", ip+":"+strconv.Itoa(port))
	if err != nil {
		fmt.Println(err.Error())
		if strings.Contains(err.Error(), "refused") {
			fmt.Println("Host not up")
			os.Exit(1)
		}
	}
	if banner {
		fig := figure.NewColorFigure("Connecting to blackStab...", "pepper", "red", true)
		fig.Scroll(rand.Intn(6000-1000)+1000, 150, "right") // random 1~5 seconds waitime

	}
	auth(conn)
	mainfig := figure.NewColorFigure("Welcome to blackStab Cloud", "smslant", "red", true)
	mainfig.Print()
	// fmt.Println()
	if mode == 1 {
		register(conn)
	} else if mode == 2 {
		login(conn)
	} else {
		fmt.Print(1, " Register\n", 2, " Login\n")
		fmt.Scan(&choice)
		if choice == 1 {
			register(conn)
		} else {
			login(conn)
		}
	}
}

func menu(conn net.Conn, op string) {
	var choice int
	// clrscr()
	if op != "" {
		clrscr()
		mainfig := figure.NewColorFigure("blackStab Cloud Services", "smslant", "red", true)
		mainfig.Print()
		fmt.Println()
		fmt.Println("Response from the server:")
		fmt.Print(op + "\n\n")
	} else {
		clrscr()
		mainfig := figure.NewColorFigure("blackStab Cloud Services", "smslant", "red", true)
		mainfig.Print()
		fmt.Println()
	}
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
		menu(conn, "")
	}
}

func main() {

	var register bool
	var login bool /// handle both
	var rapid bool
	var ip string
	var port int
	flag.BoolVar(&register, "register", false, "Register a new user for blackStab cloud services")
	flag.BoolVar(&login, "login", false, "Login to the blackStab cloud services")
	flag.BoolVar(&rapid, "rapid-connect", false, "Use this to connect to the blackStab cloud instantly")
	flag.StringVar(&ip, "ip", "", "Address of blackStab server")
	flag.IntVar(&port, "port", 0, "the port of the service")
	flag.Parse()
	if register && login {
		// fmt.Print("Invalid options selected.\nLook at the help page for more info")
		mainfig := figure.NewColorFigure("blackStab Cloud Services", "smslant", "red", true)
		mainfig.Print()
		fmt.Print("\n\n")
		fmt.Fprintf(os.Stderr, "Usage of %s:\n", os.Args[0])
		flag.PrintDefaults()
	} else if register && port > 0 && ip != "" {
		start(1, !rapid, ip, port)
	} else if login && port > 0 && ip != "" {
		start(2, !rapid, ip, port)
	} else if !login && !register && port > 0 && ip != "" {
		start(3, !rapid, ip, port)
		// fmt.Print("Enter ")
	} else {
		mainfig := figure.NewColorFigure("blackStab Cloud Services", "smslant", "red", true)
		mainfig.Print()
		fmt.Print("\n\n")
		fmt.Fprintf(os.Stderr, "Usage of %s:\n", os.Args[0])
		flag.PrintDefaults()
	}
	// 	var test = []byte(`
	// Line1
	// Line1
	// line2         Line2
	// Line33
	// 	`)
	// 	fmt.Println(BytesToString(test))
}
