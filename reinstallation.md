# 재설치 원칙

[README로 돌아가기](README.md)

## 1. 문서 목적

Mac을 초기화하거나 새 Apple Silicon Mac을 사용할 때 이 저장소의 원칙을 안전한 순서로 다시 적용하는 체크리스트를 정리한다.

이 문서는 macOS 초기화 방법이나 모든 설정 값을 직접 소유하지 않는다. 초기화해도 되는 상태인지 먼저 확인한다. 초기화가 끝난 Mac에서는 각 기준 문서를 적용할 순서와 다음 단계로 넘어갈 시점을 관리한다.

재설치에서는 아래 원칙을 지킨다.

- 복구할 수 없는 data가 남은 상태에서 초기화를 시작하지 않는다.
- 설치와 설정의 의존 순서를 지킨다.
- 같은 도구를 여러 관리 주체로 중복 설치하지 않는다.
- 프로젝트의 version·dependency 선언으로 개발환경을 복구한다.
- 각 단계의 완료 조건을 확인한 뒤 다음 단계로 이동한다.
- 추측이 위험한 상황은 중단 조건으로 명시한다.

## 2. 적용 범위와 중단 원칙

### 2.1 포함하는 범위

- 초기화 전 data와 계정 복구 가능성 확인
- 초기화 후 macOS와 Apple Silicon 기본 상태 확인
- Xcode Command Line Tools와 Homebrew 준비
- 기본 디렉토리 구성
- 필요한 CLI와 GUI 애플리케이션 설치
- shell, Git과 GitHub SSH 구성
- Java, Node.js, Python과 OrbStack 구성
- Git 저장소 clone과 프로젝트별 환경 복구
- 전체 검증과 이전 인증정보 정리

### 2.2 포함하지 않는 범위

- macOS를 삭제하거나 초기화하는 실제 조작법
- Time Machine, iCloud와 외부 저장소의 백업 체계 설계
- 개인 계정, license와 설치 프로그램 inventory
- 실제 dotfiles와 IDE 설정 원본의 자동 복원
- package 설치와 시스템 설정을 실행하는 bootstrap script
- container volume의 자동 backup, 복원 또는 삭제

### 2.3 확인할 수 없으면 진행하지 않는다

다음 단계의 완료 조건을 확인하지 못하면 명령을 추측해 실행하지 않는다. 특히 다음 상황에서는 현재 단계를 중단하고 공식 문서와 기존 상태를 다시 확인한다.

- 대체할 수 없는 data의 backup을 실제로 열어보지 못했다.
- 계정 로그인 또는 복구 수단에 다른 기기에서 접근할 수 없다.
- 같은 command가 둘 이상의 관리 주체에서 제공된다.
- 예상과 다른 architecture 또는 Homebrew prefix가 확인된다.
- SSH host key를 신뢰할 근거가 없다.
- Volume 삭제처럼 data 손실 가능성이 있는 작업이 필요하다.

## 3. 전체 재구성 순서

```text
0. 초기화 전 안전 확인
        ↓
1. macOS·Apple Silicon 확인
        ↓
2. Xcode Command Line Tools·Homebrew
        ↓
3. 기본 디렉토리
        ↓
4. CLI·GUI 애플리케이션
        ↓
5. shell
        ↓
6. Git·새 GitHub SSH key
        ↓
7. SDKMAN·fnm·uv·OrbStack
        ↓
8. 프로젝트 clone과 프로젝트별 복구
        ↓
9. 통합 검증
        ↓
10. 이전 인증정보와 임시 파일 정리
```

단계별 책임은 다음과 같다.

