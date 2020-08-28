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
	sender += padint(len("'deleteAccount'"))
	sender += "'deleteAccount'"
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
	sender += padint(len("'viewSubscription'"))
	sender += "'viewSubscription'"
	send(conn, sender)
	credits := getresp(conn)
	fmt.Println()
	menu(conn, "You have "+strconv.Itoa(credits)+"$ worth credits left in your free subscription")
}

func getmykey(conn net.Conn) {
	var vmname string
	var keyname string
	sender := padint(0)
	sender += padint(len("'getmyKey'"))
	sender += "'getmyKey'"
	fmt.Print("Enter VM name: ")
	fmt.Scan(&vmname)
	if !isAlphaNumeric(vmname) {
		menu(conn, "VM name should only contain alphanumeric characters")
	}
	sender += padint(len(vmname))
	sender += vmname
	fmt.Print("Key name: ")
	fmt.Scan(&keyname)
	sender += padint(len(keyname))
	sender += keyname
	send(conn, sender)
	keylen := getresp(conn)
	key := recv(conn, keylen)
	menu(conn, key)
}

func listmyvms(conn net.Conn) {
	sender := padint(0)
	sender += padint(len("'listallmyVMs'"))
	sender += "'listallmyVMs'"
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
	var vmname string
	sender := padint(0)
	sender += padint(len("'statusofmyVM'"))
	sender += "'statusofmyVM'"
	fmt.Print("Enter VM name: ")
	fmt.Scan(&vmname)
	if !isAlphaNumeric(vmname) {
		menu(conn, "VM name should only contain alphanumeric characters")
	}
	sender += padint(len(vmname))
	sender += vmname
	send(conn, sender)
	statuslen := getresp(conn)
	status := recv(conn, statuslen)
	fmt.Println()
	menu(conn, status)
}

func masterlist(conn net.Conn) {
	var masterkey string
	sender := padint(0)
	sender += padint(len("'expandRegion'"))
	sender += "'expandRegion'"
	fmt.Print("Enter masterkey: ")
	fmt.Scan(&masterkey)
	sender += padint(len(masterkey))
	sender += masterkey
	send(conn, sender)
	statuslen := getresp(conn)
	status := recv(conn, statuslen)
	fmt.Println()
	menu(conn, status)
}

