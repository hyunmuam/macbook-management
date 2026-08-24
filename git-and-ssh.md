# Git과 GitHub SSH 설정 원칙

[README로 돌아가기](README.md)

## 1. 문서 목적

macOS에서 Git을 사용하고 GitHub 저장소에 SSH로 접근할 때 필요한 기준과 설정 방법을 정리한다. 이 구성에서는 `git clone`, `git pull`, `git fetch`, `git push` 등의 작업을 안정적으로 수행한다.

## 2. 기본 환경

| 항목 | 기준 |
| --- | --- |
| 운영체제 | macOS |
| GitHub 인증 방식 | SSH |
| SSH key algorithm | Ed25519 |
| SSH key 저장 경로 | `~/.ssh` 아래의 Ed25519 key (`~/.ssh/id_ed25519`는 기본값 예시) |
| SSH key passphrase | 사용하지 않음 |
| macOS Keychain의 SSH passphrase 저장 | 사용하지 않음 |
| Personal Access Token 관리 | 하지 않음 |
| 별도 SSH agent 설정 | 하지 않음 |

## 3. 전체 구성

인증 흐름은 `Git` → `SSH` → `~/.ssh` 아래의 Ed25519 private key → `GitHub` 순서다.

아래 트리와 파일 표는 `ssh-keygen`의 기본 파일명인 `id_ed25519`를 사용한 예시다.

```text
~/
├── .gitconfig
└── .ssh/
    ├── config
    ├── id_ed25519
    ├── id_ed25519.pub
    └── known_hosts
```

| 파일 | 역할 |
| --- | --- |
| `~/.gitconfig` | Git 전역 사용자 정보와 설정 |
| `~/.ssh/config` | GitHub에 접속할 때 적용할 SSH 설정 |
| `~/.ssh/id_ed25519` | SSH private key |
| `~/.ssh/id_ed25519.pub` | GitHub에 등록할 SSH public key |
| `~/.ssh/known_hosts` | 접속한 SSH 서버의 host key 정보 |

## 4. 구성 원칙

### 4.1 GitHub 인증에는 SSH를 사용한다

GitHub 저장소 접근에는 SSH를 기본 방식으로 사용한다.

- Personal Access Token을 직접 관리하지 않는다.
- `git pull`과 `git push` 때마다 인증 정보를 입력하지 않는다.
- 인증에 사용할 key를 `~/.ssh/config`에 명시한다.
- 저장소 remote에는 SSH URL을 사용한다.

### 4.2 Ed25519 key를 사용한다

SSH key는 Ed25519 algorithm으로 생성한다. private key는 이 Mac에만 보관하고 public key만 GitHub에 등록한다. 기본 파일명을 사용할 때 경로는 각각 `~/.ssh/id_ed25519`와 `~/.ssh/id_ed25519.pub`다.

private key를 외부에 공개하거나 GitHub에 업로드해서는 안 된다.

### 4.3 passphrase와 별도 SSH agent 설정을 사용하지 않는다

이번 구성에서는 SSH key에 passphrase를 설정하지 않는다. SSH는 `~/.ssh/config`에 지정한 private key 파일을 직접 사용하므로 `UseKeychain yes`, `AddKeysToAgent yes`를 추가하거나 다음 명령을 실행하지 않는다.

