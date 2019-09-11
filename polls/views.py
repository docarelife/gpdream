# -*- utf8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
# Create your views here.
#投票首页
from django.views import generic

from polls.models import Question,Choice


# def index(request):
#     latest_question_list=Question.objects.order_by('-pub_date')[:5]
#     content={'latest_question_list':latest_question_list}
#     return render(request,'polls/index.html',content)
#
# #投票详情
# def detail(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     content = {'question': question}
#     return render(request, 'polls/article_detail.html', content)

# #投票结果
# def results(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     content = {'question': question}
#     return render(request, 'polls/results.html', content)
#
# #投票进行中
# def vote(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     try:
#         selected_choice=question.choice_set.get(pk=request.POST['choice'])
#     except(KeyError,Choice.DoesNotExist):
#         content={'question':question,'error_message':'you didnot select a choice',}
#         return render(request,'polls/article_detail.html',content)
#     else:
#         selected_choice.votes+=1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))


#通用视图

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/article_detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        content={'question':question,'error_message':'you didnot select a choice',}
        return render(request,'polls/article_detail.html',content)
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))