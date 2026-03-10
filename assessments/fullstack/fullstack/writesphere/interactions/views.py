from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import models
from .models import Like, Comment, Follow, Rating
from blog.models import Post

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        liked = False
        message = "Post unliked"
    else:
        liked = True
        message = "Post liked"
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count(),
            'message': message
        })
    
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        if content:
            parent = None
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)
            
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                parent=parent
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
                    'is_reply': bool(parent)
                })
            
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty!')
    
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'content': comment.content,
                    'updated_at': comment.updated_at.strftime('%B %d, %Y at %I:%M %p')
                })
            
            messages.success(request, 'Comment updated successfully!')
        else:
            messages.error(request, 'Comment cannot be empty!')
    
    return redirect('blog:post_detail', slug=comment.post.slug)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_slug = comment.post.slug
    
    if request.method == 'POST':
        comment.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Comment deleted successfully'
            })
        
        messages.success(request, 'Comment deleted successfully!')
    
    return redirect('blog:post_detail', slug=post_slug)

@login_required
@require_POST
def rate_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    score = int(request.POST.get('score', 0))
    
    if 1 <= score <= 5:
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'score': score}
        )
        
        avg_rating = post.ratings.aggregate(avg_rating=models.Avg('score'))['avg_rating']
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'user_rating': score,
                'avg_rating': round(avg_rating, 1) if avg_rating else 0,
                'ratings_count': post.ratings.count(),
                'message': f'Post rated {score} stars!'
            })
        
        messages.success(request, f'Post rated {score} stars!')
    else:
        messages.error(request, 'Invalid rating!')
    
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def user_following(request):
    following = request.user.following.select_related('following').order_by('-created_at')
    paginator = Paginator(following, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'interactions/following.html', {'page_obj': page_obj})

@login_required
def user_followers(request):
    followers = request.user.followers.select_related('follower').order_by('-created_at')
    paginator = Paginator(followers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'interactions/followers.html', {'page_obj': page_obj})
