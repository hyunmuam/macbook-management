# 개발환경 구성 원칙

[README로 돌아가기](README.md)

## 1. 문서 목적

Apple Silicon Mac에서 Spring Boot를 주력으로 사용하고 React와 Python 프로젝트를 함께 개발할 때 필요한 runtime, build, dependency와 container 구성 기준을 기록한다.

모든 언어를 하나의 version manager로 통합하지 않는다. 각 생태계에 적합한 도구의 책임을 분리한다. 프로젝트가 선언한 version과 dependency를 기준으로 초기화한 Mac에서도 같은 개발환경을 다시 구성한다.

관리 범위:

- Java, Node.js와 Python runtime의 관리 주체
- Mac에서 사용할 기준 major version과 프로젝트별 version 선언
- Spring Boot의 Gradle Wrapper 사용 원칙
- OrbStack과 Docker Compose를 이용한 로컬 service 구성
- IntelliJ IDEA, VS Code와 Warp의 역할
- 개발환경의 검증과 version 변경 기준

일반적인 설치·업데이트·제거 방식은 [소프트웨어 설치 원칙](software-installation.md)이 소유한다. `.zprofile`과 `.zshrc`의 책임은 [Shell 설정 원칙](shell-configuration.md), GitHub 연결은 [Git과 GitHub SSH 설정 원칙](git-and-ssh.md)이 소유한다.

## 2. 기본 환경

| 항목 | 기준 |
| --- | --- |
| 운영체제 | macOS |
| architecture | Apple Silicon (`arm64`) |
| 프로젝트 위치 | `~/02-work/01-development` |
| Java manager | SDKMAN |
| Java distribution | Eclipse Temurin |
| Java 기본 | 25 LTS |
| Java 호환 | 21 LTS |
| Spring build | 프로젝트의 Gradle Wrapper |
| Node.js manager | fnm |
| Node.js 기본 | 24 LTS |
| Node.js 호환 | 22 LTS |
| Python manager | uv |
| container runtime | OrbStack |
| container 정의 | 프로젝트의 `compose.yaml` |
| Java IDE | IntelliJ IDEA |
| React·Python editor | VS Code |
| 독립 terminal | Warp |