```sh
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

구성은 단순하다. 다만 private key 파일을 확보한 사람은 별도의 passphrase 없이 key를 사용할 수 있다. 파일 권한을 제한하고 private key를 외부에 공유하지 않는다.

이 선택은 SSH key의 일반적인 보안 권장값이 아니다. 현재 개인 환경에서 관리 복잡도를 줄이기 위한 명시적인 예외다. 다음 조건이 생기면 passphrase, macOS Keychain 또는 별도 agent 사용을 다시 판단한다. 판단 결과를 이 문서의 기준에 먼저 반영한 뒤 새 key를 만든다.

- Mac을 여러 사용자가 공유한다.
- private key가 포함될 수 있는 home directory backup 또는 동기화를 사용한다.
- 기기 분실이나 local account 침해 위험에 대한 보호 수준을 높여야 한다.
- 조직 또는 프로젝트의 보안 정책이 passphrase나 hardware-backed key를 요구한다.

### 4.4 저장소에는 SSH URL을 사용한다

새 저장소를 clone하거나 remote를 설정할 때는 `git@github.com:<owner>/<repository>.git` 형태의 SSH URL을 사용한다.

### 4.5 Git 설치와 GitHub 인증을 분리한다

Git과 OpenSSH는 macOS 기본 도구를 사용한다. GitHub에 접근하려고 Homebrew Git을 추가로 설치하지 않는다. 일반적인 설치 판단 기준은 [소프트웨어 설치 원칙](software-installation.md)에서 관리한다.

최신 기능이나 특정 version이 필요해지면 설치 방식을 재검토한다.

### 4.6 shell 설정을 변경하지 않는다

GitHub SSH 인증 설정은 `~/.ssh/config`에서 관리한다. `~/.zshrc`나 `~/.zprofile`은 수정하지 않는다. shell 설정의 책임과 파일별 역할은 [Shell 설정 원칙](shell-configuration.md)을 따른다.

### 4.7 GitHub CLI는 기본 구성에 포함하지 않는다

기본 구성은 `Git + SSH`로 유지한다. Pull Request나 Issue 등 GitHub 서비스 기능을 terminal에서 다룰 필요가 생기면 GitHub CLI 도입을 별도로 판단한다.

## 5. 설정 방법

### 5.1 Git과 SSH 상태 확인

```sh
git --version
command -v git
ssh -V
command -v ssh
```

명령마다 version 또는 실행 경로가 출력되어야 한다. Git 실행 시 Xcode Command Line Tools 설치 안내가 나타나면 안내에 따라 설치한다.

### 5.2 기존 SSH 설정 확인

```sh
ls -la ~/.ssh
```

초기화 직후에는 아래 메시지가 나타날 수 있다.

```text
ls: /Users/<username>/.ssh: No such file or directory
```

초기화 직후 이 메시지가 나오는 것은 정상이다. 기존 `config`나 key가 있다면 덮어쓰기 전에 용도와 사용 중인 서비스를 확인한다.

### 5.3 Git 사용자 정보 설정

```sh
git config --global user.name "<your-name>"
git config --global user.email "<your-email>"
```

```sh
git config --global user.name
git config --global user.email
git config --global --list
```

여기서 설정하는 이메일은 GitHub 인증 정보가 아니라 commit author 정보다. 이메일 공개를 원하지 않는다면 GitHub에서 제공하는 `noreply` 이메일을 사용할 수 있다.

### 5.4 SSH key 생성

```sh
ssh-keygen -t ed25519 -C "<github-email>"
```

저장 경로를 묻는 단계에서 기본 경로를 사용하려면 `Enter`를 누른다.

```text
Enter file in which to save the key (/Users/<username>/.ssh/id_ed25519):
```

passphrase를 묻는 두 단계에서도 각각 `Enter`를 누른다.

```text
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

같은 이름의 key가 이미 있다면 덮어쓰지 말고 기존 key의 용도를 먼저 확인한다. 생성 후 파일과 권한을 확인한다.

```sh
ls -l ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub
```

필요하면 권한을 맞춘다.