| 단계 | 기준 문서 | 완료 결과 |
| --- | --- | --- |
| 초기화 전 확인 | 이 문서 | data와 계정의 복구 가능성을 확인함 |
| 디렉토리 | [디렉토리 관리 원칙](directory-management.md) | 안정적인 기본 경로가 존재함 |
| 소프트웨어 | [소프트웨어 설치 원칙](software-installation.md) | 각 도구의 관리 주체가 하나임 |
| shell | [Shell 설정 원칙](shell-configuration.md) | 새 Zsh가 오류 없이 시작됨 |
| GitHub 연결 | [Git과 GitHub SSH 설정 원칙](git-and-ssh.md) | SSH 인증과 저장소 접근이 동작함 |
| 개발환경 | [개발환경 구성 원칙](development-environment.md) | runtime과 OrbStack이 동작함 |
| 프로젝트 | 각 프로젝트의 README와 선언 파일 | build, test 또는 실행 검증이 통과함 |

이 문서는 기준 문서의 상세 설정을 복사하지 않는다. 설정 방법이 바뀌면 해당 기준 문서 한 곳을 수정하고 이 문서에서는 순서와 링크만 유지한다.

## 4. 초기화 전 확인

초기화로 잃을 수 있는 data와 접근 수단을 식별하고 실제 복구 가능성을 확인한다.

완료 조건:

- 대체할 수 없는 data와 Git 작업의 backup을 검증했다.
- 필요한 계정과 license에 다시 접근할 수 있다.
- 새 GitHub SSH key를 등록할 수 있다.

중단 조건:

- backup의 존재만 확인했고 대표 파일을 실제로 열어보지 못했다.
- push하지 않은 commit, untracked 파일 또는 local container data의 보존 여부가 불명확하다.
- 계정의 로그인이나 2FA 복구 수단을 검증하지 못했다.

### 4.1 대체할 수 없는 data 확인

확인 항목:

- [ ] 문서, 사진, 영상과 개인 기록 중 원본이 이 Mac에만 있는 항목을 확인한다.
- [ ] Git remote에 push하지 않은 commit이 있는지 확인한다.
- [ ] Git에 포함되지 않은 source, 설정과 작업 파일을 확인한다.
- [ ] 애플리케이션 전용 library와 프로젝트 data를 확인한다.
- [ ] local container volume과 database 중 보존해야 할 data를 확인한다.
- [ ] backup의 파일 목록만 보지 않고 대표 파일을 실제로 열어본다.

각 Git 저장소에서 다음 상태를 확인한다.

```sh
git status --short
git branch --show-current
git log --oneline --decorate -5
git remote -v
```

untracked 파일, push하지 않은 commit 또는 remote가 없는 branch는 자동으로 복구된다고 가정하지 않는다.

### 4.2 계정과 인증 복구 가능성 확인

확인 항목:

- [ ] Apple Account에 로그인할 수 있다.
- [ ] GitHub에 로그인하고 SSH key를 등록할 수 있다.
- [ ] 필요한 계정의 2FA와 복구 수단에 다른 기기에서 접근할 수 있다.
- [ ] 유료 애플리케이션의 license 또는 구매 이력을 다시 확인할 수 있다.
- [ ] 초기화 후 필요한 공식 installer를 다시 받을 수 있다.

password, token, 복구 코드와 private key를 이 저장소에 기록해 확인 항목을 충족하지 않는다.

### 4.3 SSH key 처리 방침 확인

현재 [Git과 GitHub SSH 설정 원칙](git-and-ssh.md)은 private key를 이 Mac에만 보관한다. 초기화 후에는 새 Ed25519 key를 생성하고 GitHub에 새 public key를 등록한다.

확인 항목:

- [ ] 초기화 후 새 key를 등록할 GitHub 접근 수단이 있다.
- [ ] 기존 GitHub SSH key의 title을 식별할 수 있다.
- [ ] 새 key 검증 전에는 기존 public key 등록을 제거하지 않는다.

### 4.4 초기화 진행 조건

다음 조건을 모두 만족할 때만 macOS 초기화 단계로 이동한다.

확인 항목:

