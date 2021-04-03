from posts.models import Post

def delRejected():
    Post.rejected.all().delete()