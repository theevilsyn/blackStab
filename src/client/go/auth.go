package main

import (
	"crypto/x509"
	"encoding/base64"
	"encoding/pem"
	"fmt"
	"math/big"
	"net"
	"os"
)

func auth(conn net.Conn) {
	chlen := getresp(conn)
	challenge := recv(conn, chlen)
	der, _ := pem.Decode(pemBytes)
	if der == nil {
		fmt.Println("No keys!!")
		os.Exit(-1)
	}

	privateKey, err := x509.ParsePKCS1PrivateKey(der.Bytes)
	if err != nil {
		fmt.Println("Something Went Wrong!!")
		os.Exit(-1)
	}

	cipherText, err := base64.StdEncoding.DecodeString(challenge)
	if err != nil {
		fmt.Println("Something Went Wrong!!")
		os.Exit(-1)
	}

	c := new(big.Int).SetBytes(cipherText)
	plainText := base64.StdEncoding.EncodeToString(c.Exp(c, privateKey.D, privateKey.N).Bytes())
	sender := padint(len(plainText))
	sender += plainText
	send(conn, sender)
	resp := getresp(conn)
	if resp == 0 {
		fmt.Println("Authentication Complete")
	} else {
		fmt.Println("Authentication went wrong")
		os.Exit(-1)
	}
}

// TODO: obfuscate the private key

var pemBytes = []byte(`-----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEAy2K2TVjcSdqXqZ+iOtAUamQeXpfhWbg1ATFQ5xoGa3vQLEyD
n52sivdcnYe5+7NDWdR9UXQHJ67IyCqv6J8mzV3BBEOpa/c9FOKLezXq5qizdTh0
WXAr5VM6IVfOXZp+5JmhJQ8Gjzh8ndlPCJ2++qN5zJmuCoFznQW2GY9EL4U2AoRa
TypA+lWIfuBiDNlmeOL5l8PlcKLiEaKapvrfnyqNsCkfeptXcwo8RhRIchmEchpQ
MVfapf01lBFdf/XNLOSwgKSS4T0WIGPlfzV50B5rIj1xPJ7lb7RZbxanyfdE71EU
tPhqtHbi/BA5Txd6I1QXhLV4MHNWjWhZ0gK9xQIDAQABAoIBAQC2qH6lVIry4RiY
RD/Eph/PtP75YVoH48Hmwk2wX9UoLtg1ELqdXVQasjFBYSYNAWAZixbJUnUilHzK
GFxHhLeqdOrmU4YS6sa2vQcbrr66TQRu4DbOJEmn+WkZjOxPcHNKBxeMWsQ/WDHC
6elrCZD9NFgtAlAmK0CT4w86QUqxiUuen2885j+/mOG8AcnFzdKyC5QIlao36mQX
Of7QriwXZvXgrAOibcTtebGmqOH1bUM9W19ii69BtKAAVZ87q4c2l/dcdMDdWH0y
KfvIdxYH07+yJ2zPtEe/mrBpMbRQfomXUgXIHY+flenxmjvrEwM8ztQxpxu6SXoX
5CE3VxYBAoGBAPw8/pRchQmQgU+8RJMKoR8aEo6obzSVvDvPruojii5WjbaHZaNh
GYYNdRK9EWZKHxHXd/HCzWDdQGikZ1qpbAAEiz5KNJQtXqOnZ6dSYCRNEZiEolv/
et6zOtePJgdiMWFpvbvUAmz12F6HrsF+rz9k7L/AGpn1q5iU7yVuHa/BAoGBAM5r
NLnl/Z7ev4nkF8BlczG8nPsTMp0efSG5Ch122T3DmhPNBoRlfp6bcY2AXvVnzjg0
ow/CYFSU4kSaUiDBs3uR8LPuVyma7FzwojNlLlkFtWRiMjRtnW46QkTsDF6Y6M5H
mPqx9HPe5yESXpLIoFPMIVjcqRN6bMRtjQ82og8FAoGBAM6EugOKxLoSAG3iPVsO
xuCKHkuDCJnLRvTJk/LL6mUKJLkfnk3oQFeLSSFwf4B6i3m2KtRcpH78Z7HFeYG3
WV+iWMdFRktT4jqn46wRO/o8x31SiwQ75sPThwfagk5lTPzu8JOKf/nqR58OBD0U
ljOXVGeix6TqifZBapQA1nmBAoGBAIadu8EQkJovQlK3AhZjEwD4tJe5KWT2IT0A
4+vbOknhanZHW1y0pCLj1OYnNcZtcDuPeFgqt4/xmK6Mxcq/CEIqJwPxB78GXecu
t1k1P0inRGi28W7nnafpLpasKlT2+7yrTMURkQ6P68PRqwOm+4gqtASzw0AEszJX
D4tAYefRAoGBAO+6EXdiVY1iDrBm9NSgV90QXVA1p4dsYYeLpDN5H8YqfgcJRV5O
iTg7XlZ4nN+sVsoIHDu6bf/aorulEhe9MSTPgJcgazY8nH+gEJMgMfP3pDnOSFgv
+K24+mgGEtnlWYyzeq/+lbteo3hx1Zu/uXlBrFiDDgnyTn5yWWJauS8P
-----END RSA PRIVATE KEY-----`)