이 표의 major version은 Mac을 새로 구성할 때 적용할 기준이다. 문서를 작성한 시점에 [Eclipse Temurin 지원 일정](https://adoptium.net/support/)은 Java 25와 21을 LTS로, [Node.js release 목록](https://nodejs.org/en/about/previous-releases)은 Node.js 24와 22를 LTS로 분류한다.

지원 상태는 바뀔 수 있으므로 실제 설치와 기준 변경 전에는 공식 문서를 다시 확인한다. patch version과 SDKMAN candidate 식별자는 이 문서에 고정하지 않는다.

## 3. 전체 구성

```text
macOS
├── Homebrew
│   ├── jq
│   ├── ripgrep
│   ├── fd
│   ├── fnm
│   └── uv
├── SDKMAN
│   ├── Eclipse Temurin 25 LTS
│   └── Eclipse Temurin 21 LTS
├── OrbStack
│   ├── Docker Engine
│   └── Docker CLI·Compose
├── IntelliJ IDEA
│   └── Spring Boot
├── VS Code
│   ├── React
│   └── Python
└── ~/02-work/01-development
    └── 각 프로젝트
        ├── runtime version 선언
        ├── dependency lockfile
        ├── build wrapper 또는 script
        └── compose.yaml
```

shell 사용을 위한 `fzf`, Starship, Zoxide와 Zsh plugin은 [Shell 설정 원칙](shell-configuration.md)이 소유한다. Git은 macOS 기본 Git을 사용하고 GitHub CLI는 기본 구성에 포함하지 않는다.

## 4. 구성 원칙

### 4.1 관리 대상마다 관리 주체를 하나만 둔다

같은 Java, Node.js, Python 또는 Docker CLI를 둘 이상의 도구로 중복 설치하지 않는다.

- SDKMAN으로 관리하는 Java를 Homebrew formula로 다시 설치하지 않는다.
- fnm으로 관리하는 Node.js를 Homebrew `node` formula로 다시 설치하지 않는다.
- uv가 관리하는 Python을 사용하므로 pyenv를 추가하지 않는다.
- OrbStack을 사용할 때 Docker Desktop과 Homebrew Docker CLI를 중복해서 두지 않는다.

설치 전에 `type -a <command>`로 같은 명령이 여러 경로에 있는지 확인한다.

### 4.2 프로젝트 선언을 전역 기본값보다 우선한다

전역 기본 version은 version 선언이 없는 작업과 새 프로젝트의 시작점이다. 기존 프로젝트에 `.sdkmanrc`, `.node-version`, `.python-version` 또는 `pyproject.toml`의 Python 요구사항이 있으면 프로젝트 선언을 우선한다.

프로젝트가 요구하는 version에 맞추더라도 Mac 전체의 기본 version을 반복해서 변경하지 않는다.

### 4.3 patch version과 dependency는 프로젝트가 소유한다

이 문서는 장기 기준이 되는 major version만 관리한다. 정확한 runtime version과 dependency는 다음 프로젝트 파일이 소유한다.

| 생태계 | 프로젝트 파일 |
| --- | --- |
| Java | `.sdkmanrc`, Gradle Wrapper 설정과 build 파일 |
| Node.js | `.node-version`, `package.json`, 하나의 lockfile |
| Python | `.python-version`, `pyproject.toml`, `uv.lock` |
| container | `compose.yaml` |

현재 머신에 설치된 patch version을 이 문서에 실측값으로 기록하지 않는다.

### 4.4 전역 dependency를 최소화한다

프로젝트에서 사용하는 library와 build tool은 프로젝트 안에서 선언한다. 전역 설치는 프로젝트와 독립적으로 반복해서 사용하는 CLI에만 허용한다. 개발사도 해당 설치 방식을 지원해야 한다.

Spring Boot build에는 Gradle을 전역 설치하지 않는다. React dependency는 전역 `npm` package로 관리하지 않으며 Python 프로젝트 dependency도 system Python에 설치하지 않는다.

### 4.5 제거와 재설치가 가능한 구성을 유지한다

runtime manager의 cache나 설치 디렉토리를 수동으로 삭제하는 방식으로 정리하지 않는다. 각 관리 도구가 제공하는 제거 명령과 [소프트웨어 설치 원칙](software-installation.md)의 제거 기준을 따른다.

프로젝트는 source와 version·dependency 선언만으로 `.venv`, `node_modules`와 build output을 다시 만들 수 있어야 한다.

## 5. 설정 방법

### 5.1 공통 CLI와 설치 경계

이 개발환경이 기준으로 선택하는 Homebrew formula는 다음과 같다.

| formula | 역할 |
| --- | --- |
| `jq` | JSON 조회와 변환 |
| `ripgrep` | Source와 text 검색 |
| `fd` | 파일과 디렉토리 검색 |
| `fnm` | Node.js version 관리 |
| `uv` | Python과 Python 프로젝트 관리 |

```sh
brew install jq ripgrep fd fnm uv
```

실행 전에 [소프트웨어 설치 원칙](software-installation.md)의 중복 설치 확인과 Homebrew formula 기준을 적용한다. 실제 Brewfile과 현재 설치 목록은 이 저장소에서 관리하지 않는다.

다음 상태를 확인한다.

```sh
command -v jq
command -v rg
command -v fd
command -v fnm
command -v uv
```

각 command는 의도한 하나의 관리 주체에서 제공되어야 한다.

### 5.2 Java와 Spring Boot

#### 5.2.1 SDKMAN을 Java의 단일 관리 주체로 사용한다

SDKMAN 설치는 Homebrew formula 대신 [SDKMAN 공식 설치 절차](https://sdkman.io/install/)를 따른다. 공식 절차가 원격 installer script를 사용하므로 실행 전에 [소프트웨어 설치 원칙의 원격 script 기준](software-installation.md#410-검증되지-않은-설치-경로는-사용하지-않는다)에 따라 공식 URL과 script 내용을 확인한다.

SDKMAN installer가 shell 설정에 추가한 marker와 초기화 block은 직접 관리하는 설정과 구분한다. 구분 기준은 [Shell 설정 원칙](shell-configuration.md)을 따른다. 다른 Mac의 SDKMAN 경로를 복사하지 않는다.

설치 후 확인한다.

```sh
sdk version
sdk list java
```

#### 5.2.2 Temurin 25를 기본으로 하고 21을 호환용으로 유지한다

`sdk list java`에서 현재 제공되는 Temurin 25와 21의 정확한 candidate 식별자를 확인한 뒤 설치한다.

```sh
sdk install java <temurin-25-candidate>
sdk install java <temurin-21-candidate>
sdk default java <temurin-25-candidate>
```

`<temurin-25-candidate>`와 `<temurin-21-candidate>`에는 `sdk list java`가 현재 표시하는 값을 사용한다. 문서의 예전 patch version을 추측해 입력하지 않는다.

현재 기본 version을 확인한다.

```sh
sdk current java
java --version
```

#### 5.2.3 프로젝트는 `.sdkmanrc`로 Java version을 선언한다

Spring Boot 프로젝트 root에서 현재 Java를 기준으로 `.sdkmanrc`를 만들 수 있다.

```sh
sdk env init
```

파일에는 프로젝트가 사용하는 정확한 SDKMAN candidate를 기록한다.

```text
java=<project-temurin-candidate>
```

프로젝트 진입 후 version을 적용한다.

```sh
sdk env
```

설치되지 않은 candidate라면 프로젝트 선언을 확인한 뒤 설치한다.

```sh
sdk env install
```

프로젝트를 벗어나 기본 version으로 돌아갈 때는 다음 명령을 사용한다.

```sh
sdk env clear
```

자동 전환이 실제로 필요해지기 전에는 `sdkman_auto_env=true`를 기본값으로 강제하지 않는다.

#### 5.2.4 Gradle Wrapper만 사용한다

Spring Boot 프로젝트는 다음 파일을 함께 version control에 포함한다.

```text
spring-project/
├── build.gradle 또는 build.gradle.kts
├── gradlew
├── gradlew.bat
└── gradle/
    └── wrapper/
```

Mac에 Gradle을 전역 설치하지 않는다.

```sh
brew install gradle
```

위 명령은 실행하지 않는다. 프로젝트 wrapper로 실행하고 build한다.

```sh
./gradlew bootRun
./gradlew build
```

Wrapper file이 없거나 실행 권한이 없으면 전역 Gradle로 우회하지 않고 프로젝트 설정을 먼저 복구한다.

### 5.3 Node.js와 React

#### 5.3.1 fnm을 Node.js의 단일 관리 주체로 사용한다

Homebrew로 fnm을 설치하고 Node.js 자체는 fnm으로 설치한다.

```sh
fnm install 24
fnm install 22
fnm default 24
```

명령을 실행하면 해당 major에서 당시 지원하는 최신 patch version이 설치된다. 프로젝트가 더 정확한 version을 요구하면 `.node-version`에 그 값을 기록한다.

#### 5.3.2 fnm은 interactive Zsh에서 초기화한다

[fnm 공식 Zsh 설정](https://github.com/Schniz/fnm#shell-setup)에 따라 다음 block을 `~/.zshrc`에 둔다.

```zsh
if command -v fnm >/dev/null 2>&1; then
  eval "$(fnm env --use-on-cd --shell zsh)"
fi
```

`--use-on-cd`는 `.node-version`이 있는 프로젝트에 진입할 때 version을 전환한다. block 위치와 문법 검증은 [Shell 설정 원칙](shell-configuration.md)을 따른다.

#### 5.3.3 프로젝트는 `.node-version`으로 Node.js version을 선언한다

새 React 프로젝트의 기본 형태는 다음과 같다.

```text
frontend/
├── package.json
├── package-lock.json 또는 다른 하나의 lockfile
└── .node-version
```

기본 major version만 요구하는 프로젝트는 다음처럼 기록할 수 있다.

```text
24
```

정확한 patch version이 필요한 프로젝트는 전체 version을 기록한다. 프로젝트에 진입한 뒤 확인한다.

```sh
fnm current
node --version
```

#### 5.3.4 프로젝트마다 package manager와 lockfile을 하나만 사용한다

프로젝트가 선택한 `npm`, `pnpm` 또는 `yarn` 중 하나를 사용한다. 다음 lockfile을 한 프로젝트에서 의도 없이 함께 관리하지 않는다.

- `package-lock.json`
- `pnpm-lock.yaml`
- `yarn.lock`

dependency 설치와 build 명령은 프로젝트의 README와 `package.json` script를 따른다. MacBook 관리 문서가 모든 React 프로젝트에 하나의 package manager를 강제하지 않는다.

### 5.4 Python

#### 5.4.1 uv가 Python과 프로젝트 환경을 관리한다

Python을 가끔 사용하는 현재 범위에서는 pyenv를 추가하지 않는다. uv는 필요한 Python을 찾거나 설치하고 프로젝트 virtual environment와 dependency를 관리한다.

[uv의 Python version 문서](https://docs.astral.sh/uv/concepts/python-versions/)와 프로젝트 선언을 기준으로 필요한 Python을 준비한다.

```sh
uv python list
uv python install <python-version>
```

`<python-version>`은 프로젝트의 요구사항을 사용한다. 전역 기본 Python version을 이 문서에서 고정하지 않는다.

#### 5.4.2 프로젝트가 Python version과 dependency를 선언한다

기본 구조는 다음과 같다.

```text
python-project/
├── .python-version
├── pyproject.toml
├── uv.lock
└── .venv/
```

`.python-version`은 프로젝트 기본 Python version을 선언하고 `pyproject.toml`의 `requires-python`은 지원 범위를 선언한다. `uv.lock`은 version control에 포함하고 uv가 관리하게 한다. `.venv`는 생성물로 보고 Git에서 제외한다.

현재 디렉토리에 Python version을 선언할 때는 다음 명령을 사용할 수 있다.

```sh
uv python pin <python-version>
```

#### 5.4.3 `uv sync`와 `uv run`을 사용한다

프로젝트 environment를 복구한다.

```sh
uv sync
```

프로젝트 environment 안에서 명령을 실행한다.

```sh
uv run python main.py
```

`uv run`은 프로젝트 metadata와 lockfile을 기준으로 environment를 확인한다. system Python에 `pip install`을 실행해 프로젝트 dependency를 섞지 않는다.

### 5.5 OrbStack과 프로젝트 container

#### 5.5.1 OrbStack을 Docker runtime의 단일 관리 주체로 사용한다

OrbStack은 [공식 사이트](https://orbstack.dev/)에서 제공하는 macOS 애플리케이션으로 설치한다. GUI 애플리케이션의 설치 주체 선택은 [소프트웨어 설치 원칙](software-installation.md)을 따른다.

Docker Desktop을 함께 설치하지 않는다. OrbStack에는 Docker Engine과 `docker`, `docker compose`, `docker buildx` 등의 CLI가 포함되므로 Homebrew로 Docker CLI를 중복 설치하지 않는다. 자세한 동작은 [OrbStack Docker 문서](https://docs.orbstack.dev/docker/)에서 확인한다.

#### 5.5.2 Docker context와 CLI 출처를 확인한다

```sh
docker context show
docker version
docker compose version
type -a docker
```

기대 상태는 다음과 같다.

- Docker context가 `orbstack`이다.
- Client와 Server version이 모두 출력된다.
- Compose version이 출력된다.
- Docker CLI가 Docker Desktop 또는 Homebrew 설치본과 중복되지 않는다.

OrbStack은 기존 Docker CLI가 있으면 이를 임의로 교체하지 않을 수 있다. 중복이 확인되면 파일을 직접 삭제하기 전에 기존 관리 주체와 [OrbStack 설치 문서](https://docs.orbstack.dev/install)를 확인한다.

#### 5.5.3 프로젝트 전용 service는 해당 저장소가 소유한다

MySQL, PostgreSQL, Redis와 Kafka를 macOS에 직접 설치하지 않는다. 특정 프로젝트에 필요한 service는 해당 Git 저장소의 `compose.yaml`에 선언한다.

```text
spring-project/
├── src/
├── build.gradle 또는 build.gradle.kts
├── gradlew
└── compose.yaml
```

공용 `~/02-work/04-infra` 디렉토리나 Mac 전체에서 공유하는 중앙 Compose 구성을 만들지 않는다.

#### 5.5.4 image version과 프로젝트 data를 명시적으로 관리한다

`latest` tag를 기본값으로 사용하지 않고 프로젝트가 검증한 image version을 명시한다.

```yaml
services:
  database:
    image: postgres:<validated-version>
```

실제 password, token과 운영 환경 secret을 Compose file에 commit하지 않는다. 필요한 환경 변수의 이름과 비민감 예시는 `.env.example`처럼 실제 값과 분리한다.

Named volume이나 bind mount의 data는 source code와 별개다. `docker compose down`은 일반 종료에 사용할 수 있다. 다만 volume을 삭제하는 option은 data 삭제 목적과 backup 여부를 확인하기 전에는 실행하지 않는다.

#### 5.5.5 프로젝트별로 실행하고 검증한다

Compose file의 해석 결과를 먼저 확인한다.

```sh
docker compose config
```

이어서 service를 시작하고 상태를 확인한다.

```sh
docker compose up -d
docker compose ps
```

일반 종료는 다음 명령을 사용한다.

```sh
docker compose down
```

service가 정상인지 판단하는 healthcheck와 애플리케이션 연결 검증은 각 프로젝트가 소유한다.

### 5.6 IDE와 terminal 역할

| 도구 | 역할 |
| --- | --- |
| IntelliJ IDEA | Spring Boot와 Java 프로젝트 개발 |
| VS Code | React와 Python 프로젝트 개발 |
| Warp | 독립 interactive terminal |
| IDE 내장 terminal | 현재 프로젝트 context의 명령 실행 |

이 문서는 IDE plugin, keymap, theme, workspace와 프로젝트 setting을 관리하지 않는다. 설치·업데이트·제거는 [소프트웨어 설치 원칙](software-installation.md)을 따른다. terminal별 shell 동작은 [Shell 설정 원칙](shell-configuration.md)을 따른다.

## 6. 검증

### 6.1 관리 도구

```sh
brew --prefix
sdk version
fnm --version
uv --version
docker context show
```

다음을 확인한다.

- Homebrew prefix는 `/opt/homebrew`다.
- 각 관리 도구가 오류 없이 실행된다.

관리 도구가 실행되지 않으면 [설정 방법](#5-설정-방법)에서 해당 도구의 구성 절차를 따른다.

### 6.2 runtime

```sh
sdk current java
java --version
fnm current
node --version
uv python list
```

다음을 확인한다.

- 프로젝트 밖에서는 Java 25와 Node.js 24 계열이 기본이다.
- 프로젝트 안에서는 각 version 선언과 실행 결과가 일치한다.

전역 Java 또는 Node.js version이 다르면 [Temurin 기본·호환 version 설정](#522-temurin-25를-기본으로-하고-21을-호환용으로-유지한다)과 [fnm의 Node.js 기본 version 설정](#531-fnm을-nodejs의-단일-관리-주체로-사용한다)을 따른다.

프로젝트 선언과 실행 결과가 다르면 Java는 [`.sdkmanrc` 선언](#523-프로젝트는-sdkmanrc로-java-version을-선언한다), Node.js는 [`.node-version` 선언](#533-프로젝트는-node-version으로-nodejs-version을-선언한다), Python은 [Python version과 dependency 선언](#542-프로젝트가-python-version과-dependency를-선언한다)을 따른다.

### 6.3 프로젝트 재현

Spring Boot 프로젝트:

```sh
sdk env
./gradlew build
```

다음을 확인한다.

- `.sdkmanrc`가 지정한 Java가 선택된다.
- Gradle Wrapper의 build와 test가 통과한다.

선택된 Java가 다르면 [`.sdkmanrc` 선언](#523-프로젝트는-sdkmanrc로-java-version을-선언한다)을 따른다.

React 프로젝트는 `.node-version` 전환을 확인한 뒤 프로젝트가 선언한 lockfile과 script를 사용한다.

```sh
node --version
```

출력된 version이 `.node-version`의 선언과 일치해야 한다.

출력된 version이 다르면 [`.node-version` 선언](#533-프로젝트는-node-version으로-nodejs-version을-선언한다)을 따른다.

Python 프로젝트:

```sh
uv sync
uv run python --version
```

다음을 확인한다.

- dependency 복구가 완료된다.
- 출력된 Python version이 프로젝트 선언과 일치한다.

출력된 Python version이 다르면 [Python version과 dependency 선언](#542-프로젝트가-python-version과-dependency를-선언한다)을 따른다.

Compose 프로젝트:

```sh
docker compose config
docker compose up -d
docker compose ps
```

다음을 확인한다.

- `compose.yaml`이 오류 없이 해석된다.
- 필요한 service가 정상 상태다.

검증하려고 시작한 service는 확인 후 프로젝트 절차에 따라 종료한다.

## 7. 이후 사용 및 유지보수

### 7.1 기준 version 변경

Java 또는 Node.js 기준 major version은 다음 조건을 확인한 뒤 변경한다.

1. 공식 지원 상태가 LTS인가.
2. 주력 Spring Boot와 React 프로젝트가 지원하는가.
3. IDE와 주요 build plugin이 지원하는가.
4. 기존 호환 version을 유지해야 하는 프로젝트가 있는가.
5. 새 version에서 대표 프로젝트의 build와 test가 통과하는가.

전역 기본 version을 먼저 바꾸고 프로젝트 오류를 나중에 해결하지 않는다. 대표 프로젝트 검증 후 기준 표와 재설치 절차를 함께 갱신한다.

기준 version을 바꾸면 [재설치 원칙의 개발환경 구성](reinstallation.md#10-개발환경-구성), [개발 도구 검증](reinstallation.md#124-개발-도구), [대표 프로젝트 검증](reinstallation.md#125-대표-프로젝트)을 함께 검토한다.

### 7.2 patch version 업데이트

보안과 bug fix를 위해 지원 중인 major 안에서 patch version을 업데이트할 수 있다. 프로젝트가 정확한 patch version을 선언했다면 build와 test 없이 `.sdkmanrc`, `.node-version` 또는 lockfile을 변경하지 않는다.

### 7.3 도구 제거

더 이상 사용하지 않는 runtime과 manager는 공식 제거 절차를 확인한다. 실행 파일과 shell 초기화 block, cache와 프로젝트 생성물을 구분한다. 프로젝트 source와 lockfile은 기본적으로 보존한다.

## 8. 현재 범위 밖의 항목

- 현재 머신의 실제 runtime과 package 설치 목록: 이 문서는 장기 기준만 관리하고 머신의 실측 상태는 관리하지 않는다.
- Brewfile과 자동 설치 script: 실제 설치 목록과 자동화는 저장소의 현재 범위 밖이다.
- 실제 `.zshrc`, `.zprofile`과 SDKMAN 설정 원본: 이 문서는 책임과 배치 기준만 관리하고 실제 dotfiles는 관리하지 않는다.
- IDE plugin, keymap, theme와 workspace 설정: IDE의 역할만 정하고 애플리케이션 내부 설정은 다루지 않는다.
- 개별 프로젝트의 dependency와 build script: 각 프로젝트의 선언 파일이 소유한다.
- 운영 환경의 container 배포와 secret 관리: 이 문서는 macOS의 local 개발환경만 다룬다.
- Kubernetes와 공용 local infra 구성: 현재 역할이 확정되지 않아 기본 구성에 포함하지 않는다.
- GitHub CLI: 기본 Git과 SSH 구성에 필요하지 않아 포함하지 않는다.
- pyenv와 Docker Desktop: Python과 Docker runtime의 관리 주체를 각각 uv와 OrbStack으로 정했으므로 포함하지 않는다.

## 9. 핵심 요약

```text
Java
└── SDKMAN
    ├── Temurin 25 LTS — 기본
    ├── Temurin 21 LTS — 호환
    └── 프로젝트: .sdkmanrc + Gradle Wrapper

Node.js
└── fnm
    ├── Node.js 24 LTS — 기본
    ├── Node.js 22 LTS — 호환
    └── 프로젝트: .node-version + 하나의 lockfile

Python
└── uv
    └── 프로젝트: .python-version + pyproject.toml + uv.lock

container
└── OrbStack
    └── 프로젝트: compose.yaml + 명시적인 image version

프로젝트 root
└── ~/02-work/01-development
```

- [관리 대상마다 관리 주체를 하나만 둔다](#41-관리-대상마다-관리-주체를-하나만-둔다)
- [프로젝트 선언을 전역 기본값보다 우선한다](#42-프로젝트-선언을-전역-기본값보다-우선한다)
- [patch version과 dependency는 프로젝트가 소유한다](#43-patch-version과-dependency는-프로젝트가-소유한다)
- [전역 dependency를 최소화한다](#44-전역-dependency를-최소화한다)
- [제거와 재설치가 가능한 구성을 유지한다](#45-제거와-재설치가-가능한-구성을-유지한다)
