# Shell 설정 원칙

[README로 돌아가기](README.md)

## 1. 문서 목적

macOS 기본 Zsh와 terminal 환경의 구성 기준을 기록한다. 초기화하거나 재설치한 뒤에도 같은 원칙으로 환경을 다시 구성할 수 있게 한다.

설치 목록뿐 아니라 아래 정보도 보존한다.

- 각 설정을 선택한 이유
- `.zprofile`과 `.zshrc`에 두는 block의 역할
- 설정을 재현하고 검증하며 유지보수하는 방법

새로운 CLI, 개발 도구, runtime을 추가할 때 기존 환경을 불필요하게 복잡하게 만들지 않는 판단 기준도 함께 관리한다.

## 2. 기본 환경

| 항목 | 기준 |
| --- | --- |
| 운영체제 | macOS |
| architecture | Apple Silicon |
| 기본 shell | `/bin/zsh` |
| Homebrew prefix | `/opt/homebrew` |
| 독립 terminal | Warp |
| IDE terminal | VS Code 또는 IntelliJ의 내장 terminal |

shell과 Homebrew 상태는 다음 명령으로 확인한다.

```sh
echo "$SHELL"
command -v zsh
zsh --version
command -v brew
brew --prefix
```

기대 형태는 다음과 같다.

- `$SHELL`과 `command -v zsh`는 `/bin/zsh`를 출력한다.
- `zsh --version`은 `zsh <version> (...)` 형태를 출력한다.
- `command -v brew`는 `/opt/homebrew/bin/brew`를 출력한다.
- `brew --prefix`는 `/opt/homebrew`를 출력한다.

현재 terminal 종류는 다음 명령으로 확인한다.

```sh
echo "$TERM_PROGRAM"
```

Warp에서는 `WarpTerminal`이 출력된다. 다른 terminal에서는 해당 애플리케이션이 정한 값이 출력될 수 있다.

## 3. 전체 구성

```text
macOS
└── /bin/zsh
    ├── ~/.zprofile
    │   ├── Homebrew 환경
    │   └── installer가 관리하는 PATH
    └── ~/.zshrc
        ├── history
        ├── completion
        ├── Zsh 기본 옵션
        ├── Aliases
        ├── Zoxide
        └── terminal UI integration
```

## 4. 구성 원칙

### 4.1 macOS 기본 Zsh를 사용한다

