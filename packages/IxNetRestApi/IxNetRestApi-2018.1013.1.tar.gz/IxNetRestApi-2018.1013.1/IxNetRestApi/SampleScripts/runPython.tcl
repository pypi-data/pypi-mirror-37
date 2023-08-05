#!/usr/local/ActiveTcl-8.6/bin/expect

# Example to show how to use TCL's Expect extension to execute Python scripts.

proc GetShellPrompt {} {
   set prompt "(%|#|>|\\\$) ?$"
   return $prompt
}

proc Connect {device} {
    spawn $device
    expect {
	-re [GetShellPrompt] {
	    puts "\nConnected to $device"
	}
	timeout {
	    puts "Error: Timed out connecting to $device"
	}
    }
    return $spawn_id
}

proc SendCommand { id command {timeout -1}} {
    set timeout $timeout
    set send_human {.3 .4 0.6 .1 3}
    puts "\nSendCommand: $command"
    send -i $id $command
    expect -i $id .*
    send -i $id \r
    expect {
        -i $id
	-re [GetShellPrompt] {
	    puts "\nGot prompt"
	}
        timeout {
            puts "Error: Command timed out: $command"
        }
    }
    #puts "\nOutput: $expect_out(buffer)\n"
}


set pythonPath /usr/local/python3.7.0/bin/python3.7
set script "/home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/SampleScripts/bgpNgpf.py"

set spawnId  [Connect csh]

# Example 1
SendCommand $spawnId "$pythonPath $script"
#SendCommand $spawnId "$pythonPath bgpNgpf.py"
#SendCommand $spawnId "/home/hgee/myPyTest.py"

# Example 2
#SendCommand $spawnId $python
#SendCommand $spawnId "import bgpNgpf"


# Example 3:
#    but you cannot see the output at real time. 
#    The output shows up at the end and it is stored in the output variable.
#set output [exec /usr/local/python3.7.0/bin/python3.7 /home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/SampleScripts/bgpNgpf.py]
#puts $output



















#-------- Interactive mode --------#

if 0 {
spawn python2.7 ixnetCli.py
expect {
    "ixShell> " {
	puts "Got spawn prompt"
    }
    timeout {
	puts "ixShell timedout"
    }
}

#SendCommand $spawn_id "connect bgpConfig.json apiServerIpAddress=192.168.70.127"
#SendCommand $spawn_id "runbgp"

set ixChassisIp 172.28.95.60
# Both inputs works.
#SendCommand $spawn_id "loadJsonConfig exportedBgp.json portList={'$ixChassisIp': (('vport1', '1/1'), ('vport2', '2/1'))}"
#SendCommand $spawn_id "loadJsonConfig exportedBgp.json {'$ixChassisIp': (('vport1', '1/1'), ('vport2', '2/1'))}"
}
