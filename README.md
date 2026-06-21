# Pokémon Champions PC 무선 실행기 (Pokémon Champions PC Launcher)

[한글 (Korean)](#한글-사용-설명서) | [English](#english-user-guide)

---

## 한글 사용 설명서

이 패키지는 스마트폰에서 구동되는 **포켓몬 챔피언스(Pokémon Champions)** 게임을 PC 화면에 고해상도 독립 창으로 미러링하여 키보드와 마우스로 무선 플레이할 수 있도록 돕는 전용 런처입니다.

## 📥 최신 버전 다운로드 (v1.0.0)
아래 링크에서 런처 패키지 zip 파일을 무료로 다운로드하실 수 있습니다. 다운로드 후 압축을 풀어 사용하세요:
👉 **[Pokémon Champions PC Standalone Package 다운로드 (ZIP)](https://github.com/DOHA1012/pokemon-champions-pc/releases/download/v1.0.0/Pokemon_Champions_PC.zip)**

### ✨ 주요 핵심 기능
* **화면 해상도 다중 지원**: 720p부터 4K(3840x2160)까지 다양한 해상도 지원 (2K/4K 무선 스트리밍은 기기 성능 및 공유기 대역폭에 따라 렉이 발생할 수 있습니다.)
* **테두리 없는 전체화면 모드**: 타이틀 바를 숨기고 화면을 꽉 차게 띄워 몰입감을 높여줍니다.
* **폰 화면 자동 끄기 & 연결 유지 (Stay Awake)**: 게임 구동 시 폰의 실제 화면(액정)은 배터리 및 발열 방지를 위해 자동으로 꺼지고, 플레이 중에는 폰이 대기 상태로 잠들지 않도록 제어합니다.
* **기기 자동 깨우기 및 잠금 해제**: 실행 즉시 폰의 화면을 자동으로 켜고 잠금 화면을 진입해 줍니다.

---

### 📂 폴더 구성 정보
압축 해제 시 다음과 같은 폴더 구조로 이루어져 있습니다:
* 📄 **Pokémon Champions.exe** - 사용자 실행용 GUI 프로그램 (더블 클릭하여 실행)
* 📁 **bin** - 실행에 필요한 핵심 엔진 폴더 (수정하거나 삭제하지 마세요)
  * 📁 `adb` - 안드로이드 연결용 통신 엔진
  * 📁 `scrcpy` - 화면 송출 및 가상 창 생성 엔진

---

### 🚀 사용 및 연결 방법

#### 1단계: 스마트폰 사전 설정 (최초 1회 필수)
1. 스마트폰 **설정** ➡️ **휴대폰 정보** ➡️ **소프트웨어 정보**로 이동합니다.
2. **빌드 번호** 항목을 **7번 연속**으로 연타하여 개발자 옵션을 활성화합니다.
3. 설정 메인 화면으로 돌아와 맨 아래의 **개발자 옵션**으로 들어갑니다.
4. **USB 디버깅** 항목을 찾아서 **활성화(켬)** 상태로 켭니다.

#### 2단계: PC와 무선 연결 자동 설정
1. PC와 스마트폰을 **동일한 와이파이 공유기**에 연결합니다.
2. 스마트폰을 **USB 케이블로 PC에 연결**합니다.
   * *이때 스마트폰 화면에 "USB 디버깅을 허용하시겠습니까?" 팝업이 뜨면 **"이 컴퓨터에서 항상 허용"**에 체크하고 **[허용]**을 누릅니다.*
3. **`Pokémon Champions.exe`**를 더블 클릭하여 실행합니다.
4. 프로그램 창 중간의 **`★ USB 기기로 무선 연결 자동 설정`** 버튼을 누릅니다.
5. "자동 설정이 완료되었습니다" 팝업이 뜨면 **USB 케이블을 분리(해제)**합니다. (이제 무선으로 연결됩니다.)

#### 3단계: 무선 게임 실행
1. 프로그램 창 상단의 기기 선택 목록에서 무선 기기(`192.168.x.x:5555`)가 선택되어 있는지 확인합니다.
2. **3. 해상도 및 화면 설정**에서 원하는 가상 창 해상도와 테두리 없는 전체화면 여부를 지정합니다.
3. 맨 하단의 초록색 **`포켓몬 챔피언스 실행 (PC 독립 창)`** 버튼을 누릅니다.
4. 잠시 후 스마트폰의 화면이 켜지며 게임이 자동 구동되고, PC 화면에는 독립된 고화질 게임 창이 생성됩니다. (스마트폰의 실제 화면은 실행 즉시 꺼집니다.)

---

### 🛠️ 문제 해결 (FAQ)

#### Q. 스마트폰을 껐다 켰더니 연결이 안 됩니다.
안드로이드 보안 정책상 폰을 재부팅하면 무선 포트가 닫힙니다. 
* **해결책:** 폰을 다시 USB 케이블로 PC에 연결한 뒤, 실행기를 켜고 **`★ USB 기기로 무선 연결 자동 설정`** 버튼을 다시 한번 눌러주시면 무선 포트가 재개방됩니다.

#### Q. 와이파이 IP 주소가 변경되어 연결이 끊겼습니다.
폰이 다른 와이파이에 연결되었거나 공유기가 재시작되어 IP가 바뀔 수 있습니다.
* **해결책:** 폰 설정의 와이파이 세부 정보에서 바뀐 IP를 확인한 뒤, 실행기의 **무선 IP 주소** 칸에 직접 입력하고 **`무선 연결`** 버튼을 눌러주시면 연결됩니다.

#### Q. 실행 후 직접 폰 전원 버튼을 눌러 화면을 끄면 PC 화면도 꺼집니다.
* **이유**: 안드로이드 OS는 사용자가 물리 전원 버튼을 누르는 순간 렌더링 엔진 자체를 일시 정지시킵니다.
* **해결책**: 런처가 스마트폰의 실제 화면(액정)을 자동으로 꺼주기 때문에, 실행 후에는 **전원 버튼을 직접 누르지 마시고 그대로 폰을 냅두시면 됩니다.**

---
---

## English User Guide

This package is a dedicated launcher designed to mirror **Pokémon Champions** running on an Android device onto a high-resolution, independent PC window, allowing wireless gameplay with a keyboard and mouse.

## 📥 Download Latest Version (v1.0.0)
You can download the launcher package zip file for free from the link below. Extract and run it:
👉 **[Download Pokémon Champions PC Standalone Package (ZIP)](https://github.com/DOHA1012/pokemon-champions-pc/releases/download/v1.0.0/Pokemon_Champions_PC.zip)**

### ✨ Core Features
* **Expanded Resolutions**: Supports resolutions from 720p up to 4K (`3840x2160`, `2560x1440`, `1920x1080`, `1600x900`, `1280x720`, `960x540`).
* **Borderless Fullscreen**: Hides the title bar and stretches the window to full screen for immersive play.
* **Physical Screen Off & Stay Awake**: The phone's screen automatically goes black upon launch to save battery and prevent burn-in, while preventing the device from falling asleep during mirroring.
* **Display Wakeup & Unlock**: Automatically turns on the phone screen and attempts to bypass the lock screen on startup.

---

### 📂 Folder Structure
When extracted, the folder structure is organized as follows:
* 📄 **Pokémon Champions.exe** - The main GUI launcher program (Double-click to run).
* 📁 **bin** - Core engine folder (Do not modify or delete).
  * 📁 `adb` - Android connection engine.
  * 📁 `scrcpy` - Mirroring and virtual window engine.

---

### 🚀 How to Run

#### Step 1: Setup Android Phone (First Time Only)
1. Go to **Settings** ➡️ **About phone** ➡️ **Software information** on your smartphone.
2. Tap **Build number** **7 times** consecutively to enable Developer options.
3. Return to the main Settings menu and tap **Developer options** at the bottom.
4. Locate **USB debugging** and toggle it **ON**.

#### Step 2: Configure Wireless Connection Automatically
1. Connect both your PC and smartphone to the **same Wi-Fi router**.
2. Connect the smartphone to your PC using a **USB cable**.
   * *If the phone prompts "Allow USB debugging?", check **"Always allow from this computer"** and tap **[Allow]**.*
3. Double-click **`Pokémon Champions.exe`** to launch it.
4. Click the **`★ USB 기기로 무선 연결 자동 설정`** button in the middle.
5. Once the setup completes, **disconnect the USB cable**. (The device is now connected wirelessly.)

#### Step 3: Launch Pokémon Champions Wirelessly
1. Make sure your wireless device (`192.168.x.x:5555`) is selected in the device dropdown list at the top.
2. Configure your desired resolution and toggle Borderless Fullscreen under **3. Resolution & Window Settings**.
3. Click the green **`포켓몬 챔피언스 실행 (PC 독립 창)`** button at the bottom.
4. The smartphone's screen will wake up and run the game, while a high-definition window displays on your PC. (The physical phone display will go black automatically.)

---

### 🛠️ Troubleshooting (FAQ)

#### Q. I rebooted my phone, and it won't connect anymore.
Due to Android security policies, wireless ports close when the phone is rebooted.
* **Solution:** Re-connect the phone to your PC via USB cable, open the launcher, and click the **`★ USB 기기로 무선 연결 자동 설정`** button again to re-open the wireless port.

#### Q. The Wi-Fi IP address changed, and connection was lost.
This happens if your phone connects to a different Wi-Fi network or the router reboots.
* **Solution:** Find the new IP address in your phone's Wi-Fi details, enter it into the **Wireless IP** field, and click **`무선 연결`** (Wireless Connect) to reconnect.

#### Q. When I press the phone's physical power button, the PC mirroring window turns off.
* **Reason**: Android OS pauses all GPU rendering when the physical power button is pressed.
* **Solution**: The launcher automatically turns off the physical phone screen on startup. **Do not press the power button; just leave the phone as it is.**
