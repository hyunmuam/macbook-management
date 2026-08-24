# 소프트웨어 설치 원칙

[README로 돌아가기](README.md)

## 1. 문서 목적

macOS에서 소프트웨어를 설치하기 전에 관리 주체를 선택하고 설치 후에는 업데이트와 제거 경로까지 확인하는 기준을 기록한다.

모든 소프트웨어를 하나의 package manager로 통일하지 않는다. 도구의 종류와 개발사의 배포 정책에 맞는 설치 주체를 선택한다. 아래 내용은 시간이 지나도 설명할 수 있어야 한다.

- 어떤 목적으로 설치했는가.
- 어떤 주체가 설치와 업데이트를 관리하는가.
- 같은 프로그램이 다른 방식으로 중복 설치되어 있지 않은가.
- 설치 과정에서 어떤 파일과 시스템 항목이 추가되는가.
- 더 이상 필요하지 않을 때 어떤 방법으로 제거하는가.

이 문서는 개별 프로그램의 설치 여부나 현재 머신의 설치 목록을 관리하지 않는다. Git처럼 설치 여부를 이미 결정한 도구는 해당 도구를 소유하는 문서가 개별 결정을 관리한다. 이 문서는 그 결정에 적용할 일반 기준만 관리한다.

## 2. 기본 환경

| 항목 | 기준 |
| --- | --- |
| 운영체제 | macOS |
| architecture | Apple Silicon |
| Homebrew prefix | `/opt/homebrew` |
| Homebrew 실행 경로 | Apple Silicon 기본 경로 |

기본 환경은 다음 명령으로 확인한다.

```sh
sw_vers -productName
uname -m
brew --prefix
command -v brew
```

기대 형태는 다음과 같다.

- `sw_vers -productName`은 `macOS`를 출력한다.
- `uname -m`은 `arm64`를 출력한다.
- `brew --prefix`는 `/opt/homebrew`를 출력한다.
- `command -v brew`는 `/opt/homebrew/bin/brew` 형태를 출력한다.

