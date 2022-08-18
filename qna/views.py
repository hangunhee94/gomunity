from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import filters



from .models import (
    QnAQuestion as QnAQuestionModel,
    QuestionLike as QuestionLikeModel,
    AnswerLike as AnswerLikeModel
                     )
from .serializers import QuestionSerializer, AnswerSerializer, QnAAnswerModel

from .upload import upload_s3, upload_thumbnail_s3
import datetime

from .deep_learning import return_five_recommends


# 이미지 이름변경 함수
def change_naming(origin_image, username):
    origin_image = origin_image.replace(" ","_")
    now = datetime.datetime.now()
    now = now.strftime('%Y%m%d_%H%M%S')
    key = f"{username}/{now}.jpg"
    return key

# 이미지 즉시 업로드
class ImageUploadView(APIView):
    def post(self, request):
        image = request.data["file"]
        url = upload_s3(image, request.user.username)
        return Response({"message": "업로드 완료", "url": url}, status=status.HTTP_200_OK)        

# Create your views here.
class QuestionView(APIView):
    # 질문글 상세 보여주기 API
    def get(self, request, question_id):
        target_question = QnAQuestionModel.objects.get(id=question_id)
        return Response(QuestionSerializer(target_question).data)
    
    # 질문글 작성하기 API
    def post(self, request):
        question_serializer = QuestionSerializer(data=request.data)
        user = request.user.username
        if question_serializer.is_valid():
            question_serializer.save(user=self.request.user)
            try:
                image = f"media/{request.data['image']}"
                key = change_naming(image, user)
                question_serializer.save(image=key)
                upload_thumbnail_s3(image, user)
            except: 
                pass   
            return Response({"message":"질문글 작성에 성공했다북!"})
        return Response({"message":"질문글 작성에 실패했다북..."})
        
    # 질문글 수정하기 API
    def put(self, request, question_id):
        question = QnAQuestionModel.objects.get(id=question_id)
        user = request.user.username
        question_serializer = QuestionSerializer(question, data=request.data, partial=True)
        if question_serializer.is_valid():
            question_serializer.save(user=self.request.user)
            try:
                image = f"media/{request.data['image']}"
                key = change_naming(image, user)
                question_serializer.save(image=key)
                upload_thumbnail_s3(image, user)
            except:
                pass
            return Response({"message":"수정에 성공했다북!"}, status=status.HTTP_200_OK)
        return Response({"message":"수정할 내용을 전부 입력해라북!"}, status=status.HTTP_400_BAD_REQUEST)

    # 질문글 삭제하기 API
    def delete(self, request, question_id):
        question = QnAQuestionModel.objects.get(id=question_id)
        question.delete()
        return Response({"message":"질문 게시글이 삭제되었다북!"}, status=status.HTTP_200_OK)
    

class AnswerView(APIView):
    # 답변글 보여주기 API
    def get(self, request, answer_id):
        target_answer = QnAAnswerModel.objects.get(id=answer_id)
        return Response (AnswerSerializer(target_answer).data)
    
    # 답변글 작성하기 API
    def post(self, request, question_id):
        target_question = QnAQuestionModel.objects.get(id=question_id)
        user = request.user.username
        answer_serializer = AnswerSerializer(data=request.data)
        if answer_serializer.is_valid():
            after_valid_datas = {
                "user": request.user,
                "question":target_question,
                "is_selected": False
            }
            answer_serializer.save(**after_valid_datas)
            try:
                image = f"media/{request.data['image']}"
                key = change_naming(image, user)
                answer_serializer.save(image=key)
                upload_thumbnail_s3(image, user)
            except:
                pass
            return Response({"message": "답변 작성 고맙거북"}, status=status.HTTP_200_OK)
        return Response({"message": "답변 작성 실패거북"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 답변글 수정하기
    def put(self, request, answer_id):
        answer = QnAAnswerModel.objects.get(id=answer_id)
        answer_serializer = AnswerSerializer(answer, data=request.data, partial=True)
        user = request.user.username #이미지 이름바꾸기위해 한거고
        if answer_serializer.is_valid():
            answer_serializer.save(user=self.request.user)
            try:
                image = f"media/{request.data['image']}"
                key = change_naming(image, user)
                answer_serializer.save(image=key)
                upload_thumbnail_s3(image, user)
            except:
                pass
            return Response({"message":"답변 수정됐다북"}, status=status.HTTP_200_OK)
        return Response({"message":"답변 수정에 실패했다북!"}, status=status.HTTP_400_BAD_REQUEST)
    # 답변글 삭제하기 API
    def delete(self, request, answer_id):
        answer = QnAAnswerModel.objects.get(id=answer_id)
        answer.delete()

        return Response({"message":"소중한 답변이 삭제됐다북"})

# 질문글 목록 보기 API
class QuestionlistView(APIView):
    def get(self, request):
        questions = QnAQuestionModel.objects.all().order_by('-created_at')
        return Response(QuestionSerializer(questions, many=True).data)
    

class QuestionSearchView(generics.ListAPIView):
        queryset = QnAQuestionModel.objects.all().order_by('-created_at')
        serializer_class = QuestionSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['user__nickname', 'title', 'content', 'hashtag']
        

class LikeQuestionView(APIView):
    def post(self, request, question_id):
        user = request.user
        target_question_like = QuestionLikeModel.objects.filter(question=question_id, user=user)
        if not target_question_like:
            target_question = QnAQuestionModel.objects.get(id=question_id)
            target_question_like = QuestionLikeModel.objects.create(question=target_question, user=user)
            return Response({"message":"좋아요를 눌렀다북!"},status=status.HTTP_200_OK)
        target_question_like.delete()
        return Response({"message":"좋아요를 취소했다북.."},status=status.HTTP_200_OK)


class LikeAnswerView(APIView):
    def post(self, request, answer_id):
        user = request.user
        target_answer_like = AnswerLikeModel.objects.filter(answer=answer_id, user=user)
        if not target_answer_like:
            target_answer = QnAAnswerModel.objects.get(id=answer_id)
            target_answer_like = AnswerLikeModel.objects.create(answer=target_answer, user=user)
            return Response({"message":"좋아요를 눌렀다북!"},status=status.HTTP_200_OK)
        target_answer_like.delete()
        return Response({"message":"좋아요를 취소했다북.."},status=status.HTTP_200_OK)
        
        
class QuestionRecommendView(APIView):
    def post(self, request, question_id):
        target_hashtag = QnAQuestionModel.objects.get(id=question_id).hashtag
        all_data_hashtag = QnAQuestionModel.objects.exclude(id=question_id)
        all_hashtag_list = [
            {
                "id":excluded_data.id,
                "hashtag":excluded_data.hashtag
                } for excluded_data in all_data_hashtag]
        
        result = return_five_recommends(target_hashtag, all_hashtag_list)

        target_reco_list = []
        for i in result:
            target_reco_list.append(QnAQuestionModel.objects.get(id=i))
            
        return Response(QuestionSerializer(target_reco_list, many=True).data)
        
        
        
