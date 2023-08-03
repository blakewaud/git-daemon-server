# Git Daemon Server for Local Collaboration

This script provides a simple implementation of the Git Daemon server to allow local collaboration within a private network. It uses Invoke to implement the commands. I created this to help me collaborate with a client who used a private Gitlab server which was only accessible from within their corporate network via VPN and their VPN client could only be installed on their laptops. This set of scripts allows one to work on a personal PC and then ultimately push to the private client git server.

Eventually this set of scripts will allow the user to setup the Windows Firewall, initialize the server, and push/pull from that server, but for now, this readme serves as the primary documentation of how I did it (for myself and anyone else)

**NOTE:** I am sure there is a better way to do this via open git servers you could get from all sorts of sources, but I was trying to minimize my use of any additional tools, and focused on what I already knew and used (e.g., `git`).

# Prerequisites

* Windows Subsystem for Linux
* Invoke

# How it works

Git provides for the following command:

```shell
git daemon
```

Which has several options, but primarily allows for unauthenticated serving of specific repositories via the `git://` protocol.

With the following set of options, it is possible to server a bare repository and allow pushing from other git clients, but it is import to note that there is a known issue within the Git for Windows project that prevents that version of the client from acting as the server and receive pushes from clients.

This necesitates the need for WSL; however, the way WSL2 works in Windows 10 and 11 virtualizes the subsystem's network adapters in such a way that I was not able to figure out hot to properly set up a port-forward that allows clients on the rest of the LAN to actually pull from it. It is for this reason that you must use WSL for both the client and server when doing push operations and the Git for Windows client when serving other clients for pull operations.

Ultimately, I found the best set of options to run the daemon with where as follows:

```shell
git daemon --reuseaddr --base-path=<root-of-server-repos> --export-all --verbose --enable=receive-pack
```

This allows the daemon to export all repos within the server's base-path directory and receive pushes.

> **WARNING**: Setting up a daemon like this would allow anyone to push to it! Only configure this if you are in a private network!

In addition to the daemon settings, in order for the server to function within the LAN, you must open inbound port 9418 on the PC hosting the server.

Once that is known, you are able to start the daemon from WSL and then add a remote to your working repository like so:

```shell
git remote add local git://localhost:9418/<repo-path>.git
```

**NOTE:** I created a separate directory for the server's base path and then added a directory of the same name as the repository within it before attempting to push to it.

After this, you can push from your working repository like so:

```shell
git push local
```

Finally, to get your commits from this local bare repository to a different networked client, you must kill the daemon running in WSL and restart it from windows using the same command (or without the `--enable:receive-pack` option).

You can then add a remote and pull from the other networked client like so:

```shell
git remote add local git://<ip-of-server>:9418/<repo-path>.git
git pull local <branch-name>
```

**NOTE**: I am not sure if the port number is required in the URL, but it worked with it included so I include it here.