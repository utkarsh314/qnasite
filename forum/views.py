from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Answer, Vote, AnswerVote

# Create your views here.
class HomeView(generic.ListView):
    model = Question
    template_name = 'forum/home.html'
    context_object_name = 'questions'
    ordering = ['-date_posted']

class QuestionView(generic.DetailView):
    model = Question
    template_name = 'forum/detail.html'
    context_object_name = 'question'

class NewQuestionView(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ['Title', 'Body']

    def form_valid(self, form):
        form.instance.Asked_By = self.request.user
        return super().form_valid(form)

class NewAnswerView(LoginRequiredMixin, generic.CreateView):
    model = Answer
    fields = ['Body']

    def form_valid(self, form):
        form.instance.Answered_By = self.request.user
        question = get_object_or_404(Question, id=self.kwargs['pk'])
        form.instance.Question_Answered = question
        return super().form_valid(form)

    def get_success_url(self):
        question = get_object_or_404(Question, id=self.kwargs['pk'])
        return reverse('question', kwargs={'pk': question.pk})

class EditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Question
    fields = ['Title', 'Body']

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.Asked_By:
            return True
        return False

class DeleteQView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.Asked_By:
            return True
        return False

@login_required
def upvote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
   
    if request.user.pk != question.Asked_By.pk:
            if Vote.objects.filter(voter=request.user, question=question, upvote=True).exists():
               messages.warning(request, 'you can not upvote more than once!')
               return HttpResponseRedirect(reverse('question', kwargs={'pk': question.id}))

            elif Vote.objects.filter(voter=request.user, question=question, upvote=False).exists():
                vote = Vote.objects.filter(voter=request.user, question=question)
                vote.update(upvote=True)
                question.votes += 2
                question.save()

            else:
              vote = Vote.objects.create(voter=request.user, question=question, upvote=True)
              vote.save()
              question.votes += 1
              question.save()

    return HttpResponseRedirect(reverse('question', kwargs={'pk': question.id}))

@login_required
def downvote(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user.pk != question.Asked_By.pk:
            if Vote.objects.filter(voter=request.user, question=question, upvote=False).exists():
               messages.warning(request, 'you can not downvote more than once!')
               return HttpResponseRedirect(reverse('question', kwargs={'pk': question.id}))

            elif Vote.objects.filter(voter=request.user, question=question, upvote=True).exists():
                vote = Vote.objects.filter(voter=request.user, question=question)
                vote.update(upvote=False)
                question.votes -= 2
                question.save()

            else:
              vote = Vote.objects.create(voter=request.user, question=question, upvote=False)
              vote.save()
              question.votes -= 1
              question.save()

    return HttpResponseRedirect(reverse('question', kwargs={'pk': question.id}))

@login_required
def removevote(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if Vote.objects.filter(voter=request.user, question=question, upvote=True).exists():
       question.votes -= 1
       question.save()

    elif Vote.objects.filter(voter=request.user, question=question, upvote=False).exists():
       question.votes += 1
       question.save()

    else:
       messages.warning(request, 'you have not voted on this post!')
       return HttpResponseRedirect(reverse('question', kwargs={'pk': question.id}))

    Vote.objects.filter(voter=request.user, question=question).delete()

    return HttpResponseRedirect(reverse('question', kwargs={'pk': question.id}))

@login_required
def answerupvote(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
   
    if request.user.pk != answer.Answered_By.pk:
            if AnswerVote.objects.filter(voter=request.user, answer=answer, upvote=True).exists():
               messages.warning(request, 'you can not upvote more than once!')
               return HttpResponseRedirect(reverse('question', kwargs={'pk': answer.Question_Answered.id}))

            elif AnswerVote.objects.filter(voter=request.user, answer=answer, upvote=False).exists():
                vote = AnswerVote.objects.filter(voter=request.user, answer=answer)
                vote.update(upvote=True)
                answer.votes += 2
                answer.save()

            else:
              vote = AnswerVote.objects.create(voter=request.user, answer=answer, upvote=True)
              vote.save()
              answer.votes += 1
              answer.save()

    return HttpResponseRedirect(reverse('question', kwargs={'pk': answer.Question_Answered.id}))

@login_required
def answerdownvote(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
   
    if request.user.pk != answer.Answered_By.pk:
            if AnswerVote.objects.filter(voter=request.user, answer=answer, upvote=False).exists():
               messages.warning(request, 'you can not downvote more than once!')
               return HttpResponseRedirect(reverse('question', kwargs={'pk': answer.Question_Answered.id}))

            elif AnswerVote.objects.filter(voter=request.user, answer=answer, upvote=True).exists():
                vote = AnswerVote.objects.filter(voter=request.user, answer=answer)
                vote.update(upvote=True)
                answer.votes -= 2
                answer.save()

            else:
              vote = AnswerVote.objects.create(voter=request.user, answer=answer, upvote=False)
              vote.save()
              answer.votes -= 1
              answer.save()

    return HttpResponseRedirect(reverse('question', kwargs={'pk': answer.Question_Answered.id}))

@login_required
def removeanswervote(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if AnswerVote.objects.filter(voter=request.user, answer=answer, upvote=True).exists():
       answer.votes -= 1
       answer.save()

    elif AnswerVote.objects.filter(voter=request.user, answer=answer, upvote=False).exists():
       answer.votes += 1
       answer.save()

    else:
       messages.warning(request, 'you have not voted on this answer!')
       return HttpResponseRedirect(reverse('question', kwargs={'pk': answer.Question_Answered.id}))

    AnswerVote.objects.filter(voter=request.user, answer=answer).delete()

    return HttpResponseRedirect(reverse('question', kwargs={'pk': answer.Question_Answered.id}))