```sh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### 5.5 SSH config 구성

기존 파일이 없다면 생성하고 권한을 설정한다.

```sh
touch ~/.ssh/config
chmod 600 ~/.ssh/config
```

`~/.ssh/config`를 선호하는 텍스트 편집기로 열고 다음 block을 추가한다. 기존 파일이 있다면 전체를 교체하지 않고 충돌 없이 추가한다. 다음 예시는 기본 파일명 `id_ed25519`를 사용한다. 별도 이름으로 생성한 key를 사용할 때는 `IdentityFile`을 실제 private key 경로로 맞춘다.

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

| 옵션 | 역할 |
| --- | --- |
| `Host` | `github.com` 접속에 이 block을 적용한다. |
| `HostName` | 실제 접속할 서버 주소를 지정한다. |
| `User` | GitHub SSH 접속 사용자 `git`을 지정한다. |
| `IdentityFile` | 인증에 사용할 private key를 지정한다. |
| `IdentitiesOnly` | 지정한 `IdentityFile`만 사용하게 한다. |

GitHub 계정은 SSH public key로 식별되므로 `User`에는 GitHub 사용자명이 아니라 `git`을 사용한다.

### 5.6 GitHub에 public key 등록

public key를 macOS clipboard에 복사한다.

```sh
pbcopy < ~/.ssh/id_ed25519.pub
```

출력이 없는 것이 정상이다. 직접 확인하려면 다음 명령을 사용한다.

```sh
cat ~/.ssh/id_ed25519.pub
```

public key는 `ssh-ed25519 AAAA... <github-email>` 형태다.

GitHub의 `Settings` → `SSH and GPG keys` → `New SSH key`로 이동해 다음 값을 입력한다.

- Title: key의 용도를 식별하는 이름
- Key type: `Authentication Key`
- Key: `id_ed25519.pub` 내용

GitHub에는 public key만 등록한다.

public key를 등록한 뒤 다음 명령을 실행한다. 상세 확인 절차는 [GitHub 인증 검증](#63-github-인증)을 따른다.

```sh
ssh -T git@github.com
```

### 5.7 저장소 연결

새 repository는 SSH URL로 clone한다.

```sh
git clone git@github.com:<owner>/<repository>.git
cd <repository>
git remote -v
```

기존 HTTPS remote를 변경하려고 repository를 다시 clone할 필요는 없다.

```sh
git remote -v
git remote set-url origin git@github.com:<owner>/<repository>.git
git remote -v
```

## 6. 검증

### 6.1 Git 설정

```sh
git --version
git config --global user.name
git config --global user.email
```

다음을 확인한다.

- Git이 실행된다.
- 의도한 사용자 정보가 출력된다.

Git이 실행되지 않으면 [Git과 SSH 상태 확인](#51-git과-ssh-상태-확인), 사용자 정보가 다르면 [Git 사용자 정보 설정](#53-git-사용자-정보-설정) 절차를 따른다.

### 6.2 SSH 파일과 설정

```sh
ls -la ~/.ssh
cat ~/.ssh/config
```

다음을 확인한다.

- `~/.ssh/config`의 `IdentityFile`이 가리키는 Ed25519 private key와 대응하는 public key가 존재한다.
- `~/.ssh/config`에 `Host github.com` block이 존재한다.
- 첫 연결을 승인한 뒤 `~/.ssh/known_hosts`가 존재한다.
- private key와 `config`의 권한이 각각 `600`이다.

key, `config` 또는 권한이 기준과 다르면 [설정 방법](#5-설정-방법)의 SSH key 생성과 config 구성 절차를 따른다.

### 6.3 GitHub 인증

```sh
ssh -T git@github.com
```

처음 접속하면 host authenticity 확인 메시지가 나타날 수 있다.

```text
The authenticity of host 'github.com (...)' can't be established.
ED25519 key fingerprint is ...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

표시된 fingerprint가 [GitHub가 공개한 SSH host key fingerprint](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)와 일치하는지 확인한 뒤 `yes`를 입력한다. 확인 없이 승인하지 않는다.

인증에 성공하면 다음과 비슷한 메시지가 나타난다.

```text
Hi <github-username>! You've successfully authenticated, but GitHub does not provide shell access.
```

GitHub는 shell access를 제공하지 않으므로 다음을 확인한다.

- 위와 비슷한 성공 메시지가 나타난다.
- 의도한 `<github-username>`이 나타난다.

두 항목이 나타나면 인증에 성공했다. 이 명령은 성공 메시지를 출력해도 종료 상태 `1`을 반환할 수 있다.

### 6.4 저장소 remote

저장소 안에서 다음 명령을 실행한다.

```sh
git remote -v
```

fetch와 push URL이 `git@github.com:<owner>/<repository>.git` 형태인지 확인한다.

