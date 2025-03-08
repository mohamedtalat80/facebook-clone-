from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import login,logout ,authenticate
from .forms import *
from django.db.models import Subquery, OuterRef,Exists 
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import postform
from .models import post,comment 
from rest_framework import viewsets
from .serializers import  *
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action 
from rest_framework import status

class PostViewSet(viewsets.ModelViewSet):
    queryset = post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can modify posts, others can view them
    def perform_create(self, serializer):
        print(f"User in perform_create: {self.request.user}") 
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return post.objects.prefetch_related('comments', 'likes').all()
    @action(detail=False, methods=['post'])
    def create_post(self, request):
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)  # Assign the current user to the post
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['put'])
    def update_post(self, request, pk=None):
        post_instance = self.get_object()
        if post_instance.user != request.user:
            return Response({"detail": "Not authorized to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_post(self, request, pk=None):
        post_instance = self.get_object()
        if post_instance.user != request.user:
            return Response({"detail": "Not authorized to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
        post_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        print(f"User in perform_create: {self.request.user}") 
        serializer.save(user_comment=self.request.user)
        
    @action(detail=False, methods=['post'])
    def add_comment(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_comment=request.user)  # إضافة المستخدم الذي أضاف التعليق
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print(f"User in perform_create: {self.request.user}") 
        serializer.save(user_like=self.request.user)
        
    @action(detail=False, methods=['post'])
    def toggle_like(self, request):
        post_id = request.data.get('post_id')
        post_to_like = post.objects.get(id=post_id)

        # التحقق إذا كان المستخدم قد أعجب بالبوست
        existing_like = like.objects.filter(user_like=request.user, post_like=post_to_like).first()

        if existing_like:
            # إذا كان قد أعجب بالفعل، نقوم بإلغاء الإعجاب
            existing_like.delete()
            return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        else:
            # إذا لم يكن قد أعجب من قبل، نقوم بإضافة الإعجاب
            like.objects.create(user_like=request.user, post_like=post_to_like, liked=True)
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
    
@login_required(login_url='login/')
def home(request):
    posts = post.objects.annotate(
        user_liked=Exists(
            like.objects.filter(
                user_like=request.user.id,
                post_like=OuterRef('pk'),
                liked=True
            )
        )
      
        
    )
    print(str(posts.query))
    print(request.user.id)
    if request.method == 'POST':
        form = postform(request.POST,request.FILES)
        comment_form = commentform(request.POST)
       
       
        if 'comment' in request.POST:
                if comment_form.is_valid():
                    post_id_1 = request.POST.get('post-id-1')
                    print("Debug: post-id-1 =", post_id_1)  # Add this line for debugging
                    post_to_comment = post.objects.filter(id=post_id_1).first()
                    print("Debug: post_to_comment =", post_to_comment)  # Add this line for debugging

                    if post_to_comment:
                        comment_of_the_user = comment_form.save(commit=False)
                        comment_of_the_user.user_comment = request.user
                        comment_of_the_user.post_comment = post_to_comment
                        comment_of_the_user.save()
                        print("Debug: Comment saved")  # Add this line for debugging
                        return redirect('home')  # Redirect to the 'home' page after adding a comment 
                    else:
                        print("Debug: Post not found")  # Add this line for debugging
                else:
                    print("Debug: Invalid comment form data")  # Add this line for debugging

        elif 'create_post' in request.POST:
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post
                new_post.save()
                return redirect('home')  # Redirect to the 'home' page after posting a new post
        elif 'post-id-3' in request.POST:
            post_id = request.POST.get("post-id-3")
            print(post_id)
            post_to_delete = post.objects.filter(id=post_id, user=request.user).first()
            print(post_to_delete)
            if post_to_delete and post_to_delete.user == request.user:
                post_to_delete.delete()
                return redirect('home')  # Redirect to the 'home' page after deleting a post
        elif 'like' in request.POST:
            post_id_2 = request.POST.get('post-id-2')
            post_to_like = get_object_or_404(post, id=post_id_2)
            user_liked = like.objects.filter(user_like=request.user, post_like=post_to_like).first()
            if user_liked:
                
                # User has already liked the post, so unlike it
                user_liked.delete()
            else:
                
                # User hasn't liked the post, so like it
                like.objects.create(user_like=request.user, post_like=post_to_like,liked=True)
            return redirect('home')
                
    else:
        form = postform()
        comment_form = commentform()
      
    context = {
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
        
        
    }
    return render(request, 'home.html', context)

@login_required(login_url='login/')
def create_profile(request):
    profile_creating = ProfileForm()

    if request.method == 'POST':
        if 'skip' in request.POST:
            print("Skip button pressed")
            return redirect('home')
        elif 'create-profile' in request.POST:
            profile_creating = ProfileForm(request.POST, request.FILES)
            if profile_creating.is_valid():
                profile_instance = profile_creating.save(commit=False)
                profile_instance.user = request.user
                profile_instance.save()
                print("Profile created successfully")
                return redirect('home')
            else:
                print("Form validation errors:", profile_creating.errors)
        else:
            print("Unknown POST request")

    return render(request, 'profile_form.html', {'profile': profile_creating})
    
      
@login_required(login_url='login/')
def user_posts(request, username):
    user_profile = get_object_or_404(profile, user__username=username)
    user_posts = post.objects.filter(user__username=username)
    context = {
        'user_posts': user_posts,
        'target_user': username,
        'profile_content':user_profile,
    }
    return render(request, 'user_posts.html', context)
@login_required(login_url='login/')
def edit_post(request,postid):
    post_to_edit=post.objects.get(id=postid)
    if request.method == 'POST':
        Post_editing=postform(request.POST,request.FILES,instance=post_to_edit)
        if Post_editing.is_valid():
            Post=Post_editing.save()
            Post.user=request.user
            Post.save()
            return redirect('home')
    else:
        Post_editing=postform(instance=post_to_edit)
    return render(request,'editpost.html',{'form':Post_editing})
def register(request):
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)  # Use the saved user instance for login
            return redirect('create_profile')
    else:
        form = registerform()
    return render(request, 'registration/regitration.html', {'form': form})
@login_required(login_url='login/')
def createpost(request):
    if request.method == 'POST':
        form = postform(request.POST,request.FILES)
        if form.is_valid():
            Post=form.save(commit=False)
            Post.user=request.user
            Post.save()
            return redirect('/home')
    else:
        form = postform()
    return render(request, 'createpost.html', {'form': form})
    
def log_out(request):
    logout(request)
    return redirect('login')        

 
@login_required(login_url='login/')
def reply_to_comment(request, comment_id):
    comment_to_reply = get_object_or_404(comment, id=comment_id)

    if request.method == 'POST':
        reply_form = commentform(request.POST)
        if reply_form.is_valid():
            post_of_comment = comment_to_reply.post_comment

            reply_of_comment = reply_form.save(commit=False)
            reply_of_comment.user_comment = request.user
            reply_of_comment.post_comment = post_of_comment
            reply_of_comment.reply = comment_to_reply
            reply_of_comment.is_reply=True
            reply_of_comment.save()

            return redirect(request.path)

    else:
        reply_form = commentform()

    context = {
        'reply_form': reply_form,
        'comment': comment_to_reply,
    }

    return render(request,'reply.html',context)     
    