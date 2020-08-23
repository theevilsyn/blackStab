package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
)

func deleteacc(conn net.Conn) {
	var password string
	sender := padint(0)
	sender += padint(len("deleteAccount"))
	sender += "deleteAccount"
	fmt.Print("For security reasons, please enter your password: ")
	fmt.Scan(&password)
	sender += padint(len(password))
	sender += password
	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {

	}
}

func viewsubscription(conn net.Conn) {
	sender := padint(0)
	sender += padint(len("viewSubscription"))
	sender += "viewSubscription"
	send(conn, sender)
	credits := getresp(conn)
	fmt.Println("You have ", credits, " $ worth credits left in your free subscription")
	menu(conn)
}

func listmyvms(conn net.Conn) {
	sender := padint(0)
	sender += padint(len("listallmyVMs"))
	sender += "listallmyVMs"
	send(conn, sender)
	count := getresp(conn)
	if count == 0 {
		fmt.Println("You have 0 VMs associated to your account")
		menu(conn)
	} else {
		list := recv(conn, count)
		fmt.Print(list)
	}
}

func vmstatus(conn net.Conn) {
	var vmtag string
	sender := padint(0)
	sender += padint(len("statusofmyVM"))
	sender += "statusofmyVM"
	fmt.Print("Enter VM Tag")
	fmt.Scan(&vmtag)
	sender += padint(len(vmtag))
	sender += vmtag
	send(conn, sender)
	statuslen := getresp(conn)
	status := recv(conn, statuslen)
	fmt.Print(status)
	menu(conn)
}

func deletevm(conn net.Conn) {
	var vmtag string
	sender := padint(0)
	sender += padint(len("deleteVM"))
	sender += "deleteVM"
	fmt.Print("Enter VM Tag: ")
	fmt.Scan(&vmtag)
	sender += padint(len(vmtag))
	sender += vmtag
	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println("Successfully deleted the VM")
		menu(conn)
	} else if resp == 1 {
		fmt.Println("Action failed, the VM with requested tag not found.")
		menu(conn)
	}
}

