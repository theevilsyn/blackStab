package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

func deleteacc(conn net.Conn) {
	var choice string
	var password string
	sender := padint(0)
	sender += padint(len("deleteAccount"))
	sender += "deleteAccount"
	fmt.Print("For security reasons, please enter your password: ")
	fmt.Scan(&password)
	fmt.Println("Are you sure you want to delete your account? [y/n]")
	fmt.Print("Choice >> ")
	fmt.Scan(&choice)
	if choice == "y" {
		fmt.Print()
	} else {
		fmt.Println()
		menu(conn, "Alright, taking you back to main menu")
	}
	sender += padint(len(password))
	sender += password
	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println("Successfully Removed your Account, Bye!")
		// _exit(conn)
		conn.Close()
	} else {
		fmt.Println()
		menu(conn, "Password Incorrect :(")
	}
}

func viewsubscription(conn net.Conn) {
	sender := padint(0)
	sender += padint(len("viewSubscription"))
	sender += "viewSubscription"
	send(conn, sender)
	credits := getresp(conn)
	fmt.Println()
	menu(conn, "You have "+strconv.Itoa(credits)+"$ worth credits left in your free subscription")
}

func listmyvms(conn net.Conn) {
	sender := padint(0)
	sender += padint(len("listallmyVMs"))
	sender += "listallmyVMs"
	send(conn, sender)
	count := getresp(conn)
	if count == 0 {
		fmt.Println()
		menu(conn, "You have 0 VMs associated to your account")
	} else {
		list := recv(conn, count)
		fmt.Print(list)
		fmt.Println()
		menu(conn, list)
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
	fmt.Println()
	menu(conn, status)
}

func deletevm(conn net.Conn) {
	var vmtag string
	var choice string
	sender := padint(0)
	sender += padint(len("deleteVM"))
	sender += "deleteVM"
	fmt.Print("Enter VM Tag: ")
	fmt.Scan(&vmtag)
	fmt.Println("Are you sure you want to delete the VM? [y/n]")
	fmt.Print("Choice >> ")
	fmt.Scan(&choice)
	if choice == "y" {
		fmt.Print()
	} else {
		fmt.Println()
		menu(conn, "")
	}

	sender += padint(len(vmtag))
	sender += vmtag
	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println()
		menu(conn, "Successfully deleted the VM")
	} else if resp == 1 {
		fmt.Println()
		menu(conn, "Action failed, the VM with requested tag not found.")
	}
}

