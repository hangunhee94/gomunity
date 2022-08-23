# :pushpin: Gomunity
![gomunity_og](https://user-images.githubusercontent.com/97969957/185279549-76daa3f9-50dc-4eb7-b412-2f9faec1c2b3.png)
>초보 개발자들의 커뮤니티, 거뮤니티    
>https://github.com/hangunhee94/gomunity   

</br>

## 1. 제작 기간 & 참여 인원
- 2022년 7월 18일 ~ 8월 16일(진행중)    
- 팀 프로젝트
- 4인  

</br>

## 2. 사용 기술
#### `Back-end`
  - Django
  - DRF
  - PostgreSQL
  - Docker

#### `Front-end`
  - HTML5
  - CSS3
  - JavaScript
  
#### `배포` 
  - EC2
  - S3
  - CloudFront
  - Route53 
</br>

## 3. 핵심 기능
>이 프로젝트의 핵심 기능은 개발자의 길에 들어선 <b>주니어개발자들의 소통 공간</b>입니다.   
>사용자는 주니어 개발자들의 개발에 대한 질문들을 알아볼 수 있고, 알고있는 것에 대하여 답을 줄 수 있습니다.      
>개발 공부를 하면서 알게된 꼭 나와 같은 초보들에게 공유하고 싶은 팁을 게시하는 자료게시판 또한 있어    
>누구나 초보였던 시절에 불편했던 일들을 해결했던 자료를 공유하여 쉽게 찾을 수 있는 레퍼런스가 되기를 희망합니다.   

### 3.1. 아키텍쳐   
![image](https://user-images.githubusercontent.com/97969957/185283041-45f4504d-e797-4714-9d7e-058568c20f8d.png) 


#### 서버

- EC2 안 nginx,gunicorn/django,postgreSQL이 도커를 통해 이미지로 빌드
- Lets Encrypt를 사용하여 443포트로 열린 HTTPS 도메인 배포
- 도메인 : Route 53

#### 프론트엔드

- 정적배포 : S3
- AWS CloudFront으로 AWS SSL 인증서가 적용된 HTTPS 도메인 배포
- 도메인 : Gabia  

### 3.2. ERD    
![Gomunity](https://user-images.githubusercontent.com/97969957/185282933-80713a8e-cdf6-47c4-ba20-ef985fddf0d0.png)  

  - 회원 모델
  - 질의응답 게시글/답글/좋아요 모델
  - 자료게시판 게시글/답글/카테고리/좋아요 모델
<br>

<details>
<summary><b> Service Flow</b></summary>  

<div markdown="1">

### 회원기능

![회원가입](https://user-images.githubusercontent.com/97969957/185279221-5abe2894-0fd2-4636-8023-a467a292a2d6.gif)

- 사용자는 거뮤니티의 게시글을 열람할 수 있습니다. 그러나, 작성/수정/삭제/좋아요 등의 기능은 로그인을 요구합니다.
- 사용자는 회원가입 페이지에서 아이디,비밀번호,닉네임,이메일을 입력하고 회원가입합니다.
  - 아이디,비밀번호,이메일은 작성조건이 있어 작성조건이 일치하지 않는다면 오류를 표시합니다.

![로그인 및 게시판](https://user-images.githubusercontent.com/97969957/185279234-26e622ee-b357-4830-9792-d0a63abe1336.gif)

- 사용자는 아이디 비밀번호를 입력하고 로그인합니다.
  - 로그인한 사용자는 DRF Simple JWT로 토큰이 브라우저 로컬 스토리지에 저장됩니다.
  - 사용자는 약 15분간 한 번 로그인한 상태를 유지하며, 새로고침을 통해서 토큰을 60일까지 저장합니다.

### 질의응답게시판

![게시글 등록](https://user-images.githubusercontent.com/97969957/185279026-1c6a22e1-b005-496e-977e-3940c4707a37.gif)

- 사용자는 질의응답게시판을 통해서 개발과 관련된 주제로 자유롭게 질문하고 답변할 수 있습니다.
- 사용자는 질의응답게시판에 작성된 글을 열람할 수 있습니다.
- 사용자는 질의응답게시판의 글 및 답변의 작성/수정/삭제/좋아요 기능은 로그인을 통해서만 접근할 수 있습니다.
- 사용자는 게시글 작성 버튼을 눌러 질문하고 싶은 내용을 담아 글을 작성합니다.
  - 해시태그를 작성하여 이 후 게시글을 추천하는 용도로 활용됩니다.
  - TOAST UI EDITOR가 적용되어 있어 마크다운 형식으로 글을 작성하거나 이미지를 업로드 할 수 있습니다.
- 사용자는 자신이 작성한 글에 대해 수정/삭제 권한이 있으며 버튼으로 표시됩니다.
  - 수정 버튼을 눌러 작성된 제목/해시태그/내용 등이 에디터 안에 표시되며 글을 수정할 수 있습니다.
  - 삭제 버튼을 눌러 작성한 글 레코드를 삭제합니다.
- 사용자는 게시글에 제목 밑의 좋아요 버튼을 클릭하여 좋아요 기능을 사용할 수 있습니다.
  - 좋아요 된 버튼은 모양이 변경되며, 다시 한 번 클릭하면 좋아요가 취소됩니다.
- 사용자는 게시글에 답글을 작성할 수 있습니다.
  - 텍스트를 입력하고 작성버튼을 눌러 답글을 작성할 수 있습니다.
- 사용자는 자신이 작성한 답글에 대해 수정/삭제 권한이 있으며 버튼으로 표시됩니다.
  - 수정 버튼을 눌러 작성된 내용이 인풋에 표시되며 답글을 수정할 수 있습니다.
  - 삭제 버튼을 눌러 작성한 답글 레코드를 삭제합니다.

![게시글추천](https://user-images.githubusercontent.com/97969957/185279067-0d0505ee-fea5-4667-ab82-bc58cbaf9043.gif)

- 사용자는 게시글을 조회 페이지에서 추천받기 버튼을 눌러 유사한 해시태그를 가진 게시글을 추천받을 수 있습니다.

### 자료게시판

![자료게시판](https://user-images.githubusercontent.com/97969957/185283883-96c75c91-1fb8-47a9-9d7d-4faf16956633.gif)

- 사용자는 자료게시판을 통해서 개발하면서 알게 된 팁을 글을 작성하여 공유할 수 있습니다.
- 사용자는 자료게시판의 글 및 답글의 조회가 가능합니다.
- 사용자는 자료게시판의 글 및 답글의 작성/수정/삭제/좋아요 기능을 로그인을 통해서 접근할 수 있습니다.
- 사용자는 게시글 작성 버튼을 눌러 질문하고 싶은 내용을 담아 글을 작성합니다.
  - 카테고리를 중 공용 및 특정 권한 전용 하나를 선택하여, 열람권한을 정합니다.
  - 해시태그를 작성하여 이 후 게시글을 추천하는 용도로 활용됩니다.
  - TOAST UI EDITOR가 적용되어 있어 마크다운 형식으로 글을 작성하거나 이미지를 업로드 할 수 있습니다.
- 사용자는 자신이 작성한 글에 대해 수정/삭제 권한이 있으며 버튼으로 표시됩니다.
  - 수정 버튼을 눌러 작성된 제목/해시태그/내용 등이 에디터 안에 표시되며 글을 수정할 수 있습니다.
  - 삭제 버튼을 눌러 작성한 글 레코드를 삭제합니다.
- 사용자는 게시글에 제목 밑의 좋아요 버튼을 클릭하여 좋아요 기능을 사용할 수 있습니다.
  - 좋아요 된 버튼은 모양이 변경되며, 다시 한 번 클릭하면 좋아요가 취소됩니다.
- 사용자는 게시글에 답글을 작성할 수 있습니다.
  - 텍스트를 입력하고 작성버튼을 눌러 답글을 작성할 수 있습니다.
- 사용자는 자신이 작성한 답글에 대해 수정/삭제 권한이 있으며 버튼으로 표시됩니다.
  - 수정 버튼을 눌러 작성된 내용이 인풋에 표시되며 답글을 수정할 수 있습니다.
  - 삭제 버튼을 눌러 작성한 답글 레코드를 삭제합니다.
</div>
</details>

---

### 버전 별 SA

---

### ver.1.0  [상세 내용 참고](https://www.notion.so/Starting-Assignment-a93d84d8a6a0455abff9975c2de1313f)

### ver.1.1  [상세 내용 참고](https://www.notion.so/Starting-Assignment-a93d84d8a6a0455abff9975c2de1313f)

### ver.1.2  [상세 내용 참고](https://www.notion.so/Starting-Assignment-dcdf8dc5fef84f25975c3cd28c95dc7e)

### ver.1.2.1  [상세 내용 참고](https://www.notion.so/VER-1-2-1-5e0e1cf5477d484fb8808eb0fc444589)

### ver.1.3  [상세 내용 참고](https://www.notion.so/VER-1-3-e9dbd0b5b1ba4947b4744b876b6f9300)

### ver.1.4  [상세 내용 참고](https://www.notion.so/VER-1-4-4c8099f4818841499e3fb36e8a2ffff9)


## 4. 핵심 트러블 슈팅
### 4.1. QueryDict is Immutable
>게시글을 작성하는 post 메서드 API를 작성한 뒤, POSTMAN으로 테스트까지 마쳤다.<br>
>테스트코드를 공부하면서 적용해보기 위해서 테스트코드를 작성했는데, 테스트코드가 view의 코드를 참조하는 도중 에러가 발생하면서 테스트가 실패하였고,      
>여전히 서버 코드를 실행하는데 있어서는 문제가 없지만, 테스트코드는 제대로 작동하지 않는 상태이다

> 해당 오류는 QueryDict가 변경할 수 없는  자료형(immutable) 이라고 한다.
> 오류코드를 Stacktrace 해보니, views.py에서 [request.data](http://request.data) 가 QueryDict였다.
> QueryDict는 Immutable 자료형이기 때문에 테스트코드는 중간에 request.user라는 데이터를 새로운 키로 삽입할 수 없다는 것이었다!
> 하지만, 서버에서는 정상적으로 작동하지만,
> 일단 테스트코드의 오류를 해결하기 위해서 mutable의 자료형으로 새로 가져오기로 했다     
<details>
<summary><b>기존 코드</b></summary>  
<div markdown="1">

````

def post(self, request):
    request.data['user'] = request.user.id
    notice_serializer = NoticeSerializer(data=request.data)	
                 ...
		생략
        
````

</div>
</details>

<details>
<summary><b>개선된 코드</b></summary>  
<div markdown="1">

````

def post(self, request):
	print(request.data) # 테스트코드 상에서 QueryDict인 request.data에서 사용할 수 있는 메서드 확인
	request_data_copy = request.data.copy() # mutable 한 딕셔너리로 카피하는 메서드
	request_data_copy['user'] = request.user.id
	notice_serializer = NoticeSerializer(data=request_data_copy)
                ...
		생략
        
````

</div>
</details>

> 결과적으로 copy 메서드를 사용함으로 test 코드까지 잘 통과 되는 것을 확인할 수 있었습니다.
> 만약 immutable QueryDict를 받는다면, 수정하지 않고 데이터를 삽입하여도 된다라고 보았습니다.

</br>

## 5. 그 외 트러블 슈팅    
### 5.1. DRF 시리얼라이저 쿼리셋과 many=True
>DRF의 시리얼라이저를 통해서 데이터를 리턴해주려고 했는데 문제가 발생.<br>
>시리얼라이저에 담아주고 싶은 데이터는 objects.all() 을 사용한 쿼리셋 데이터 형식.    

    
>쿼리셋 오브젝트(다수의 오브젝트)는 제목이라는 속성이 없다. <br>
>하나의 오브젝트에는 해당 속성이 있겠지만, 여러 개를 바라본다면 제대로 참조 할 수 없다.    

>단일 오브젝트가 아닌, 여러 개의 오브젝트인 쿼리셋을 받아주려면 many=True 를 추가로 작성해주어야 한다고 한다.     

<details>
<summary><b>기존 코드</b></summary>  
<div markdown="1">

````

.. 생략

class View(APIView):
	def get(self, request):
		notices = NoticeModel.objects.all()
		notice_serializer = NoticeSerializer(data=notices).data
		return Response(notice_serializer)
````

</div>
</details>

<details>
<summary><b>개선된 코드</b></summary>  
<div markdown="1">

````

.. 생략

class View(APIView):
	def get(self, request):
		notices = NoticeModel.objects.all()
		notice_serializer = NoticeSerializer(data=notices).data
		return Response(notice_serializer, many=True)
        
````

</div>
</details> 

>시리얼라이저로 보내주는 데이터가 여러 개의 오브젝트인 쿼리셋이었고,  
>쿼리셋을 넘겨주기 위해서는 many=True 를 추가로 작성하여 해결하였다.

</br>

## 6. 회고 / 느낀점
>프로젝트 개발 회고 글: https://hee94.tistory.com/77 

---