remote URL이 기준과 다르면 [저장소 연결](#57-저장소-연결) 절차를 따른다.

## 7. 이후 사용 및 유지보수

### 7.1 기본 Git 작업

SSH 설정을 마치면 다음 명령에는 별도의 GitHub 로그인이 필요하지 않다.

```sh
git pull
git fetch
git push
```

새 repository에는 SSH URL을 사용하고 `git remote -v`로 remote가 의도한 주소를 가리키는지 확인한다.

### 7.2 SSH key 관리

- private key와 public key의 보관·등록 기준은 [Ed25519 key 사용 원칙](#42-ed25519-key를-사용한다)을 따른다.
- key 파일이나 `~/.ssh/config`를 변경한 뒤에는 [GitHub 인증 검증](#63-github-인증)을 다시 수행한다.
- 새로운 key를 만들기 전에 기존 key의 용도와 등록 상태를 확인한다.

### 7.3 SSH key 회전과 폐기

기존 key를 교체할 때는 다음 순서를 지킨다.

1. 새 key 생성
   - 기존 key를 덮어쓰지 않도록 `ssh-keygen -t ed25519 -C "<github-email>"`을 실행하고 저장 경로에 별도의 `<new-key-name>`을 지정한다.
   - 새 private key는 `600`, public key는 `644` 권한으로 맞춘다.
2. GitHub 등록 교체
   - 새 public key를 GitHub의 `SSH and GPG keys`에 `Authentication Key`로 등록한다.
   - `~/.ssh/config`의 `IdentityFile`을 `~/.ssh/<new-key-name>`으로 변경한다.
   - `ssh -T git@github.com`으로 새 key가 동작하는지 확인한다.
3. 기존 key 폐기
   - 기존 key가 다른 서비스나 자동화에서 사용되지 않는지 확인한다.
   - GitHub의 `SSH and GPG keys`에서 기존 public key를 삭제한다.
   - 로컬의 기존 private key와 public key 파일을 삭제한다. 삭제한 credential은 복구할 수 없으므로 정확한 파일을 확인한 뒤 처리한다.
4. 재검증
   - [GitHub 인증 검증](#63-github-인증)과 [저장소 remote 검증](#64-저장소-remote)을 다시 수행한다.

## 8. 현재 범위 밖의 항목

- 다계정(work/personal) SSH 구성: 현재 기준은 하나의 GitHub 계정과 `Host github.com` 하나만 사용하므로 다루지 않는다.
- commit signing: 저장소 접근 인증과 commit 서명은 책임이 다르므로 현재 SSH 인증 범위에 포함하지 않는다.
- HTTPS + PAT: SSH를 기본 접근 방식으로 정했으므로 token 발급과 보관 절차를 다루지 않는다.
- GitHub CLI 인증: 기본 Git 작업에는 `Git + SSH`로 충분하므로 `gh auth` 구성은 필요가 생길 때 별도로 다룬다.

## 9. 핵심 요약

```text
macOS
│
├── Git
│   ├── user.name / user.email
│   └── SSH 저장소 URL
│
└── OpenSSH
    ├── ~/.ssh/config
    └── ~/.ssh/<ed25519-key>
              │
              └── GitHub SSH authentication
```

- [GitHub 인증에는 SSH를 사용한다](#41-github-인증에는-ssh를-사용한다)
- [Ed25519 key를 사용한다](#42-ed25519-key를-사용한다)
- [passphrase와 별도 SSH agent 설정을 사용하지 않는다](#43-passphrase와-별도-ssh-agent-설정을-사용하지-않는다)
- [저장소에는 SSH URL을 사용한다](#44-저장소에는-ssh-url을-사용한다)
- [Git 설치와 GitHub 인증을 분리한다](#45-git-설치와-github-인증을-분리한다)
- [shell 설정을 변경하지 않는다](#46-shell-설정을-변경하지-않는다)
- [GitHub CLI는 기본 구성에 포함하지 않는다](#47-github-cli는-기본-구성에-포함하지-않는다)