- [ ] 대체할 수 없는 data의 backup과 복구 가능성을 확인했다.
- [ ] 모든 필요한 계정에 다시 로그인할 수 있다.
- [ ] 보존해야 할 Git 작업과 container data를 별도로 확보했다.
- [ ] 초기화 후 새 GitHub SSH key를 등록할 수 있다.
- [ ] Mac이 전원과 안정적인 network에 연결되어 있다.

하나라도 확인하지 못했다면 초기화를 진행하지 않는다.

## 5. macOS 기본 상태 확인

macOS 초기화와 초기 사용자 생성은 Apple의 현재 공식 절차를 따른다. 초기 설정이 끝난 뒤 다음 상태부터 이 문서를 적용한다.

이후 문서가 전제로 삼는 운영체제, architecture, 사용자 홈과 shell을 확인한다.

완료 조건:

- macOS 업데이트 확인을 마쳤다.
- `arm64`, `/Users/<username>`, `/bin/zsh` 기준과 일치한다.

중단 조건:

- architecture, 사용자 홈 또는 기본 shell이 기준과 다르다.
- 중요 보안 update나 재시작이 완료되지 않았다.

### 5.1 운영체제와 architecture

```sh
sw_vers
uname -m
printf '%s\n' "$HOME"
echo "$SHELL"
```

확인 항목:

- [ ] macOS version이 출력된다.
- [ ] architecture가 `arm64`다.
- [ ] `$HOME`이 `/Users/<username>` 형태다.
- [ ] 기본 shell이 `/bin/zsh`다.

중단 조건:

- `uname -m`이 `arm64`가 아니다.
- `$HOME`이 예상하지 않은 계정이나 volume을 가리킨다.
- 관리 대상과 다른 macOS 또는 shell 구성이 필요하다.

### 5.2 macOS 업데이트

확인 항목:

