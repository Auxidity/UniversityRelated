# Useful Linux commands from class walkthrough

```
		git status
		ls -al
		mkdir playground
		cd playground
		nano demo.txt
			ctrl-S	save
			ctrl-X  exit
		git add *
		git commit -a -m"message"
		git checkout <commit number>
		cat demo.txt
		git tag -a v1.00 -m""
		git checkout -b newfeature
		git log --oneline --graph --all
		
	>>in order to merge newfeature to main:
		git checkout main
		git merge newfeature
```
