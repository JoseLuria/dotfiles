eval "$(starship init zsh)"

alias la="ls -la"
alias dev="cd ~/Development"
alias conf="cd ~/.config"

_change_branch() {
  branch_name=$(git branch | fzf --header="change branch")
  if [ ! -z $branch_name ]
  then
    git checkout "${branch_name##*( )}"
    zle reset-prompt
  fi
}

_delete_branch() {
  branch_name=$(git branch | fzf --header="delete branch")
  if [ ! -z $branch_name ]
  then
    git branch -D "${branch_name##*( )}"
    zle reset-prompt
  fi
}

_open_project_folder(){
  project=$(ls ~/Development | fzf --header="change project")
  if [ ! -z $project ]
  then
    cd ~/Development/$project
    zle reset-prompt
  fi
}

zle -N _change_branch
bindkey '^b' _change_branch

zle -N _delete_branch
bindkey '^k' _delete_branch

zle -N _open_project_folder
bindkey '^p' _open_project_folder

plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

export BAT_THEME=base16
export FZF_DEFAULT_OPTS='--color=fg:#f8f8f2,bg:#282a36,hl:#bd93f9 --color=fg+:#f8f8f2,bg+:#44475a,hl+:#bd93f9 --color=info:#ffb86c,prompt:#50fa7b,pointer:#ff79c6 --color=marker:#ff79c6,spinner:#ffb86c,header:#6272a4'
export ZSH="$HOME/.oh-my-zsh"

source $ZSH/oh-my-zsh.sh
source /usr/share/nvm/init-nvm.sh