func modifyvm(conn net.Conn) {
	var port int
	var proto int
	var modify int
	var choice string
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
			fmt.Print("Enter the port: ")
			fmt.Scan(&port)
			if port > 65535 {
				fmt.Println()
				menu(conn, "Please select a proper port next time. No scope for overflow here :P")
			}
			sender += padint(port)
			fmt.Print("1. Open TCP Port ", port, "\n2. Close TCP Port ", port, "\n")
			fmt.Scan(&operation)
			if operation == 1 {
				action = "opened"
			} else if operation == 2 {
				action = "closed"
			} else {
				fmt.Println()
				menu(conn, "Please choose a proper port next time.")
			}
			sender += padint(operation)
			fmt.Println("Are you sure you want to modify the VM's TCP ingress rules? [y/n]")
			fmt.Print("Choice >> ")
			fmt.Scan(&choice)
			if choice == "y" {
				fmt.Print()
			} else {
				fmt.Println()
				menu(conn, "")
			}
			send(conn, sender)
			resp := getresp(conn)
			if resp == 0 {
				fmt.Println()
				menu(conn, "Successfully "+action+" the TCP Port "+strconv.Itoa(port))
			} else if resp == 1 {
				fmt.Println()
				menu(conn, "TCP Port "+strconv.Itoa(port)+"already "+action)
			} else if resp == 2 {
				fmt.Println()
				menu(conn, "VM with the requested tag not found")
			} else {
				fmt.Println("Something went wrong")
				_exit(conn)
			}
		} else if proto == 2 {
			sender += padint(len("ruleAddUDP"))
			sender += "ruleAddUDP"
			sender += padint(len(vmtag))
			sender += vmtag
			fmt.Print("Enter the port: ")
			fmt.Scan(&port)
			if port > 65535 {
				fmt.Println()
				menu(conn, "Please select a proper port next time. No scope for overflow here :P")
			}
			sender += padint(port)
			fmt.Print("1. Open UDP Port ", port, "\n2. Close UDP Port ", port, "\n")
			fmt.Scan(&operation)
			if operation == 1 {
				action = "opened"
			} else if operation == 2 {
				action = "closed"
			} else {
				fmt.Println()
				menu(conn, "Please choose a proper port next time.")
			}
			sender += padint(operation)
			fmt.Println("Are you sure you want to modify the VM's UDP ingress rules? [y/n]")
			fmt.Print("Choice >> ")
			fmt.Scan(&choice)
			if choice == "y" {
				fmt.Print()
			} else {
				fmt.Println()
				menu(conn, "")
			}
			send(conn, sender)
			resp := getresp(conn)
			if resp == 0 {
				fmt.Println()
				menu(conn, "Successfully "+action+" the UDP Port "+strconv.Itoa(port))
			} else if resp == 1 {
				fmt.Println()
				menu(conn, "UDP Port "+strconv.Itoa(port)+"already "+action)
			} else if resp == 2 {
				fmt.Println()
				menu(conn, "VM with the requested tag not found")
			} else {
				fmt.Println("Something went wrong")
				_exit(conn)
			}

		} else {
			fmt.Println()
			menu(conn, "Please select a proper option next time")
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
				fmt.Println("Are you sure you want to modify the VM's Shape? [y/n]")
				fmt.Print("Choice >> ")
				fmt.Scan(&choice)
				if choice == "y" {
					fmt.Print()
				} else {
					fmt.Println()
					menu(conn, "")
				}
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println()
					menu(conn, "Successfully Added "+strconv.Itoa(quantity)+" GB memory to your VM")
				} else if resp == 1 {
					fmt.Println()
					menu(conn, "Action Failed, Insufficient Funds to complete the operation.")
				} else if resp == 2 {
					fmt.Println()
					menu(conn, "Action Failed, VM with the requested tag not found.")
				}
			} else if operation == 2 {
				fmt.Print("Please enter the amount of RAM that should be removed from the VM")
				fmt.Scan(&quantity)
				sender += padint(quantity)
				fmt.Println("Are you sure you want to modify the VM's Shape? [y/n]")
				fmt.Print("Choice >> ")
				fmt.Scan(&choice)
				if choice == "y" {
					fmt.Print()
				} else {
					fmt.Println()
					menu(conn, "")
				}
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println()
					menu(conn, "Successfully removed "+strconv.Itoa(quantity)+" GB memory your VM")
				} else if resp == 1 {
					fmt.Println()
					menu(conn, "Action Failed, the requested quantity is greater than the current VM's RAM.")
				} else if resp == 2 {
					fmt.Println()
					menu(conn, "Action Failed, VM with the requested tag not found.")
				}
			} else {
				fmt.Println()
				menu(conn, "Undefined option selected")
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
				fmt.Println("Are you sure you want to modify the VM's Shape? [y/n]")
				fmt.Print("Choice >> ")
				fmt.Scan(&choice)
				if choice == "y" {
					fmt.Print()
				} else {
					fmt.Println()
					menu(conn, "")
				}
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println()
					menu(conn, "Successfully added "+strconv.Itoa(quantity)+" CPUs your VM")
				} else if resp == 1 {
					fmt.Println()
					menu(conn, "Action Failed, Insufficient Funds to complete the operation.")
				} else if resp == 2 {
					fmt.Println()
					menu(conn, "Action Failed, VM with the requested tag not found.")
				}
			} else if operation == 2 {
				fmt.Print("Please enter the CPUs that should be removed from the VM")
				fmt.Scan(&quantity)
				sender += padint(quantity)
				fmt.Println("Are you sure you want to modify the VM's Shape? [y/n]")
				fmt.Print("Choice >> ")
				fmt.Scan(&choice)
				if choice == "y" {
					fmt.Print()
				} else {
					fmt.Println()
					menu(conn, "Alright, taking you back to main menu")
				}
				send(conn, sender)
				resp := getresp(conn)
				if resp == 0 {
					fmt.Println()
					menu(conn, "Successfully Removed "+strconv.Itoa(quantity)+" CPUs from your VM")
				} else if resp == 1 {
					fmt.Println()
					menu(conn, "Action Failed, the requested quantity is greater than the current VM's CPU count.")
				} else if resp == 2 {
					fmt.Println()
					menu(conn, "Action Failed, VM with the requested tag not found.")
				}

			} else {
				fmt.Println()
				menu(conn, "Undefined option selected")
			}

		} else {
			fmt.Println()
			menu(conn, "Undefined option selected")
		}

	} else {
		fmt.Println()
		menu(conn, "Undefined option selected")
	}
}