[README의 적용 기준](README.md#적용-기준)은 기본 shell을 `/bin/zsh`로 정한다. 현재 구성에 필요한 history, completion, Zsh 옵션과 plugin 초기화는 별도의 Zsh 설치 없이 사용할 수 있다. Homebrew Zsh를 추가하면 shell 경로, `/etc/shells`, `chsh`, `PATH`, IDE별 shell 설정이 새로운 관리 대상이 된다.

명확한 기능 또는 version 요구가 생기기 전에는 macOS 기본 Zsh를 유지하고 다음 설치는 하지 않는다.

```sh
brew install zsh
```

### 4.2 shell framework는 사용하지 않는다

필요한 기능 수가 많지 않으므로 package를 직접 구성한다. 다음 framework는 현재 구성에 포함하지 않는다.

- Oh My Zsh
- Zinit
- Antidote
- Prezto
- Powerlevel10k

새로운 추상화 계층은 실제 필요성이 생겼을 때 추가한다.

### 4.3 `.zprofile`과 `.zshrc`의 역할을 분리한다

`~/.zprofile`은 로그인 shell에서 프로그램을 찾고 실행하기 위한 환경을 담당한다.

- Homebrew 환경
- 필수 `PATH`
- 로그인 시 필요한 환경 변수

`~/.zshrc`는 사람이 interactive shell을 사용할 때 필요한 기능을 담당한다.

- history
- completion
- alias
- Prompt
- Interactive CLI integration
- shell plugin

새 프로그램을 설치했다는 이유만으로 모든 설정을 `.zprofile`에 넣지 않는다.

### 4.4 Warp와 일반 terminal의 UI 기능을 분리한다

Warp에는 자체 Prompt와 Input Editor가 있고 IDE 내장 terminal과 일반 terminal에는 같은 기능이 없다. terminal 종류와 무관한 기능은 공통으로 적용하고 UI와 밀접한 기능만 Warp 밖에서 활성화한다.

| 공통 기능 | Warp 밖에서 활성화하는 UI 기능 |
| --- | --- |
| history | Starship Prompt |
| Zsh completion | fzf shell integration |
| Aliases | zsh-autosuggestions |
| Zoxide | zsh-syntax-highlighting |

분기 조건은 다음 한 곳에서 사용한다.

```zsh
if [[ "$TERM_PROGRAM" != "WarpTerminal" ]]; then
  # terminal UI integration
fi
```

### 4.5 설정 파일은 읽을 수 있고 제거에 안전한 상태를 유지한다

설정은 역할별 block으로 나눈다. [Zoxide 초기화](#zoxide)처럼 프로그램이 설치되어 있을 때만 초기화한다.

installer가 추가한 설정은 marker를 유지해 직접 관리하는 설정과 구분한다. marker 형식은 [일반형 예시](#installer가-관리하는-path)를 따른다. 프로그램을 삭제한 뒤에도 shell 전체가 오류를 내지 않도록 명령 또는 파일 존재 여부를 확인한다.

### 4.6 기본 Unix 명령은 가능한 한 덮어쓰지 않는다

`eza`, `bat`, `ripgrep` 같은 대체 CLI를 설치하더라도 기존 Unix 명령 이름을 바로 alias로 덮어쓰지 않는다.

```zsh
alias ls='eza'
alias cat='bat'
alias grep='rg'
```

기본 명령과 대체 명령을 구분하면 다른 Mac이나 Linux server에서도 같은 명령 습관을 유지할 수 있다. script와 interactive shell의 차이 및 문제 원인도 추적하기 쉽다.

### 4.7 alias는 실제 사용하는 것만 만든다

현재 구성에 필요한 최소 alias만 둔다.

```zsh
alias ll='ls -alh'
alias ..='cd ..'
alias ...='cd ../..'
```

Git alias처럼 아직 반복 사용하지 않는 항목은 미리 추가하지 않는다. 같은 명령을 반복해서 입력하면서 실제 불편함이 생겼을 때 추가한다.

## 5. 설정 방법

### 5.1 기본 환경 확인

[기본 환경](#2-기본-환경)의 확인 명령을 실행하고 `/bin/zsh`와 `/opt/homebrew`가 기준에 맞는지 확인한다. Homebrew가 없다면 [Homebrew 공식 사이트](https://brew.sh/)의 현재 설치 절차를 확인한다.

### 5.2 shell 관련 package 준비

이 구성은 다음 Homebrew package를 사용한다.

| package | 역할 |
| --- | --- |
| `starship` | Warp가 아닌 terminal의 prompt |
| `zoxide` | 사용 기록 기반 디렉토리 이동 |
| `fzf` | Fuzzy finder |
| `zsh-autosuggestions` | history 기반 명령 제안 |
| `zsh-syntax-highlighting` | 입력 중인 명령 syntax highlighting |

```sh
brew install starship zoxide fzf zsh-autosuggestions zsh-syntax-highlighting
```

### 5.3 `.zprofile` block 구성

`.zprofile`에는 로그인할 때 필요한 환경 block만 둔다.

#### Homebrew 환경

Apple Silicon Homebrew 환경을 적용한다.

```zsh
eval "$(/opt/homebrew/bin/brew shellenv zsh)"
```

#### installer가 관리하는 PATH

installer가 `PATH` block을 추가했다면 시작과 끝 marker를 함께 유지해 관리 주체를 드러낸다. 설치 방식에 따라 내용이 달라질 수 있다. 다른 기기의 block을 그대로 복사하지 말고 해당 installer가 추가한 값과 프로그램의 실제 실행 경로를 확인한다.

```zsh
# >>> Tool installer >>>
# <<< Tool installer <<<
```

```sh
command -v <installed-command>
```

### 5.4 `.zshrc` block 구성

`.zshrc`는 block 단위로 목적과 필요한 최소 설정을 관리한다. 실제 파일에서는 같은 순서로 block을 구분한다.

#### history

History는 `~/.zsh_history`에 저장하고 최대 10,000개를 유지한다.

```zsh
HISTFILE="$HOME/.zsh_history"
HISTSIZE=10000
SAVEHIST=10000

setopt APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
```

| 옵션 | 역할 |
| --- | --- |
| `APPEND_HISTORY` | 기존 history를 덮어쓰지 않고 추가한다. |
| `SHARE_HISTORY` | 여러 shell session이 history를 공유한다. |
| `HIST_IGNORE_DUPS` | 연속된 중복 history를 줄인다. |
| `HIST_IGNORE_SPACE` | 공백으로 시작하는 명령을 history에서 제외한다. |

`HIST_IGNORE_SPACE`를 보안 기능으로 의존하지 않는다. Password, token, API key는 가능한 한 CLI argument로 직접 입력하지 않는다.

#### completion

Zsh completion을 활성화하고 후보 선택과 대소문자 matching 방식을 지정한다.

```zsh
autoload -Uz compinit
compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
```

#### Zsh 기본 옵션

```zsh
setopt AUTO_CD
setopt INTERACTIVE_COMMENTS
```

`AUTO_CD`는 `cd` 없이 디렉토리 이름만 입력해 이동할 수 있게 한다. `INTERACTIVE_COMMENTS`는 interactive shell에서 `#` 주석을 사용할 수 있게 한다.

#### aliases

alias block에는 [실제로 사용하는 최소 alias](#47-alias는-실제-사용하는-것만-만든다)만 둔다. 기본 명령을 대체하는 alias는 [기본 Unix 명령 원칙](#46-기본-unix-명령은-가능한-한-덮어쓰지-않는다)을 따른다.

#### Zoxide

설치 여부를 확인한 뒤 공통 기능으로 초기화한다.

```zsh
if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init zsh)"
fi
```

#### terminal UI integration

다음 package 초기화 조각은 모두 [Warp와 일반 terminal의 UI 기능 분리](#44-warp와-일반-terminal의-ui-기능을-분리한다) 조건 안에 둔다.

##### fzf

fzf는 command가 있을 때 shell integration을 활성화한다.

```zsh
if command -v fzf >/dev/null 2>&1; then
  source <(fzf --zsh)
fi
```

##### zsh-autosuggestions

zsh-autosuggestions는 Homebrew가 설치한 파일이 있을 때 불러온다.

```zsh
if [[ -f "$(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]]; then
  source "$(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi
```

##### Starship

Starship은 command가 있을 때 prompt를 초기화한다.

```zsh
if command -v starship >/dev/null 2>&1; then
  eval "$(starship init zsh)"
fi
```

##### zsh-syntax-highlighting

zsh-syntax-highlighting은 다른 widget 설정을 감쌀 수 있으므로 UI integration block의 마지막에 둔다.

```zsh
if [[ -f "$(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
  source "$(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi
```

### 5.5 설정 적용

설정 파일을 저장한 뒤 [설정 문법 검증](#62-설정-문법)을 수행한다. 문제가 없으면 현재 interactive shell에 적용한다.

```sh
source ~/.zshrc
```

마지막으로 새 terminal session을 열어 로그인 환경과 interactive 환경을 함께 확인한다.

## 6. 검증

### 6.1 shell과 Homebrew

[기본 환경](#2-기본-환경)의 확인 명령을 다시 실행하고 기대 형태와 일치하는지 확인한다.

### 6.2 설정 문법

```sh
zsh -n ~/.zshrc
```

다음을 확인한다.

- 정상이면 아무것도 출력되지 않는다.
- 설정을 바꾼 뒤에는 현재 session뿐 아니라 새 terminal session에서도 문제가 없다.

문법 오류나 새 terminal session의 문제가 있으면 [설정 변경과 백업](#73-설정-변경과-백업)에 따라 최근 변경한 block부터 확인한다.

### 6.3 관련 CLI

```sh
brew list --versions starship zoxide fzf zsh-autosuggestions zsh-syntax-highlighting
command -v starship
command -v zoxide
command -v fzf
```

다음을 확인한다.

- 각 package의 version이 출력된다.
- `starship`, `zoxide`, `fzf`의 실행 경로가 출력된다.

package 또는 실행 경로가 확인되지 않으면 [shell 관련 package 준비](#52-shell-관련-package-준비) 절차를 따른다.

### 6.4 terminal별 동작

```sh
echo "$TERM_PROGRAM"
```

다음을 확인한다.

- Warp에서는 `WarpTerminal`이 출력된다.
- 각 환경에서 [Warp와 일반 terminal의 UI 기능 분리 표](#44-warp와-일반-terminal의-ui-기능을-분리한다)에 해당하는 기능이 활성화된다.

terminal UI 기능이 기준과 다르면 [`.zshrc` block 구성](#54-zshrc-block-구성)을 따른다.

## 7. 이후 사용 및 유지보수

### 7.1 shell 구성이 필요한 도구의 추가 판단

설치 전후의 공통 판단과 관리 주체 선택은 [소프트웨어 설치 원칙](software-installation.md)을 따른다. shell 구성이 필요한 도구에는 다음 판단을 추가한다.

1. 환경 또는 `PATH`는 `.zprofile`, interactive 기능은 `.zshrc`에 둔다는 [역할 분리 원칙](#43-zprofile과-zshrc의-역할을-분리한다)을 적용한다.
2. 단일 기능 때문에 framework 전체가 필요한지 [shell framework를 사용하지 않는 원칙](#42-shell-framework는-사용하지-않는다)으로 판단한다.

### 7.2 Homebrew package 관리

shell 관련 CLI에는 [소프트웨어 설치 원칙](software-installation.md)의 단일 관리 주체 기준을 적용하고 Homebrew를 관리 주체로 사용한다.

### 7.3 설정 변경과 백업

중요한 변경 전에는 대상 파일의 backup을 만들 수 있다.

```sh
cp ~/.zshrc ~/.zshrc.backup
cp ~/.zprofile ~/.zprofile.backup
```

`.backup`, `.old`, `.bak` 파일을 계속 누적하지 않는다. 변경 후에는 [설정 문법 검증](#62-설정-문법)과 [terminal별 동작 검증](#64-terminal별-동작)을 수행한다. 문제가 생기면 최근 변경한 block부터 확인한다.

검증이 완료되면 해당 backup 파일을 삭제한다.

### 7.4 의도적으로 사용하지 않는 항목

- Homebrew Zsh를 사용하지 않는 근거는 [macOS 기본 Zsh 사용 원칙](#41-macos-기본-zsh를-사용한다)에서 관리한다.
- shell framework를 사용하지 않는 근거는 [shell framework를 사용하지 않는 원칙](#42-shell-framework는-사용하지-않는다)에서 관리한다.
- 기본 명령을 alias로 대체하지 않는 근거는 [기본 Unix 명령 원칙](#46-기본-unix-명령은-가능한-한-덮어쓰지-않는다)에서 관리한다.

### 7.5 유지보수 기준

- 사용하지 않는 plugin은 제거한다.
- 의미를 모르는 설정은 추가하지 않는다.
- 외부 dotfiles를 통째로 복사하지 않는다.
- installer가 추가한 설정과 직접 추가한 설정을 구분한다.
- 새로운 도구를 추가하기 전 [소프트웨어 설치 원칙의 판단 순서](software-installation.md#51-설치-전-판단-순서)와 [shell 구성이 필요한 도구의 추가 판단](#71-shell-구성이-필요한-도구의-추가-판단)을 따른다.
- 설정 변경 후 [검증](#6-검증)을 반복한다.

## 8. 현재 범위 밖의 항목

- 현재 머신의 전체 설치 애플리케이션과 CLI 목록: 이 문서는 shell 구성이 의존하는 package만 설명한다.
- 실제 `.zprofile`과 `.zshrc` 전문 및 머신별 override: dotfiles 원본은 README가 정한 현재 범위 밖이다.
- dotfiles manager와 Git 저장소 배포: 실제로 반복 배포할 필요가 생기기 전에는 도입하지 않는다.
- 자동 bootstrap과 `$HOME` 배포: 자동화보다 수동 절차와 안전 조건을 먼저 관리한다.
- Warp와 IDE 자체 설정: 이 문서는 shell에서 기능을 분리하는 기준만 다루고 애플리케이션 내부 설정은 다루지 않는다.
- 향후 설치 후보 CLI 목록: 필요성이 확인되지 않은 도구를 관리 목록으로 만들지 않는다.
- Git과 GitHub SSH 설정: shell 파일을 변경하지 않는 별도 책임이며 [Git과 GitHub SSH 설정 원칙](git-and-ssh.md)에서 관리한다.

## 9. 핵심 요약

```text
shell
└── macOS 기본 /bin/zsh

package manager
└── Homebrew (/opt/homebrew)

Environment
└── ~/.zprofile
    ├── Homebrew 환경
    └── installer가 관리하는 PATH

interactive Zsh
└── ~/.zshrc
    ├── history
    ├── completion
    ├── Zsh 기본 옵션
    ├── 최소한의 aliases
    └── Zoxide

Warp
├── Warp Prompt
└── Warp Input Editor

Warp가 아닌 terminal
├── Starship
├── fzf
├── zsh-autosuggestions
└── zsh-syntax-highlighting
```

- [macOS 기본 Zsh를 사용한다](#41-macos-기본-zsh를-사용한다)
- [shell framework는 사용하지 않는다](#42-shell-framework는-사용하지-않는다)
- [`.zprofile`과 `.zshrc`의 역할을 분리한다](#43-zprofile과-zshrc의-역할을-분리한다)
- [Warp와 일반 terminal의 UI 기능을 분리한다](#44-warp와-일반-terminal의-ui-기능을-분리한다)
- [설정 파일은 읽을 수 있고 제거에 안전한 상태를 유지한다](#45-설정-파일은-읽을-수-있고-제거에-안전한-상태를-유지한다)
- [기본 Unix 명령은 가능한 한 덮어쓰지 않는다](#46-기본-unix-명령은-가능한-한-덮어쓰지-않는다)
- [alias는 실제 사용하는 것만 만든다](#47-alias는-실제-사용하는-것만-만든다)