이 표의 값은 [README의 적용 기준](README.md#적용-기준)을 설치 판단에 적용한 기준이며 현재 기기의 실측 기록이 아니다.

macOS, Homebrew 또는 각 도구의 version에 따라 명령과 설치 방식이 달라질 수 있다. 실제로 설치하거나 제거하기 전에는 해당 도구의 공식 문서에서 현재 절차를 다시 확인한다.

## 3. 전체 구성

```text
설치 대상
├── CLI 또는 개발 환경 구성 요소
│   └── Homebrew formula
├── GUI 애플리케이션
│   ├── 개발사가 명시한 공식 권장 방식
│   ├── 공식 installer
│   ├── Mac App Store
│   └── Homebrew cask
├── 프로젝트 dependency
│   └── 프로젝트의 language-specific package manager
├── 프로젝트와 독립적인 전역 CLI
│   └── 공식 language-specific package manager
└── 직접 다운로드
    └── 공식 배포와 검증 조건을 충족한 파일
```

## 4. 구성 원칙

### 4.1 도구 종류와 공식 배포 정책에 따라 설치 주체를 정한다

CLI와 개발 환경 구성 요소는 Homebrew formula를 우선한다. 설치 위치와 version, 업데이트와 제거를 같은 관리 주체에서 확인할 수 있기 때문이다.

프로젝트 dependency는 프로젝트가 사용하는 language-specific package manager로 관리한다. 개발사가 공식 설치 경로를 제공하는 전역 CLI도 `npm`, `pipx`, `cargo` 같은 language-specific package manager로 관리할 수 있다. 다만 프로젝트와 독립적인 도구여야 한다. runtime version 관리와 프로젝트 dependency 격리의 상세 기준은 [개발환경 구성 원칙](development-environment.md)에서 관리한다.

GUI 애플리케이션은 [GUI 애플리케이션 설치 원칙](#43-gui-애플리케이션은-개발사가-의도한-관리-방식을-우선한다)의 우선순위를 따른다. 도구 종류만으로 설치 명령을 기계적으로 정하지 않는다. 개발사가 지원하는 업데이트와 제거 경로까지 함께 판단한다.

### 4.2 하나의 프로그램에는 관리 주체를 하나만 둔다

같은 프로그램을 Homebrew formula, Homebrew cask, 공식 installer, Mac App Store, language-specific package manager 중 둘 이상으로 중복 설치하지 않는다.

관리 주체가 여러 개이면 실행 파일과 업데이트 대상이 달라지고 제거한 뒤에도 다른 설치본이 남을 수 있다. 설치 전에 기존 실행 경로와 package manager의 관리 목록을 확인한다. 이미 설치되어 있다면 기존 관리 주체부터 식별한다.

Git 설치 여부는 [Git과 GitHub SSH 설정 원칙](git-and-ssh.md)이 소유한다.

### 4.3 GUI 애플리케이션은 개발사가 의도한 관리 방식을 우선한다

GUI 애플리케이션은 다음 순서로 설치 방식을 판단한다.

1. 개발사가 명시한 공식 권장 설치 방법
2. 개발사가 제공하는 공식 installer
3. Mac App Store
4. Homebrew cask

개발사가 여러 방식을 같은 수준으로 제공하면 다음 기준을 순서대로 비교한다.

1. 공식 업데이트 체계를 가장 잘 지원하는가.
2. 애플리케이션 권한과 보안 검증이 명확한가.
3. 삭제와 다른 Mac으로의 이전이 쉬운가.
4. 여러 Mac에서 같은 구성을 재현할 필요가 있는가.

Mac App Store는 Apple 생태계 앱과 Mac App Store에서만 제공되는 앱에 제한적으로 사용한다. 구독·구매 이력 관리가 중요하거나 Apple ID 기반 동기화가 필요한 앱도 대상이다. 개발 도구나 개발사가 직접 배포하는 앱은 공식 사이트의 배포 방식을 우선한다.

Homebrew cask를 금지하지는 않는다. 공식 설치 방법이 불편하거나 여러 Mac에서 재현할 필요가 있고 Homebrew 관리의 실익이 분명할 때 선택한다. 다만 기본 우선순위는 낮게 둔다. 그래야 GUI 애플리케이션의 자체 updater와 공식 지원 경로를 개발사가 의도한 대로 유지하기 쉽다.

### 4.4 정상 동작하는 기존 설치는 방식 통일만을 위해 변경하지 않는다

Homebrew cask로 설치한 GUI 애플리케이션이 정상적으로 동작한다면 공식 installer 방식과 통일하기 위한 목적으로만 재설치하지 않는다.

설치 방식을 바꾸면 다운로드와 재설치 비용이 발생하고 설정이나 사용자 data에 영향을 줄 수 있다. 기능 차이와 관리상 실익이 없다면 기존 관리 주체를 유지한다. 문제가 생기거나 Mac을 초기화할 때 [GUI 애플리케이션 설치 원칙](#43-gui-애플리케이션은-개발사가-의도한-관리-방식을-우선한다)의 기준으로 전환 여부를 다시 판단한다.

### 4.5 설치 전에 변경 범위와 제거 방법을 함께 확인한다

설치할 때 변경 범위와 제거 경로도 확인한다. 구체적인 확인 항목은 [설치 전 판단 순서](#51-설치-전-판단-순서)가 소유한다.

제거 방법을 미리 확인해 두면 사용하지 않는 프로그램을 나중에 추측으로 삭제하지 않아도 된다. 제거 경로를 확인할 수 없는 설치 방식은 관리 가능한 설치로 보지 않는다.

설치물이 놓이는 디렉토리의 배치 기준은 [디렉토리 관리 원칙](directory-management.md)이 소유한다. Homebrew 환경을 shell에 적용하는 방법, `.zprofile`과 `.zshrc`의 역할, `PATH` 책임 분리와 installer marker는 [Shell 설정 원칙](shell-configuration.md)이 소유한다.

### 4.6 자동 업데이트는 공식 updater와 Mac App Store에만 허용한다

GUI 애플리케이션이 공식 updater를 제공하면 해당 updater의 자동 업데이트를 허용한다. Mac App Store 앱은 Mac App Store 자동 업데이트를 허용한다. 개발사 또는 Apple이 배포와 검증을 함께 관리하는 경로이기 때문이다.

Homebrew와 language-specific package manager의 자동 업데이트는 사용하지 않는다. 수동 업데이트로 CLI, 개발 환경 구성 요소와 프로젝트 도구의 version 변경 시점을 직접 통제하고 변경 범위를 확인한다.

### 4.7 업데이트는 필요에 따라 관리 주체별로 수행한다

정기 일괄 업데이트를 기본으로 하지 않고 다음 우선순위에 따라 필요한 업데이트를 수행한다.

1. 보안 문제를 해결하는 업데이트
2. 사용 중인 기능의 버그를 해결하는 업데이트
3. 필요한 기능을 추가하는 업데이트
4. 일반적인 최신 version 유지 목적의 업데이트

Homebrew는 필요한 package만 업데이트한다. 전체 package를 함께 변경해야 할 이유가 있을 때만 일괄 업데이트한다.

### 4.8 제거할 때 사용자 data는 기본적으로 보존한다

프로그램 제거는 선택한 관리 주체의 제거 명령 또는 공식 uninstaller로 시작한다. 그다음 알려진 설정과 캐시, Login Item과 백그라운드 서비스를 확인해 더 이상 필요하지 않은 항목을 제거한다.

문서, 프로젝트 파일, 브라우저 data와 계정 관련 data처럼 다시 사용할 가능성이 있는 사용자 data는 기본적으로 보존한다. 완전 제거가 명확한 목적일 때만 대상과 복구 가능성을 확인한 뒤 사용자 data를 삭제한다.

애플리케이션 파일만 삭제한 채 관리 주체의 기록이나 백그라운드 서비스를 남기지 않으려면 설치할 때 확인한 제거 절차를 그대로 따른다.

### 4.9 Brewfile은 재설치 가치가 있는 CLI와 개발 구성 요소로 제한한다

Brewfile은 다음 대상을 같은 개발 환경에서 다시 설치할 필요가 있을 때 사용한다.

- CLI 도구
- 개발 환경 구성 요소
- 재설치 가치가 높은 Homebrew package

GUI 애플리케이션, 개인 취향에 가까운 앱과 자주 변경되는 앱은 기본적으로 기록하지 않는다. 공식 installer와 자체 updater를 따르는 편이 [GUI 애플리케이션 설치 원칙](#43-gui-애플리케이션은-개발사가-의도한-관리-방식을-우선한다)의 기준에 더 가깝기 때문이다.

Brewfile에는 실제로 Homebrew가 관리하는 package만 기록한다. 예를 들어 이 구성에서 Homebrew로 설치하지 않기로 한 Git을 formula로 기록하지 않는다. Brewfile에서 항목을 제거하는 것은 설치된 package를 제거하는 작업과 같지 않으므로 두 작업을 구분한다.

이 문서는 Brewfile의 포함과 제외 기준만 소유한다. 현재 머신의 실제 Brewfile과 설치 목록은 [README의 현재 범위 밖의 항목](README.md#현재-범위-밖의-항목)에 따라 저장소에서 관리하지 않는다.

### 4.10 검증되지 않은 설치 경로는 사용하지 않는다

비공식 다운로드 사이트, 출처를 확인할 수 없는 공유 파일과 검증되지 않은 직접 다운로드는 사용하지 않는다. 배포 주체와 업데이트 경로를 설명할 수 없고 파일 변조 여부를 신뢰할 수 없기 때문이다.

다음과 같이 원격 script를 바로 실행하는 방식도 기본적으로 사용하지 않는다.

```sh
curl https://<official-domain>/<installer-script> | sh
```

공식 프로젝트의 공식 문서가 해당 방식을 권장하고 실행 전에 script의 내용을 검토할 수 있을 때만 예외적으로 허용한다. 명령과 URL은 공식 문서에서 현재 값을 다시 확인한다.

직접 다운로드는 다음 조건을 모두 만족할 때 허용한다.

- 공식 사이트가 HTTPS로 제공한다.
- 공식 개발사가 배포한 파일임을 확인할 수 있다.
- macOS code signing 정보를 확인할 수 있다.
- checksum이 제공되면 다운로드한 파일의 값과 비교한다.
- release 페이지가 제공되면 대상 version과 파일명을 확인한다.

## 5. 설정 방법

### 5.1 설치 전 판단 순서

새로운 프로그램을 설치할 때 다음 순서를 반복한다.

1. 해결하려는 문제가 기존 도구의 기능과 겹치지 않는지 확인한다.
2. CLI, GUI 애플리케이션, 프로젝트 dependency 또는 전역 CLI 중 설치 대상의 종류를 정한다.
3. 개발사의 공식 문서에서 권장 설치 방법과 지원하는 업데이트 경로를 확인한다.
4. 기존 설치와 관리 주체가 있는지 [중복 설치 확인](#52-기존-설치와-관리-주체-확인) 절차로 확인한다.
5. 설치 파일과 실행 파일의 위치, shell과 `PATH` 변경, Login Item, 백그라운드 서비스, 설정과 캐시의 생성 위치를 확인한다.
6. 공식 제거 명령이나 uninstaller와 제거 후 남는 항목을 확인한다.
7. [도구 종류와 공식 배포 정책에 따른 설치 원칙](#41-도구-종류와-공식-배포-정책에-따라-설치-주체를-정한다)과 [GUI 애플리케이션 설치 원칙](#43-gui-애플리케이션은-개발사가-의도한-관리-방식을-우선한다)에 따라 관리 주체 하나를 선택한다.
8. Homebrew formula라면 [Brewfile 반영 기준](#54-brewfile-반영-판단)을 적용한다.

설치나 제거 명령은 도구 version에 따라 달라질 수 있으므로 실행 직전에 공식 문서를 다시 확인한다.

### 5.2 기존 설치와 관리 주체 확인

CLI는 같은 command가 여러 경로에 존재하는지 확인한다.

```sh
type -a <command>
```

출력 경로가 하나인지, 여러 경로가 있다면 어떤 package manager나 기본 도구가 각각의 파일을 설치했는지 확인한다.

Homebrew가 관리하는 formula와 cask는 각각 확인한다.

```sh
brew list --formula
brew list --cask
```

GUI 애플리케이션은 `/Applications`의 애플리케이션, Homebrew cask 목록, Mac App Store의 구매·설치 상태와 공식 installer의 관리 정보를 함께 비교한다. 공식 installer가 package receipt나 별도 manager를 사용하는지는 개발사 문서에서 확인한다.

Language-specific package manager의 전역 목록 확인 명령은 manager와 version에 따라 다르므로 해당 공식 문서를 확인한다. 프로젝트 dependency 목록과 전역 CLI 목록을 혼합하지 않는다.

### 5.3 선택한 관리 주체로 설치

Homebrew formula를 선택했다면 현재 Homebrew 공식 문서에서 package 이름을 확인한 뒤 설치한다.

```sh
brew install <formula>
```

Homebrew cask를 선택했다면 [GUI 애플리케이션 설치 원칙](#43-gui-애플리케이션은-개발사가-의도한-관리-방식을-우선한다)의 조건을 확인한 뒤 설치한다.

```sh
brew install --cask <cask>
```

공식 installer, Mac App Store와 직접 다운로드를 선택했다면 공식 배포 경로를 사용한다. 직접 다운로드는 [검증되지 않은 설치 경로를 사용하지 않는 원칙](#410-검증되지-않은-설치-경로는-사용하지-않는다)의 출처와 검증 조건을 먼저 확인한다.

전역 CLI를 language-specific package manager로 설치할 때는 프로젝트와 독립적인 도구인지, 개발사가 공식 설치 방법으로 제공하는지 확인한다. 실제 명령은 manager version에 따라 달라질 수 있으므로 공식 문서에서 다시 확인한다.

설치 과정에서 shell 환경이나 `PATH`를 변경해야 한다면 [Shell 설정 원칙](shell-configuration.md)의 `.zprofile`과 `.zshrc` 역할 분리 및 installer marker 기준을 적용한다.

### 5.4 Brewfile 반영 판단

Homebrew formula를 설치한 뒤 [Brewfile 포함·제외 기준](#49-brewfile은-재설치-가치가-있는-cli와-개발-구성-요소로-제한한다)을 적용하고 다음 형식으로 기록한다.

```ruby
brew "<formula>"
```

## 6. 검증

### 6.1 설치 출처와 관리 주체

설치 후 다음을 확인한다.

- 공식 installer, Homebrew, Mac App Store 또는 language-specific package manager 중 어떤 주체가 프로그램을 관리하는지 설명할 수 있다.
- 설치, 업데이트와 제거가 같은 주체로 이어진다.

CLI는 같은 command가 여러 경로에 존재하는지 확인한다.

```sh
type -a <command>
```

다음을 확인한다.

- 출력에서 경로가 하나인지 여러 개인지 구분된다.
- 여러 경로가 있다면 어떤 package manager나 기본 도구가 각각의 파일을 설치했는지 설명할 수 있다.

같은 프로그램을 의도하지 않게 Homebrew와 language-specific package manager 양쪽에서 관리하는 상태를 정상으로 보지 않는다.

Homebrew package는 선택한 유형에 맞게 관리 목록에 나타나는지 확인한다.

```sh
brew list --versions <formula>
brew list --cask
```

다음을 확인한다.

- formula는 package 이름과 version이 출력된다.
- cask는 설치한 cask 이름이 목록에 나타난다.

GUI 애플리케이션은 다음을 확인한다.

- `/Applications`, Homebrew cask 목록과 Mac App Store 설치 상태가 선택한 관리 주체와 일치한다.
- 공식 installer와 Homebrew cask 양쪽에서 설치했거나 이름이 같은 애플리케이션이 둘 이상이면 각각의 설치 출처를 설명할 수 있다.

의도하지 않은 중복이나 관리 주체 불일치는 [관리 주체 변경](#74-관리-주체-변경) 절차를 따른다.

### 6.2 CLI 실행

CLI는 실행 경로와 version을 확인한다.

```sh
command -v <command>
<command> --version
```

다음을 확인한다.

- 실행 경로가 선택한 관리 주체의 경로와 일치한다.
- version 정보가 출력된다.

실행 경로가 선택한 관리 주체와 일치하지 않으면 [관리 주체 변경](#74-관리-주체-변경) 절차를 따른다. version 확인 option은 프로그램마다 다를 수 있으므로 공식 문서를 확인한다.

### 6.3 GUI 애플리케이션과 직접 다운로드

GUI 애플리케이션은 다음을 확인한다.

- 정상적으로 실행된다.
- updater 또는 Mac App Store가 선택한 업데이트 정책과 일치한다.
- 권한 요청, Login Item과 백그라운드 서비스가 설치 전에 확인한 범위를 벗어나지 않는다.

직접 다운로드한 애플리케이션은 macOS code signing과 실행 허용 상태를 확인한다.

```sh
codesign --display --verbose=4 "/Applications/<application-name>.app"
spctl --assess --type execute --verbose=4 "/Applications/<application-name>.app"
```

다음을 확인한다.

- 서명 주체를 식별할 수 있다.
- macOS 평가에서 허용되는 형태다.

macOS version에 따라 출력과 option이 달라질 수 있으므로 Apple 공식 문서에서 현재 명령을 다시 확인한다.

공식 checksum이 제공되면 다운로드한 파일의 값을 계산해 공식 값과 정확히 비교한다.

```sh
shasum -a 256 <downloaded-file>
```

출력되는 digest가 공식 배포 페이지의 값과 일치해야 한다.

### 6.4 설치로 변경된 항목

설치 전에 확인한 내용과 실제 변경 결과를 비교한다.

- 실행 파일과 애플리케이션 위치가 예상과 일치한다.
- shell 환경과 `PATH` 변경은 [Shell 설정 원칙](shell-configuration.md)의 책임에 맞게 배치되어 있다.
- Login Item과 백그라운드 서비스는 프로그램 동작에 필요한 항목만 존재한다.
- 설정과 캐시가 공식 문서가 설명하는 위치에 생성된다.
- 예상하지 못한 system-wide 설정 변경이 없다.

shell 환경이나 `PATH` 배치가 책임과 일치하지 않으면 [Shell 설정 원칙의 설정 방법](shell-configuration.md#5-설정-방법)을 따른다.

### 6.5 업데이트와 제거 가능성

다음을 확인한다.

- 공식 updater, Mac App Store 또는 수동 package manager 명령 중 사용할 업데이트 경로를 설명할 수 있다.
- 같은 관리 주체가 제공하는 제거 명령이나 공식 uninstaller를 확인할 수 있다.

제거 방법을 찾을 수 없거나 관리 주체를 설명할 수 없다면 설치 검증이 끝난 것으로 보지 않는다.

업데이트 경로가 불분명하면 [업데이트 수행](#71-업데이트-수행), 제거 경로가 불분명하면 [프로그램 제거](#73-프로그램-제거) 절차를 따른다.

### 6.6 Brewfile 반영

[Brewfile 포함·제외 기준](#49-brewfile은-재설치-가치가-있는-cli와-개발-구성-요소로-제한한다)에 맞는 선언만 Brewfile에 포함되어 있는지 확인한다.

Brewfile 선언이 기준과 일치하지 않으면 [Brewfile 반영 판단](#54-brewfile-반영-판단) 절차를 따른다.

실제 설치 상태와 Brewfile 선언은 서로 다른 대상이다. Brewfile에서 formula를 지운 것만으로 package가 제거되었다고 판단하지 않는다.

## 7. 이후 사용 및 유지보수

### 7.1 업데이트 수행

자동 업데이트 여부에는 [자동 업데이트 원칙](#46-자동-업데이트는-공식-updater와-mac-app-store에만-허용한다)을 적용한다. 업데이트 대상과 시점에는 [관리 주체별 업데이트 원칙](#47-업데이트는-필요에-따라-관리-주체별로-수행한다)을 적용한다.

Homebrew package를 업데이트할 때는 현재 package 정보를 갱신한 뒤 outdated 목록을 확인한다.

```sh
brew update
brew outdated
```

formula 또는 cask를 선택해 업데이트한다.

```sh
brew upgrade <formula>
brew upgrade --cask <cask>
```

전체 Homebrew package를 업데이트하는 명령은 다음과 같다.

```sh
brew upgrade
```

프로젝트 dependency와 runtime version 변경 절차는 [개발환경 구성 원칙](development-environment.md)에서 확인한다. 전역 CLI는 language-specific package manager의 공식 문서에서 현재 업데이트 명령과 변경 범위를 확인한 뒤 실행한다.

### 7.2 업데이트 전후 확인

업데이트 전에는 release 정보와 변경 범위를 확인하고 보안 문제, 사용 중인 버그, 필요한 기능 중 어떤 이유로 변경하는지 구분한다.

업데이트 후에는 [검증](#6-검증)을 반복한다. CLI는 실행 경로와 version을, GUI 애플리케이션은 실행과 updater 상태를 확인한다. shell 환경이나 `PATH`가 변경되었다면 [Shell 설정 원칙](shell-configuration.md)의 검증도 함께 수행한다.

### 7.3 프로그램 제거

먼저 설치 주체를 확인하고 같은 주체의 제거 경로를 사용한다. Homebrew가 관리하는 package는 유형에 맞는 명령으로 제거한다.

```sh
brew uninstall <formula>
brew uninstall --cask <cask>
```

공식 installer로 설치한 프로그램은 개발사가 제공하는 uninstaller 또는 공식 제거 절차를 사용한다. Mac App Store 앱과 language-specific package manager의 제거 방법도 각 공식 문서에서 현재 절차를 확인한다.

기본 제거 후에는 설정과 캐시도 검토하되 해당 프로그램이 만든 것으로 확인된 항목만 살핀다. 다음 경로는 구조를 설명하기 위한 대체 표기이며 실제 경로와 파일명은 프로그램의 공식 문서에서 확인한다.

```text
~/Library/Application Support/<application-name>
~/Library/Caches/<application-name>
~/Library/Preferences/<application-identifier>.plist
```

시스템 설정의 로그인 항목과 프로그램이 등록한 LaunchAgent 또는 LaunchDaemon도 확인한다. 다른 프로그램이 함께 사용하는 항목인지 확인하지 않은 상태에서 삭제하지 않는다.

문서, 프로젝트 파일, 브라우저 data와 계정 관련 data는 기본적으로 보존한다. 완전 제거가 목적일 때만 삭제 대상을 명시하고 필요한 data의 backup과 복구 가능성을 확인한 뒤 처리한다.

### 7.4 관리 주체 변경

정상 동작하는 설치는 관리 방식 통일만을 위해 변경하지 않는다. 문제 해결, 지원 종료 또는 Mac 초기화처럼 전환할 이유가 생기면 다음 순서로 관리 주체를 바꾼다.

1. 기존 관리 주체와 사용자 data 위치를 확인한다.
2. 기존 관리 주체의 공식 절차로 프로그램을 제거한다.
3. 실행 파일과 GUI 애플리케이션이 중복으로 남지 않았는지 확인한다.
4. [설치 전 판단 순서](#51-설치-전-판단-순서)에 따라 새 관리 주체를 정한다.
5. 설치 후 [검증](#6-검증)을 수행한다.

### 7.5 유지보수 기준

- 새 도구를 설치하기 전에 [설치 전 판단 순서](#51-설치-전-판단-순서)를 따른다.
- 업데이트와 제거는 설치에 사용한 관리 주체에서 수행한다.
- 사용하지 않는 프로그램은 제거 방법과 남는 항목을 확인한 뒤 정리한다.
- Brewfile은 [Brewfile 포함·제외 기준](#49-brewfile은-재설치-가치가-있는-cli와-개발-구성-요소로-제한한다)에 맞게 유지한다.
- 설치 방식이나 명령이 바뀔 수 있는 항목은 실행 전에 공식 문서를 다시 확인한다.
- 변경 후에는 [검증](#6-검증)을 반복한다.

## 8. 현재 범위 밖의 항목

- 현재 머신의 설치 애플리케이션과 CLI 목록: README가 현재 상태와 머신 고유 정보를 관리 대상에서 제외하므로 이 문서는 선택 기준만 기록한다.
- 실제 Brewfile 파일과 현재 package 선언: [Brewfile 포함·제외 기준](#49-brewfile은-재설치-가치가-있는-cli와-개발-구성-요소로-제한한다)만 이 문서가 소유하고 실제 내용은 현재 머신의 설치 목록이므로 저장소에서 관리하지 않는다.
- runtime version 관리와 프로젝트 dependency 격리: 도구 종류에 따른 설치 주체만 이 문서에서 정하고 상세 구성은 [개발환경 구성 원칙](development-environment.md)에 위임한다.
- 설치물이 놓이는 디렉토리 배치: 설치 전 위치를 확인한다는 기준만 두고 배치 원칙은 [디렉토리 관리 원칙](directory-management.md)에 위임한다.
- Homebrew 환경의 shell 적용, `.zprofile`과 `.zshrc` 배치, `PATH` 책임 분리와 installer marker: [Shell 설정 원칙](shell-configuration.md)에 위임한다.
- Git 설치 여부: 일반적인 중복 설치와 관리 주체 기준만 제공하며 개별 결정은 [Git과 GitHub SSH 설정 원칙](git-and-ssh.md)이 소유한다.
- package 설치·업데이트·삭제 자동화와 bootstrap: 현재는 수동 절차와 안전 조건을 먼저 관리하며 반복 자동화가 실제로 필요해질 때 별도 책임으로 검토한다.

## 9. 핵심 요약

```text
CLI 또는 개발 환경 구성 요소
└── Homebrew formula

GUI 애플리케이션
└── 공식 권장 방식 → 공식 installer → Mac App Store → Homebrew cask

프로젝트 dependency
└── 프로젝트 package manager

프로젝트와 독립적인 전역 CLI
└── 공식 language-specific package manager

직접 다운로드
└── 공식 출처 + HTTPS + code signing + 제공되는 검증 정보

관리 주체 하나
└── 설치 → 검증 → 업데이트 → 제거
```

- [도구 종류와 공식 배포 정책에 따라 설치 주체를 정한다](#41-도구-종류와-공식-배포-정책에-따라-설치-주체를-정한다)
- [하나의 프로그램에는 관리 주체를 하나만 둔다](#42-하나의-프로그램에는-관리-주체를-하나만-둔다)
- [GUI 애플리케이션은 개발사가 의도한 관리 방식을 우선한다](#43-gui-애플리케이션은-개발사가-의도한-관리-방식을-우선한다)
- [정상 동작하는 기존 설치는 방식 통일만을 위해 변경하지 않는다](#44-정상-동작하는-기존-설치는-방식-통일만을-위해-변경하지-않는다)
- [설치 전에 변경 범위와 제거 방법을 함께 확인한다](#45-설치-전에-변경-범위와-제거-방법을-함께-확인한다)
- [자동 업데이트는 공식 updater와 Mac App Store에만 허용한다](#46-자동-업데이트는-공식-updater와-mac-app-store에만-허용한다)
- [업데이트는 필요에 따라 관리 주체별로 수행한다](#47-업데이트는-필요에-따라-관리-주체별로-수행한다)
- [제거할 때 사용자 data는 기본적으로 보존한다](#48-제거할-때-사용자-data는-기본적으로-보존한다)
- [Brewfile은 재설치 가치가 있는 CLI와 개발 구성 요소로 제한한다](#49-brewfile은-재설치-가치가-있는-cli와-개발-구성-요소로-제한한다)
- [검증되지 않은 설치 경로는 사용하지 않는다](#410-검증되지-않은-설치-경로는-사용하지-않는다)