func createvm(conn net.Conn) {
	var vmname string
	var vmtag string
	var choice string
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
		fmt.Println()
		menu(conn, "Please select a valid operating system next time")
	} else if image == 6 {
		fmt.Println("This is to inform you that you are about to waste $150 cloud credits on --windows VM-- ")
		fmt.Print("\n\t1. Continue\n\t2. Use your mind.\n")
		fmt.Scan(&winchoice)
		switch winchoice {

		case 1:
			fmt.Println("Mehh, alright ¯\\_(ツ)_/¯")
		case 2:
			fmt.Println()
			menu(conn, "Good Choice!! You just saved 150$ just by using your mind!! f4lc0n appreciates you :P")
		default:
			fmt.Println()
			menu(conn, "Good Choice!! You just saved 150$ just by using your mind!! f4lc0n appreciates you :P")
		}

	}
	sender := padint(0) + padint(len(funcname)) + funcname + padint(len(vmname)) + vmname + padint(len(vmtag)) + vmtag + padint(image)
	fmt.Println("Are you sure you want to use $150 from your free subscription to spawn a VM with the selected options? [y/n]")
	fmt.Print("Choice >> ")
	fmt.Scan(&choice)
	if choice == "y" {
		fmt.Print()
	} else {
		fmt.Println()
		menu(conn, "")
	}

	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println("Successfully created the VM print image, config and say you canyou can scale the vm")
		details := padint(0)
		details += padint(len("statusofmyVM"))
		details += "statusofmyVM"
		details += padint(len(vmtag))
		details += vmtag
		send(conn, details)
		resp := getresp(conn)
		fmt.Println()
		menu(conn, "Here are the details of the VM that has just been spawned\n"+recv(conn, resp))
	} else if resp == 1 {
		fmt.Println()
		menu(conn, "VM with the requested tag is already present")
	} else if resp == 2 {
		fmt.Println()
		menu(conn, "Funds not sufficient to spawn a VM")
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
	if len(email) > 90 {
		fmt.Println("Sorry, email can't be greater than 100 characters")
		os.Exit(0)
	} else if len(username) > 90 {
		fmt.Println("Sorry, username can't be greater than 100 characters")
		os.Exit(0)
	} else {
		fmt.Println("Sorry, password can't be greater than 100 characters")
		os.Exit(0)
	}

	sender := padint(1) + padint(len(email)) + email + padint(len(username)) + username + padint(len(password)) + password
	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {
		print("Registration Successful")
	} else if resp == 1 {
		fmt.Println("Email Already Taken")
		send(conn, "-337")
		conn.Close()
		os.Exit(0)
	} else if resp == 2 {
		fmt.Println("Password is not greater than 12 :/")
		send(conn, "-337")
		conn.Close()
		os.Exit(0)
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
		fmt.Println("Successfully Logged In")
		menu(conn, "")
	} else if resp == 1 {
		fmt.Println("User Not Found")
		send(conn, "-337")
		conn.Close()
		os.Exit(0)
	} else if resp == 2 {
		fmt.Println("Password Incorrect")
		send(conn, "-337")
		conn.Close()
		os.Exit(0)
	} else {
		print("Something Went Wrong")
		_exit(conn)
	}

}
