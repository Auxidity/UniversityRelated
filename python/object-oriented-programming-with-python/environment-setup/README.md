# object-oriented programming with python

## Overview of course setup

For Python OO course works you need to have 
1. Lab VM running on VirtualBox: VM provides standardised development toolchain and IDE.
2. TUAS gitlab account and working git skills (developed alongside the course). Course exercise instructions and files are distributed from this repository, and you will return your work into your personal forked return repository.

## The environment setup

### Step 1: Install VM

Download VM image from (link valid until 28.1.) https://filesender.funet.fi/?s=download&token=412b3f3e-f1d0-48c3-aefc-bab44132b185  alternatively from emblab ftp ftp://172.27.0.240 navigate to python-oo.
Import VM to VirtualBox.
Modify configuration:
- The default "NAT" network is recommended.
- Check the amount of CPU cores and memory allocated for the VM. 2 cores + 4GB RAM should do, but double that amount is better.
- VM default user/passwd is student/student
Check that you can start the VM, log in and have Ubuntu desktop running with internet connectivity.

### Step 2: Fork lab repository

Log into TUAS gilab https://git.dc.turkuamk.fi/ and in main menu, switch to Groups / Python-OO. (If Python-OO is not shown, ask instructor to add you to that group). In that group there is repository `object-oriented-programming-with-python`. Create a private <b>fork</b> to your personal namespace. A fork is a copy of a project. Forking a repository allows you to make changes without affecting the original project. This forked project works as your return repository.  
- add user `jppaalas` to the project with "Developer" role.
- add tag 'python-oo-2024K' to your repository: In gitlab Settings->General, "Topics"

### Step 3: Customize VM

The installed VM is naturally the same for all students, but will want to use your own identity to sync with TUAS gitlab repository. 
- Configure git identity
```bash
   student@student-VirtualBox:~$ git config --global user.name "Mona Lisa"
   student@student-VirtualBox:~$ git config --global user.email "YOUR_EMAIL@edu.turkuamk.fi"
```
- Create keypair for the VM:
```bash
   student@student-VirtualBox:~$ ssh-keygen -t rsa -b 2048 -f /home/student/.ssh/id_rsa -q -N ""
```
- Copy your public key to your forked project in TUAS gitlab: print your public key on terminal, copy content and paste to TUAS gitlab in browser (top left corner menu box and top-right icon in there, "Edit profile / SSH Keys").
```bash
   student@student-VirtualBox:~$ cat /home/student/.ssh/id_rsa.pub
```
- (Change passwd for student on VM)

### Step 4: Clone your remote repository to your VM

```bash
   student@student-VirtualBox:~$ git clone git@git.dc.turkuamk.fi:YOUR-NAMESPACE/object-oriented-programming-with-python.git
```
If gitlab asks for credentials, then your SSH keys setting has failed.  
You should now have a local git repository containing all lab assignments and files, linked to a private remote repository in TUAS gitlab. 

### Step 5: git + gitlab skills

All your lab work will end up in your git repository, so it is necessary develop git skills as well.  
Check the material and exercises [on this page](git_tutorial.md)