- [ ] System Settings에서 사용 가능한 중요 보안 및 macOS update를 확인한다.
- [ ] 업데이트가 재시작을 요구하면 개발 도구 설치 전에 완료한다.
- [ ] 업데이트 후 [운영체제와 architecture 확인](#51-운영체제와-architecture)을 반복한다.

이 문서에 특정 macOS patch version을 고정하지 않는다.

## 6. 개발 기반 준비

macOS 기본 개발 도구와 Apple Silicon Homebrew를 다른 개발 도구보다 먼저 준비한다.

완료 조건:

- Xcode Command Line Tools, macOS 기본 Git과 OpenSSH가 실행된다.
- Homebrew가 `/opt/homebrew`에서 실행된다.

중단 조건:

- Xcode Command Line Tools 설치가 완료되지 않거나 license·network 오류가 발생한다.
- `/usr/local`의 Intel Homebrew와 `/opt/homebrew`의 Apple Silicon Homebrew가 함께 확인된다.
- 어떤 `git`, `ssh` 또는 `brew`가 실행되는지 설명할 수 없다.

### 6.1 Xcode Command Line Tools

상태를 확인한다.

```sh
xcode-select -p
git --version
```

설치되어 있지 않다면 macOS가 제공하는 설치 절차를 시작한다.

```sh
xcode-select --install
```

설치 UI와 option은 macOS version에 따라 달라질 수 있다. 완료 후 다시 확인한다.

```sh
xcode-select -p
git --version
ssh -V
```

확인 항목:

- [ ] Xcode Command Line Tools 경로가 출력된다.
- [ ] macOS 기본 Git과 OpenSSH가 실행된다.

### 6.2 Homebrew

[Homebrew 공식 사이트](https://brew.sh/)의 현재 설치 절차를 확인하고 [소프트웨어 설치 원칙](software-installation.md)의 원격 script 검토 기준을 적용한다.

설치 후 확인한다.

```sh
command -v brew
brew --prefix
brew doctor
```

확인 항목:

- [ ] `command -v brew`가 `/opt/homebrew/bin/brew` 형태를 출력한다.
- [ ] `brew --prefix`가 `/opt/homebrew`를 출력한다.
- [ ] `brew doctor`의 warning을 읽고 현재 구성에 영향을 주는 항목을 확인했다.

중단 조건:

- Intel Homebrew 경로인 `/usr/local`과 Apple Silicon Homebrew가 함께 확인된다.
- 기존 package manager 흔적 때문에 어떤 `brew`가 실행되는지 설명할 수 없다.

## 7. 기본 디렉토리 구성

data와 프로젝트를 복원하기 전에 장기적으로 사용할 안정적인 목적지를 먼저 만든다.

완료 조건:

- [디렉토리 관리 원칙](directory-management.md)의 안정적인 기본 경로가 존재한다.
- Screenshot 앱의 실제 저장 위치가 `~/Pictures/screenshots`다.
- macOS와 애플리케이션이 관리하는 기존 경로를 임의로 이동하지 않았다.

중단 조건:

- 생성하려는 경로와 같은 이름의 파일 또는 symlink가 이미 존재한다.
- backup 복원이 기존 디렉토리를 덮어쓰거나 애플리케이션 library를 임의로 이동해야 한다.
- Screenshot test가 Desktop에 저장되어 지정한 Inbox 구성이 적용되지 않았다.

[디렉토리 관리 원칙의 기본 디렉토리 생성](directory-management.md#8-설정-방법) 절차를 적용한다.

확인 항목:

- [ ] `~/01-personal`이 존재한다.
- [ ] `~/02-work/01-development`가 존재한다.
- [ ] `~/02-work/02-study`와 `~/02-work/03-career`가 존재한다.
- [ ] `~/03-reference`의 기본 하위 경로가 존재한다.
- [ ] `~/04-quickshare`와 필요한 `99-archive`가 존재한다.
- [ ] `~/Pictures/screenshots`가 존재한다.
- [ ] `Shift-Command-5` → `Options`에서 screenshot 저장 위치를 `~/Pictures/screenshots`로 지정했다.
- [ ] test screenshot이 해당 경로에 저장되고 Desktop에는 생성되지 않는다.
- [ ] `Desktop`을 장기 보관 위치로 사용하지 않는다.

기존 data를 복원할 때는 최상위 디렉토리를 한꺼번에 덮어쓰지 않는다. backup의 항목은 용도에 따라 확인한다. macOS 또는 애플리케이션이 관리하는 경로는 해당 애플리케이션의 복원 절차를 따른다.

## 8. 소프트웨어와 shell 구성

필요한 프로그램을 관리 주체 하나로 설치한다. 새 Zsh에서는 설치된 도구를 오류 없이 찾을 수 있어야 한다.

완료 조건:

- 필요한 CLI와 GUI 애플리케이션만 선택한 관리 주체로 설치했다.
- 같은 command의 중복 설치가 없다.
- `.zprofile`과 `.zshrc` 문법 검증 및 새 login shell 시작이 성공한다.

중단 조건:

- 기존 installer, Homebrew 또는 다른 manager 중 어떤 주체가 program을 관리하는지 알 수 없다.
- `type -a`에서 의도하지 않은 중복 실행 경로가 확인된다.
- 새 login shell이 오류를 출력하거나 Homebrew 경로를 잃는다.

### 8.1 설치 순서

다음 순서로 설치 주체를 확인하고 필요한 항목만 설치한다.

1. Homebrew formula로 관리할 CLI와 개발 구성 요소
2. 개발사가 제공하는 GUI 애플리케이션
3. 언어별 manager가 관리할 runtime
4. 프로젝트가 관리할 dependency

GUI 애플리케이션과 CLI의 실제 설치 목록은 이 저장소에서 inventory로 관리하지 않는다. [소프트웨어 설치 원칙](software-installation.md)의 선택 기준을 적용하고 각 책임 문서에서 선택한 도구만 설치한다.

### 8.2 기본 개발 CLI

[개발환경 구성 원칙의 공통 CLI](development-environment.md#51-공통-cli와-설치-경계)를 적용한다.

```sh
brew install jq ripgrep fd fnm uv
```

[Shell 설정 원칙](shell-configuration.md)에 필요한 package도 해당 문서의 절차로 설치한다.

중복을 확인한다.

```sh
type -a jq
type -a rg
type -a fd
type -a fnm
type -a uv
```

### 8.3 GUI 애플리케이션

[소프트웨어 설치 원칙](software-installation.md)의 GUI 우선순위에 따라 필요한 애플리케이션을 공식 배포 경로로 설치한다.

개발환경의 역할이 확정된 GUI는 다음과 같다.

| 애플리케이션 | 역할 |
| --- | --- |
| OrbStack | Docker runtime |
| IntelliJ IDEA | Spring Boot와 Java 개발 |
| VS Code | React와 Python 개발 |
| Warp | 독립 terminal |

현재 필요하지 않은 애플리케이션을 과거 설치 이력만으로 다시 설치하지 않는다.

### 8.4 shell

[Shell 설정 원칙](shell-configuration.md)의 순서로 `~/.zprofile`과 `~/.zshrc`를 수동 구성한다. 실제 dotfiles 원본을 저장소에서 복사하지 않는다.

설정 후 문법과 새 login shell을 확인한다.

```sh
zsh -n ~/.zprofile
zsh -n ~/.zshrc
exec zsh -l
```

새 shell에서 다음을 확인한다.

```sh
command -v brew
brew --prefix
echo "$PATH"
```

확인 항목:

- [ ] Zsh 문법 오류가 없다.
- [ ] 새 login shell이 오류 메시지 없이 시작된다.
- [ ] Homebrew가 `/opt/homebrew`에서 실행된다.
- [ ] 삭제되거나 설치되지 않은 명령 때문에 shell 전체가 실패하지 않는다.

## 9. Git과 GitHub SSH 구성

commit author 정보와 GitHub 인증을 분리하고 새 Mac 전용 SSH key로 저장소 접근을 복구한다.

완료 조건:

- Git 사용자 정보가 의도한 값으로 설정되어 있다.
- 새 Ed25519 public key만 GitHub에 등록했다.
- `ssh -T git@github.com`과 SSH 저장소 접근이 성공한다.

중단 조건:

- 같은 이름의 기존 key가 있는데 용도를 식별할 수 없다.
- private key 또는 `~/.ssh/config`의 권한이 기준과 다르다.
- GitHub host key fingerprint를 공식 정보와 비교할 수 없다.
- 새 key 검증 전에 이전 public key를 제거해야 하는 상황이다.

[Git과 GitHub SSH 설정 원칙](git-and-ssh.md)을 처음부터 적용한다.

### 9.1 Git 사용자 정보 설정

확인 항목:

- [ ] `git config --global user.name`을 설정했다.
- [ ] `git config --global user.email`을 설정했다.
- [ ] commit author 정보와 GitHub 인증을 서로 다른 책임으로 이해하고 있다.

확인한다.

```sh
git config --global user.name
git config --global user.email
```

### 9.2 새 SSH key

확인 항목:

- [ ] 새 Ed25519 key를 생성했다.
- [ ] private key와 `~/.ssh/config` 권한을 제한했다.
- [ ] public key만 GitHub에 등록했다.
- [ ] `~/.ssh/config`에서 사용할 key를 명시했다.

key 생성과 파일 내용은 [Git과 GitHub SSH 설정 원칙](git-and-ssh.md#54-ssh-key-생성)의 명령을 따른다. 기존 private key가 backup에 있다는 이유만으로 용도와 보안을 확인하지 않고 덮어쓰지 않는다.

### 9.3 GitHub 연결 검증

```sh
ssh -T git@github.com
```

처음 연결할 때 표시되는 host key는 GitHub 공식 문서의 현재 fingerprint와 비교한다. 일치 여부를 확인할 수 없다면 연결을 승인하지 않는다.

확인 항목:

- [ ] GitHub가 새 key로 계정을 식별한다.
- [ ] SSH config와 key 권한 검증이 통과한다.
- [ ] test 저장소를 SSH URL로 clone하거나 기존 remote를 조회할 수 있다.

새 key 검증이 끝나기 전에는 GitHub의 이전 public key 등록을 제거하지 않는다.

## 10. 개발환경 구성

언어별 manager와 OrbStack을 각각 단일 관리 주체로 구성하고 프로젝트 복구에 필요한 runtime을 준비한다.

완료 조건:

- Temurin 25와 Node.js 24가 프로젝트 밖의 기본 version이다.
- Temurin 21과 Node.js 22를 호환 프로젝트에서 선택할 수 있다.
- uv와 OrbStack Docker context가 동작한다.
- 전역 Gradle, pyenv, Docker Desktop과 중복 Docker CLI를 추가하지 않았다.

중단 조건:

- 공식 지원 상태나 현재 candidate 식별자를 확인할 수 없다.
- Java, Node.js, Python 또는 Docker CLI가 둘 이상의 manager에서 제공된다.
- shell 초기화 오류 때문에 프로젝트 version 전환이 동작하지 않는다.
- Docker context가 `orbstack`이 아니거나 Client와 Server가 연결되지 않는다.

[개발환경 구성 원칙](development-environment.md)의 관리 주체와 version 기준을 적용한다.

### 10.1 Java와 Spring Boot

확인 항목:

- [ ] SDKMAN을 공식 절차로 설치했다.
- [ ] 현재 Temurin 25 candidate를 기본으로 설치했다.
- [ ] 현재 Temurin 21 candidate를 호환용으로 설치했다.
- [ ] Gradle을 전역 설치하지 않았다.

```sh
sdk version
sdk current java
java --version
type -a java
```

### 10.2 Node.js와 React

확인 항목:

- [ ] fnm으로 Node.js 24를 기본으로 설치했다.
- [ ] fnm으로 Node.js 22를 호환용으로 설치했다.
- [ ] fnm 초기화 block을 `.zshrc`에 추가했다.
- [ ] Homebrew `node` formula를 중복 설치하지 않았다.

```sh
fnm --version
fnm current
node --version
type -a node
```

### 10.3 Python

확인 항목:

- [ ] uv가 실행된다.
- [ ] pyenv를 추가하지 않았다.
- [ ] 프로젝트가 요구하기 전에 임의의 전역 Python version과 dependency를 설치하지 않았다.

```sh
uv --version
uv python list
```

### 10.4 OrbStack

확인 항목:

- [ ] OrbStack을 공식 macOS 애플리케이션으로 설치하고 시작했다.
- [ ] Docker Desktop과 Homebrew Docker CLI를 중복 설치하지 않았다.
- [ ] Docker context가 `orbstack`이다.

```sh
docker context show
docker version
docker compose version
type -a docker
```

## 11. 프로젝트 복구

필요한 저장소만 clone한다. 각 프로젝트는 version control에 기록한 선언을 기준으로 runtime, dependency와 local service를 재생성한다.

완료 조건:

- 필요한 repository를 SSH URL로 clone했다.
- 프로젝트 version 선언과 실제 runtime이 일치한다.
- Lockfile, wrapper와 `compose.yaml`을 기준으로 대표 build·test·service 검증이 통과한다.

중단 조건:

- 프로젝트 선언 파일이 없거나 서로 충돌해 필요한 version과 package manager를 판단할 수 없다.
- Global tool을 임의로 설치해야만 build가 진행되는 상태다.
- Lockfile을 무시하거나 새로 생성해야 하는데 변경 이유를 확인할 수 없다.
- container volume 삭제 또는 database migration이 필요하지만 backup과 프로젝트 절차가 없다.

### 11.1 SSH URL로 clone

필요한 저장소만 `~/02-work/01-development` 아래에 clone한다.

```sh
cd ~/02-work/01-development
git clone git@github.com:<owner>/<repository>.git
```

모든 과거 저장소를 일괄 clone하지 않는다. 현재 사용하는 저장소부터 복구하고 나머지는 필요할 때 가져온다.

### 11.2 프로젝트 선언 확인

clone한 뒤 실행 명령보다 먼저 version과 dependency 선언을 확인한다.

```text
Java
├── .sdkmanrc
├── gradlew
└── gradle/wrapper

Node.js
├── .node-version
├── package.json
└── 하나의 lockfile

Python
├── .python-version
├── pyproject.toml
└── uv.lock

container
└── compose.yaml
```

선언 파일이 없다면 임의의 global tool로 우회하지 않고 프로젝트 README와 이력을 확인한다.

### 11.3 Spring Boot 프로젝트

```sh
sdk env
./gradlew build
```

확인 항목:

- [ ] `.sdkmanrc`가 지정한 Java가 사용된다.
- [ ] Gradle Wrapper가 실행된다.
- [ ] 프로젝트 build와 test가 통과한다.

### 11.4 React 프로젝트

프로젝트에 진입한 뒤 fnm 전환을 확인한다.

```sh
fnm current
node --version
```

그다음 프로젝트가 이미 선택한 package manager와 lockfile에 맞는 설치 명령을 사용한다. `npm`, `pnpm`, `yarn` 중 하나를 이 문서가 임의로 선택하지 않는다.

확인 항목:

- [ ] `.node-version`과 실행 중인 Node.js version이 일치한다.
- [ ] 하나의 lockfile을 기준으로 dependency가 설치된다.
- [ ] 프로젝트가 정의한 build 또는 test script가 통과한다.

### 11.5 Python 프로젝트

```sh
uv sync
uv run python --version
```

확인 항목:

- [ ] 프로젝트가 요구하는 Python이 선택된다.
- [ ] `uv.lock`을 기준으로 `.venv`가 재생성된다.
- [ ] 프로젝트의 test 또는 대표 실행 명령이 통과한다.

### 11.6 Compose 프로젝트

```sh
docker compose config
docker compose up -d
docker compose ps
```

확인 항목:

- [ ] `compose.yaml`이 오류 없이 해석된다.
- [ ] 필요한 service가 정상 상태다.
- [ ] 애플리케이션이 local service에 연결된다.

검증 후 프로젝트 절차에 따라 종료한다.

```sh
docker compose down
```

Volume을 삭제하는 option은 일반 복구와 종료 절차에 포함하지 않는다.

## 12. 전체 검증

### 12.1 기본 환경

```sh
uname -m
echo "$SHELL"
command -v brew
brew --prefix
git --version
ssh -V
```

확인 항목:

- [ ] `arm64`, `/bin/zsh`, `/opt/homebrew` 기준과 일치한다.
- [ ] Git과 SSH가 실행된다.

### 12.2 디렉토리와 shell

```sh
test -d ~/02-work/01-development
zsh -n ~/.zprofile
zsh -n ~/.zshrc
```

확인 항목:

- [ ] 기본 프로젝트 경로가 존재한다.
- [ ] shell 설정의 문법 오류가 없다.
- [ ] 새 Warp와 IDE terminal에서 필요한 command가 같은 관리 주체로 실행된다.

### 12.3 GitHub

```sh
ssh -T git@github.com
```

확인 항목:

- [ ] 새 SSH key로 GitHub 인증이 동작한다.
- [ ] clone한 저장소의 `origin`이 SSH URL을 사용한다.

### 12.4 개발 도구

```sh
sdk current java
java --version
fnm current
node --version
uv --version
docker context show
docker compose version
```

확인 항목:

- [ ] Java 25와 Node.js 24가 프로젝트 밖의 기본이다.
- [ ] 프로젝트 안에서는 version 선언이 우선한다.
- [ ] uv와 OrbStack이 정상 동작한다.
- [ ] 같은 runtime과 Docker CLI가 중복 설치되지 않았다.

### 12.5 대표 프로젝트

생태계마다 현재 사용하는 대표 프로젝트를 하나 이상 선택해 다음을 검증한다.

확인 항목:

- [ ] Spring Boot build와 test
- [ ] React dependency 복구와 build 또는 test
- [ ] Python dependency 복구와 대표 실행 또는 test
- [ ] 필요한 Compose service와 애플리케이션 연결

설치 command의 version 출력만으로 프로젝트 복구가 끝났다고 판단하지 않는다.

## 13. 재설치 후 정리

### 13.1 이전 GitHub SSH key

새 key로 GitHub 인증과 저장소 접근을 검증한 뒤 GitHub 설정에서 이전 Mac의 public key를 식별한다.

확인 항목:

- [ ] 새 key와 이전 key의 title을 구분했다.
- [ ] 다른 기기에서 아직 사용하는 key가 아닌지 확인했다.
- [ ] 더 이상 사용하지 않는 이전 public key만 제거했다.

현재 key를 잘못 제거하면 GitHub 연결이 중단되므로 fingerprint와 등록 시점을 확인한다.

### 13.2 설치 파일과 Inbox

확인 항목:

- [ ] `Downloads`의 installer와 disk image 중 더 이상 필요하지 않은 사본을 정리했다.
- [ ] `Desktop`에 임시 파일을 남기지 않았다.
- [ ] `04-quickshare`에 재설치 과정의 임시 사본을 남기지 않았다.
- [ ] 삭제할 애플리케이션 data는 공식 제거 범위를 확인했다.

### 13.3 문서 기준 갱신

재설치 중 공식 절차나 기준 version의 변경을 확인했다면 실제 머신 상태를 기록하는 대신 해당 원칙 문서를 수정한다.

1. 변경된 사실의 책임 문서를 찾는다.
2. 선택 이유와 검증 방법을 갱신한다.
3. 관련 문서의 링크와 재설치 순서를 검토한다.
4. secret과 머신 고유 값이 포함되지 않았는지 확인한다.

## 14. 현재 범위 밖의 항목

- macOS 삭제와 초기화 화면의 단계별 안내: Apple의 현재 공식 절차를 따르고 이 문서는 초기화 전후의 확인 순서만 관리한다.
- backup media 선택, 보존 주기와 암호화 방식: 이 문서는 backup 완료 여부만 확인하고 매체와 보존 정책은 다루지 않는다.
- Apple Account와 개인 서비스의 실제 계정 정보: 개인 계정 정보는 저장소에서 관리하지 않는다.
- 현재 설치된 애플리케이션과 CLI inventory: 재설치 순서만 관리하고 머신의 현재 설치 목록은 관리하지 않는다.
- password, token, 복구 코드와 private key backup: secret과 인증정보는 저장소에 기록하지 않는다.
- 실제 dotfiles와 IDE 설정 파일: 책임과 수동 구성 절차만 관리하고 실제 설정 원본은 관리하지 않는다.
- 모든 Git 저장소의 일괄 clone 목록: 현재 필요한 저장소만 복구한다.
- 프로젝트별 database data migration: 각 프로젝트의 절차가 소유한다.
- package 설치와 설정을 실행하는 자동 bootstrap: 현재는 수동 절차와 중단 조건을 먼저 관리한다.

## 15. 핵심 요약

```text
초기화 전
├── data backup을 실제로 검증한다.
├── Git 작업과 container data를 확인한다.
├── 계정 복구 수단을 확인한다.
└── 하나라도 불확실하면 중단한다.

초기화 후
├── macOS·arm64
├── Xcode Command Line Tools·Homebrew
├── 기본 디렉토리
├── CLI·GUI·shell
├── Git·새 GitHub SSH key
├── SDKMAN·fnm·uv·OrbStack
├── 필요한 프로젝트만 clone
└── 프로젝트 선언으로 build·test·service를 검증한다.

완료 후
├── 검증된 새 key를 유지한다.
├── 더 이상 쓰지 않는 이전 key와 임시 파일을 정리한다.
└── 바뀐 공식 절차는 책임 문서 한 곳에 반영한다.
```
