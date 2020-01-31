# ga:userActivty

### Usage
- 아래의 명령어로 패키지를 설치합니다.
  ```sh
  $ sh install.sh
  ```
- `data.csv`라는 파일명으로 ga에서 **audience - user-exeplorer**에서 내보내기로 파일들을 가져옵니다. 파일이 여러개가 필요하다면 csv파일 로딩하는 코드만 조금 수정해주세요.
  - 사용자 목록을 api로 받아오는 방법만 알면 충분히 자동화시킬 수 있는 부분입니다.
- `client_secrets.json`이라는 파일명으로 google developers console에서 **사용자 인증 정보 - 사용자 인증 정보 만들기 - OAuth 클라이언트 ID - 기타**로 id를 만들어, 다운받습니다.
- 아래와 같은 명령어로 파일을 실행합니다.
  ```sh
  $ python index.py --noauth_local_webserver
  ```
- 콘솔에 찍히는 링크로 들어가서 시키는대로 인증키를 생성해 붙여넣습니다.
  ```sh
  Go to the following link in your browser:

      https://accounts.google.com/o/oauth2/auth?client_id=<client_id>&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fanalytics.readonly&access_type=offline&response_type=code
  ```
- 아래의 인증키를 입력하면, `credentials.dat`파일이 생성됩니다.
  ```sh
  Enter verification code: foo_bar_faz
  ```

### Process
- 인증키로 새로운 인증키를 만듭니다.
- 클라이언트 id가 들어있는 csv파일을 이용해 사용자 활동을 얻어냅니다.