func modifyvm(conn net.Conn) {
	var port int
	var proto int
	var modify int
	var quantity int
	var resource int
	var operation int // 0:1 -> open:close | 0:1 -> upscale:downscale
	var vmtag string
	var action string
	sender := padint(0)
	fmt.Print("Enter the VM tag: ")
	fmt.Scan(&vmtag)
	fmt.Print("1. Edit Firewall Rules\n2. Scale an existing VM\n")
	fmt.Scan(&modify)
	if modify == 1 {
		fmt.Print("1. Open/Close a TCP Port\n2. Open/Close a UDP Port\n")
		fmt.Scan(&proto)
		if proto == 1 {
			sender += padint(len("ruleAddTCP"))
			sender += "ruleAddTCP"
			sender += padint(len(vmtag))
			sender += vmtag
			fmt.Print("1. Open a TCP Port\n2. Close a TCP Port\n")
			fmt.Scan(&port)
			if port > 65535 {
				fmt.Println("Please select a proper port next time. No scope for overflow here :P")
				menu(conn)
			}
			sender += padint(port)
			fmt.Print("1. Open TCP Port ", port, "\n2. Close TCP Port ", port, "\n")
			fmt.Scan(&operation)
			if operation == 1 {
				action = "open"
			} else if operation == 2 {
				action = "clos"
			} else {
				fmt.Println("Please choose a proper port next time.")
				menu(conn)
			}
			sender += padint(operation)
			send(conn, sender)
			resp := getresp(conn)
			if resp == 0 {
				fmt.Println("Successfully ", action, "ed the TCP Port ", port)
				menu(conn)
			} else if resp == 1 {
				fmt.Println("TCP Port ", port, "already ", action, "ed")
				menu(conn)
			} else if resp == 2 {
				fmt.Println("VM with the requested tag not found")
				menu(conn)
			} else {
				fmt.Println("Something went wrong")
				_exit(conn)
			}
		} else if proto == 2 {
			sender += padint(len("ruleAddUDP"))
			sender += "ruleAddUDP"
			sender += padint(len(vmtag))
			sender += vmtag
			fmt.Print("1. Open a UDP Port\n2. Close a UDP Port\n")
			fmt.Scan(&port)
			if port > 65535 {
				fmt.Println("Please select a proper port next time. No scope for overflow here :P")
				menu(conn)
			}
			sender += padint(port)
			fmt.Print("1. Open UDP Port ", port, "\n2. Close UDP Port ", port, "\n")
			fmt.Scan(&operation)
			if operation == 1 {
				action = "open"
			} else if operation == 2 {
				action = "clos"
			} else {
				fmt.Println("Please choose a proper port next time.")
				menu(conn)
			}
			sender += padint(operation)
			resp := getresp(conn)
			if resp == 0 {
				fmt.Println("Successfully ", action, "ed the UDP Port ", port)
				menu(conn)
			} else if resp == 1 {
				fmt.Println("UDP Port ", port, "already ", action, "ed")
				menu(conn)
			} else if resp == 2 {
				fmt.Println("VM with the requested tag not found")
				menu(conn)
			} else {
				fmt.Println("Something went wrong")
				_exit(conn)
			}

		} else {
			fmt.Println("Please select a proper option next time")
			menu(conn)
		}
	} else if modify == 2 {
		fmt.Print("1. Add/Remove RAM\n2. Upscale/Downscale CPU\n")
		fmt.Scan(&resource)
		if resource == 1 {
			sender += padint(len("scaleMemory"))
			sender += "scaleMemory"
			sender += padint(len(vmtag))
			sender += vmtag
			fmt.Print("1. Add RAM\n2. Remove RAM")
			fmt.Scan(&operation)
			sender += padint(operation)
			if operation == 1 {
				fmt.Print("Please enter the amount of RAM that should be added to the VM")
				fmt.Scan(&quantity)
				sender += padint(quantity)
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println("Successfully Added ", quantity, " GB memory to your VM")
					menu(conn)
				} else if resp == 1 {
					fmt.Println("Action Failed, Insufficient Funds to complete the operation.")
					menu(conn)
				} else if resp == 2 {
					fmt.Println("Action Failed, VM with the requested tag not found.")
					menu(conn)
				}
			} else if operation == 2 {
				fmt.Print("Please enter the amount of RAM that should be removed from the VM")
				fmt.Scan(&quantity)
				sender += padint(quantity)
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println("Successfully removed ", quantity, " GB memory your VM")
					menu(conn)
				} else if resp == 1 {
					fmt.Println("Action Failed, the requested quantity is greater than the current VM's RAM.")
					menu(conn)
				} else if resp == 2 {
					fmt.Println("Action Failed, VM with the requested tag not found.")
					menu(conn)
				}
			} else {
				fmt.Println("Undefined option selected")
				menu(conn)
			}
		} else if resource == 2 {
			sender += padint(len("scaleCPU"))
			sender += "scaleCPU"
			fmt.Print("1. Add CPUs to an existing VM\n2. Remove CPUs from an existing VM")
			fmt.Scan(&operation)
			sender += padint(operation)
			if operation == 1 {
				fmt.Print("Please enter the CPUs that should be added to the VM")
				fmt.Scan(&quantity)
				sender += padint(quantity)
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println("Successfully Added ", quantity, " CPUs to your VM")
					menu(conn)
				} else if resp == 1 {
					fmt.Println("Action Failed, Insufficient Funds to complete the operation.")
					menu(conn)
				} else if resp == 2 {
					fmt.Println("Action Failed, VM with the requested tag not found.")
					menu(conn)
				}
			} else if operation == 2 {
				fmt.Print("Please enter the CPUs that should be removed from the VM")
				fmt.Scan(&quantity)
				sender += padint(quantity)
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println("Successfully Removed ", quantity, " CPUs from your VM")
					menu(conn)
				} else if resp == 1 {
					fmt.Println("Action Failed, the requested quantity is greater than the current VM's CPU count.")
					menu(conn)
				} else if resp == 2 {
					fmt.Println("Action Failed, VM with the requested tag not found.")
					menu(conn)
				}

			} else {
				fmt.Println("Undefined option selected")
				menu(conn)
			}

		} else {
			fmt.Println("Please select a proper option.")
			menu(conn)
		}

	} else {
		fmt.Println("Please choose a proper option.")
		menu(conn)
	}
}

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