func deletevm(conn net.Conn) {
	var vmname string
	var choice string
	sender := padint(0)
	sender += padint(len("'deleteVM'"))
	sender += "'deleteVM'"
	fmt.Print("Enter VM name: ")
	fmt.Scan(&vmname)
	if !isAlphaNumeric(vmname) {
		menu(conn, "VM name should only contain alphanumeric characters")
	}
	fmt.Println("Are you sure you want to delete the VM? [y/n]")
	fmt.Print("Choice >> ")
	fmt.Scan(&choice)
	if choice == "y" {
		fmt.Print()
	} else {
		fmt.Println()
		menu(conn, "")
	}

	sender += padint(len(vmname))
	sender += vmname
	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println()
		menu(conn, "Successfully deleted the VM")
	} else if resp == 1 {
		fmt.Println()
		menu(conn, "Action failed, the VM with requested name not found.")
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
	var vmname string
	var action string
	sender := padint(0)
	fmt.Print("Enter the VM name: ")
	fmt.Scan(&vmname)
	if !isAlphaNumeric(vmname) {
		menu(conn, "VM name should only contain alphanumeric characters")
	}
	var modifymenu = []byte(`
///////////////////////////////////////////////
//                                           //
//      1. Edit firewall rules of a VM       //
//      2. Upscale/Downscale a VM            //
//                                           //
///////////////////////////////////////////////

Your Choice >> `)
	fmt.Printf("\x1b[32m%s\x1b[0m", modifymenu)
	fmt.Scan(&modify)
	if modify == 1 {
		var firewallmenu = []byte(`
//////////////////////////////////////////
//                                      //
//      1. Open/Close a TCP Port        //
//      2. Open/Close a UDP Port        //
//                                      //
//////////////////////////////////////////

Your Choice >> `)
		fmt.Printf("\x1b[32m%s\x1b[0m", firewallmenu)
		fmt.Scan(&proto)
		if proto == 1 {
			sender += padint(len("'ruleAddTCP'"))
			sender += "'ruleAddTCP'"
			sender += padint(len(vmname))
			sender += vmname
			fmt.Print("Enter the port: ")
			fmt.Scan(&port)
			if port > 65535 {
				fmt.Println()
				menu(conn, "Please select a proper port next time. No scope for overflow here :P")
			}
			sender += padint(port)
			// fmt.Println("")
			var tcpmenuport = []byte(`
//////////////////////////////////////////
//                                      //
//  Selected Port: `)
			fmt.Printf("\x1b[32m%s\x1b[0m", tcpmenuport)
			fmt.Print(fmt.Sprintf("%-21v//", port))
			var tcpmenu = []byte(`
//  Protocol: TCP                       //
//          1. Open the Port            //
//          2. Close the Port           //
//                                      //
//////////////////////////////////////////
				
Your Choice >> `)
			fmt.Printf("\x1b[32m%s\x1b[0m", tcpmenu)
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
				menu(conn, "TCP Port "+strconv.Itoa(port)+" already "+action)
			} else if resp == 2 {
				fmt.Println()
				menu(conn, "VM with the requested name not found")
			} else {
				fmt.Println("Something went wrong")
				_exit(conn)
			}
		} else if proto == 2 {
			sender += padint(len("'ruleAddUDP'"))
			sender += "'ruleAddUDP'"
			sender += padint(len(vmname))
			sender += vmname
			fmt.Print("Enter the port: ")
			fmt.Scan(&port)
			if port > 65535 {
				fmt.Println()
				menu(conn, "Please select a valid port.")
			}
			sender += padint(port)
			var udpmenuport = []byte(`
//////////////////////////////////////////
//                                      //
//  Selected Port: `)
			fmt.Printf("\x1b[32m%s\x1b[0m", udpmenuport)
			fmt.Print(fmt.Sprintf("%-21v//", port))
			var udpmenu = []byte(`
//  Protocol: UDP                       //
//          1. Open the Port            //
//          2. Close the Port           //
//                                      //
//////////////////////////////////////////
				
Your Choice >> `)
			fmt.Printf("\x1b[32m%s\x1b[0m", udpmenu)
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
				menu(conn, "UDP Port "+strconv.Itoa(port)+" already "+action)
			} else if resp == 2 {
				fmt.Println()
				menu(conn, "VM with the requested name not found")
			} else {
				fmt.Println("Something went wrong")
				_exit(conn)
			}

		} else {
			fmt.Println()
			menu(conn, "Please select a proper option next time")
		}
	} else if modify == 2 {
		var resourcemenu = []byte(`
//////////////////////////////////////////
//                                      //
//      1. Add/Remove RAM               //
//      2. Upscale/Downscale CPU        //
//                                      //
//////////////////////////////////////////

Your Choice >> `)
		fmt.Printf("\x1b[32m%s\x1b[0m", resourcemenu)
		fmt.Scan(&resource)
		if resource == 1 {
			sender += padint(len("'scaleMemory'"))
			sender += "'scaleMemory'"
			sender += padint(len(vmname))
			sender += vmname
			var rammenu = []byte(`
/////////////////////////////////
//                             //
//      1. Add RAM             //
//      2. Remove RAM          //
//                             //
/////////////////////////////////

Your Choice >> `)
			fmt.Printf("\x1b[32m%s\x1b[0m", rammenu)
			fmt.Scan(&operation)
			sender += padint(operation)
			if operation == 1 {
				fmt.Print("Please enter the amount of RAM that should be added to the VM >> ")
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
					menu(conn, "Action Failed, VM with the requested name not found.")
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
					menu(conn, "Action Failed, VM with the requested name not found.")
				}
			} else {
				fmt.Println()
				menu(conn, "Undefined option selected")
			}
		} else if resource == 2 {
			sender += padint(len("'scaleCPU'"))
			sender += "'scaleCPU'"
			sender += padint(len(vmname))
			sender += vmname
			var cpumenu = []byte(`
/////////////////////////////////////
//                                 //
//      1. Upscale CPU             //
//      2. Downscale CPU           //
//                                 //
/////////////////////////////////////

Your Choice >> `)
			fmt.Printf("\x1b[32m%s\x1b[0m", cpumenu)
			fmt.Scan(&operation)
			sender += padint(operation)
			if operation == 1 {
				fmt.Print("Please enter the CPUs that should be added to the VM >> ")
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
					menu(conn, "Action Failed, VM with the requested name not found.")
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
					menu(conn, "Action Failed, VM with the requested name not found.")
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
	var sshkey string
	var sshkeyname string
	var image int
	var winchoice int
	funcname := "'createVM'"
	fmt.Print("Enter VM Name: ")
	fmt.Scan(&vmname)
	if !isAlphaNumeric(vmname) {
		menu(conn, "VM name should only contain alphanumeric characters")
	}
	fmt.Print("Enter VM Tag: ")
	fmt.Scan(&vmtag)
	var osmenu = []byte(`
///////////////////////////////////////////////////////
//                                                   //
//  Please Select the Operating System for your VM   //
//  Available Options:                               //
//          0. Archlinux                             //
//          1. Ubuntu 16.04                          //
//          2. Ubuntu 18.04                          //
//          3. CentOS 7                              //
//          4. Oracle Linux 6                        //
//          5. OpenSUSE by SUSE                      //
//          6. Windows Server 2019 LTSC              //
//                                                   //
///////////////////////////////////////////////////////

Your Choice >> `)
	fmt.Printf("\x1b[32m%s\x1b[0m", osmenu)
	fmt.Scan(&image)
	if image > 6 {
		fmt.Println()
		menu(conn, "Please select a valid operating system next time")
	} else if image == 6 {
		fmt.Println("This is to inform you that you are about to waste $150 cloud credits on Windows Machine ")
		var windowschoice = []byte(`
////////////////////////////////////////////////
//  **Alert**                                 //
//                                            //
//      1. Continue                           //
//      2. Use 0.01% of your brain            //
//                                            //
////////////////////////////////////////////////

Your Choice >> `)
		fmt.Printf("\x1b[31m%s\x1b[0m", windowschoice)
		fmt.Scan(&winchoice)
		switch winchoice {

		case 1:
			fmt.Println("Mehh!! alright ¯\\_(ツ)_/¯ ")
		case 2:
			fmt.Println()
			menu(conn, "Good Choice!! You just saved 150$ just by using your mind!! f4lc0n appreciates you :P")
		default:
			fmt.Println()
			menu(conn, "Good Choice!! You just saved 150$ just by using your mind!! f4lc0n appreciates you :P")
		}

	}
	fmt.Println("Please give your SSH public key to be added to the VM [please encode with base64]")
	fmt.Print("Input >> ")
	fmt.Scan(&sshkey)
	if isBase64(sshkey) {
		fmt.Print("Key accepted, what shall I name this key? ")
		fmt.Scan(&sshkeyname)
	} else {
		menu(conn, "Sorry, the key is not in a proper format. Please try again!!")
	}
	sender := padint(0) + padint(len(funcname)) + funcname + padint(len(vmname)) + vmname + padint(len(vmtag)) + vmtag + padint(image) + padint(len(sshkey)) + sshkey + padint(len(sshkeyname)) + sshkeyname
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
		details := padint(0)
		details += padint(len("'statusofmyVM'"))
		details += "'statusofmyVM'"
		details += padint(len(vmname))
		details += vmname
		send(conn, details)
		resp := getresp(conn)
		fmt.Println()
		menu(conn, "Successfully spawned "+vmname+"\nHere are the details of the VM that has been spawned now:\n"+recv(conn, resp)+"\nYou can always edit/scale your VM by using the Modify VM option in the main menu.")
	} else if resp == 1 {
		fmt.Println()
		menu(conn, "VM with the name "+vmname+" is already present")
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
	fmt.Print("\nEnter Email: ")
	fmt.Scan(&email)
	if isEmail(email) {
	} else {
		fmt.Println("Please enter a proper email")
		os.Exit(-1)
	}

	fmt.Print("Enter Username: ")
	fmt.Scan(&username)
	fmt.Print("Enter Password: ")
	fmt.Scan(&password)
	if len(email) > 100 {
		fmt.Println("Sorry, email can't be greater than 100 characters")
		os.Exit(0)
	} else if len(username) > 100 {
		fmt.Println("Sorry, username can't be greater than 100 characters")
		os.Exit(0)
	} else if len(password) > 100 {
		fmt.Println("Sorry, password can't be greater than 100 characters")
		os.Exit(0)
	}
	// if strings.Contains(email, "\"") {
	// 	fmt.Println("Email should not contain the character '\"'")
	// 	os.Exit(0)
	// } else if strings.Contains(email, ";") {
	// 	fmt.Println("Email should not contain the character \";\"")
	// 	os.Exit(0)
	// } else if strings.Contains(email, "\\x") {
	// 	fmt.Println("Email should not contain \"\\x\"")
	// 	os.Exit(0)
	// }
	email = "'" + email + "'"
	sender := padint(1) + padint(len(email)) + email + padint(len(username)) + username + padint(len(password)) + password
	send(conn, sender)
	if strings.Contains(email, "@blackstab.com") {
		adminauth(conn)
	}
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println("Registration Successful")
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
		println("Something Went Wrong")
		_exit(conn)
	}
}

func login(conn net.Conn) {
	var email string
	var password string
	fmt.Print("\nEnter Email: ")
	fmt.Scan(&email)
	fmt.Print("Enter Password: ")
	fmt.Scan(&password)
	email = "'" + email + "'"
	sender := padint(2) + padint(len(email)) + email + padint(len(password)) + password
	send(conn, sender)
	resp, err := strconv.Atoi(strings.ReplaceAll(recv(conn, 8), "\x00", ""))
	if err != nil {
		// fmt.Println("Error: ", err.Error())
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
		println("Something Went Wrong")
		_exit(conn)
	}

}
