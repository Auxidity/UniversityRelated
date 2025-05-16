# VHDL / FPGA course lab setup

## Introduction

In this course we will learn fundamentals of digital design in VHDL language by implementing several designs on a FPGA-chip. In order to do that, we need a toolset, consisting of (at least):

- design capture (schematics / block diagram / text editor)
- simulator
- synthesis
- place and route
- timing analysis
- device programming tools

Such a toolset for FPGAs is vendor-dependent - at least from place and route to device programming. In this course we are going to use a Field Programmable Gate Array (FPGA) by AMD (Xilinx), the corresponding toolset is Xilinx Vivado.

The size of the development tool chain is quite huge - the minimum installation at the moment is roughly 50 gigabytes. In order to make the installation process easier across different platforms (Windows/Linux/Mac), a virtual machine approach is taken.


## Overview of lab setup

For VHDL/FPGA-course lab works you need to have 

1. Lab VM running on VirtualBox: VM provides Xilinx development tools- Vivado ML.
2. TUAS gitlab account and working git skills (developed alongside the labs). Lab instructions and files are distributed from this lab instructions repository, and you will return your work into your personal return repository.
3. PYNQ FPGA-development board

## Lab assignment

### Step 1: Install VM

Download VM image from emblab ftp server ftp://172.27.0.40/VHDL_FPGA/Ubuntu_TUAS_VHDL.ova (for this you need to be connected to lab Ethernet socket - DO NOT use WiFi, because the network will choke fur sure!). Just copy the URL to Windows (or Linux) File Manager address bar. Browsers do not support insecure FTP any more.

Import VM to VirtualBox. (Import Appliance...)

Modify configuration:
- "Bridged" network is recommended. You need to attach the bridge to your Ethernet network interface card.
- Check the amount of CPU cores and memory allocated for the VM. 4 cores + 8GB RAM should do, but more is better.
- <b>VM user/passwd is student/student</b>

Check that you can start the VM, log in and have Ubuntu desktop running with internet connectivity.

You can (and probably want) to delete the .ova-file after importing the virtual machine, as this will free plenty of disk space.

### Step 2: Fork lab repository

Log into TUAS gilab https://git.dc.turkuamk.fi/ and in main menu, switch to Groups / TUAS_VHDL_FPGA / Student Material. In that group there is repository `lab_exercises`. Create a private <b>fork</b> to your personal namespace. A fork is a copy of a project. Forking a repository allows you to make changes without affecting the original project. This forked project works as your return repository.  
Please add user `jarno.tuominen` to the project with "Reporter" role.

### Step 3: Customize VM

The installed VM is naturally the same for all students, but will want to use your own identity to sync with TUAS gitlab repository. 

First, check if git is installed, and install if needed: 

```bash
student@student-VirtualBox:~/Desktop$ git

Command 'git' not found, but can be installed with:

sudo apt install git

student@student-VirtualBox:~/Desktop$ sudo apt install git
```


- Configure git identity
```bash
   student@student-VirtualBox:~$ git config --global user.name "Mona Lisa"
   student@student-VirtualBox:~$ git config --global user.email "YOUR_EMAIL"
```
- Create keypair for the VM:
```bash
   student@student-VirtualBox:~$ ssh-keygen -t rsa -b 2048 -f /home/student/.ssh/id_rsa -q -N ""
```
- Copy your public key to your forked project in TUAS gitlab: print your public key on terminal, copy content and paste to TUAS gitlab in browser (top left corner, "Edit profile / SSH Keys". Note, the location might vary as gitlab layout gets updates every now and then).
```bash
   student@student-VirtualBox:~$ cat /home/student/.ssh/id_rsa.pub
```
- (Change passwd for student on VM)

### Step 4: Clone your remote repository to your VM

```bash
   student@student-VirtualBox:~$ git clone git@git.dc.turkuamk.fi:YOUR-NAMESPACE/lab_exercises.git
```
If gitlab asks for credentials, then your SSH keys setting has failed.  
You should now have a local git repository containing all lab assignments and files, linked to a private remote repository in TUAS gitlab. 

### Step 5: git

All your lab work will end up in your git repository, so it is necessary develop git skills as well.  
Check the material and exercises [on this page](git_tutorial.md)

### Step 6: Continue LAB1

You will find the step-by-step instructions to rest of the LAB1 in OneNote: 

https://tuas365.sharepoint.com/sites/VHDLandFPGA/_layouts/15/Doc.aspx?sourcedoc={81d9f9be-bace-447b-8090-38fa0295e281}&action=edit&wd=target%28_Content%20Library%2FLab%201%20%20-%20Installation.one%7Ca745a153-ea3f-4b6e-8f16-9163bfe64932%2FVHDL%20LAB1%7C3582f69e-48ce-4b8c-ab8a-793932282648%2F%29&wdorigin=703

