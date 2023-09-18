alias ll='ls -lF'
alias la='ls -aF'
alias lla='ls -alF'
alias xargs='xargs '

alias sed='gsed'
alias python='python3'

# Tell ls to be colourful
export CLICOLOR=1
export LSCOLORS=Exfxcxdxbxegedabagacad

# Tell grep to highlight matches
export GREP_OPTIONS='--color=auto'

export TERM="xterm-color"

export PATH=$PATH::~/.npm-global/bin:~/bin:.
export NODE_PATH=$NODE_PATH:~/.npm-global/lib/node_modules
export PYTHONPATH=/usr/local/lib/python3.11/site-packages

source ~/bin/zsh-git-prompt/zshrc.sh
PROMPT='👉 %{$fg[white]%}[%D{%f} %D{%L:%M}]$fg[green]%~%b$(git_super_status)\$ '

# BEGIN SNIPPET: Platform.sh CLI configuration
HOME=${HOME:-'/Users/henrywu21'}
export PATH="$HOME/"'.platformsh/bin':"$PATH"
if [ -f "$HOME/"'.platformsh/shell-config.rc' ]; then . "$HOME/"'.platformsh/shell-config.rc'; fi 
# END SNIPPET

# set random color for new iTerm2 tab
tabcolor() {
  echo -n -e "\033]6;1;bg;red;brightness;$1\a"
  echo -n -e "\033]6;1;bg;green;brightness;$2\a"
  echo -n -e "\033]6;1;bg;blue;brightness;$3\a"
}

tabcolor $(jot -r 1 0 255) $(jot -r 1 0 255) $(jot -r 1 0 255)

# sets the tab title to current dir
echo -ne "\e]1;${PWD##*/}\a"

# for wireshark TLS
export SSLKEYLOGFILE=/Users/$USER/.ssl-key.log

export ANDROID_HOME=~/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/emulator

# Xcode's command-line tools
export PATH=$PATH:/Applications/Xcode.app/Contents/Developer/usr/bin
export DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer"

