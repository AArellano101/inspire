import os
from .models import *
from inspire_project.settings import BASE_DIR

commonwords = []

def notify(user, notification):
    n = Notification.objects.create_notification(notification)
    n.save()

    InspireUser.objects.add_notification(user, n.id)

def text_or_video(category):
    if category == "quote":
        return "text"
    elif category == "speech":
        return "video"
    elif category == "article":
        return "text"
    elif category == "movie":
        return "text"
    elif category == "album":
        return "text"

def get_featured():
    featured_quote = Text.objects.filter(featured=True, category="quote")[0]
    featured_speech = Video.objects.filter(featured=True, category="speech")[0]
    featured_article = Text.objects.filter(featured=True, category="article")[0]
    featured_movie = Text.objects.filter(featured=True, category="movie")[0]
    featured_album = Text.objects.filter(featured=True, category="album")[0]
    return {"quote": featured_quote, "speech": featured_speech, 
            "article": featured_article, "movie": featured_movie,
            "album": featured_album}

def get_liked(user, posts):
    liked = {}
    favourites = user.favourites
    for post in posts:
        postid = post.postid
        favourite = Favourite.objects.filter(category=post.category, postid=postid)
        if favourite.exists():
            fid = favourite[0].id
            if fid in favourites:
                liked[postid] = True
            else:
                liked[postid] = False
        else:
            liked[postid] = False

    return liked

def readable_datetime(date):
    months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"June",
              7:"July",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    
    month = months[int(date.strftime("%m"))]
    day = date.strftime("%d")
    year = date.strftime("%Y")  
    time = date.strftime("%H:%M")

    return f"{month} {day}, {year} - {time}"

def like(user, body):
    category = body["category"]
    id = body["id"]
    f = Favourite.objects.filter(category=category, postid=id)
    if not f.exists():
        f = Favourite.objects.create_favourite(category, id)
    else:
        f = f[0]

    if f.id not in user.favourites:
        InspireUser.objects.add_favourite(user, f.id)

def unlike(user, body):
    category = body["category"]
    id = body["id"]
    f = Favourite.objects.filter(category=category, postid=id)[0]

    InspireUser.objects.remove_favourite(user, f.id)

def handle_like(user, body):
    if body["type"] == "like":
        like(user, body)
    if body["type"] == "unlike":
        unlike(user, body)

def get_post(postid):
    post = Text.objects.filter(postid=postid)
    if post.exists():
        return post[0]
    
    post = Video.objects.filter(postid=postid)
    if post.exists():
        return post[0]
    
    return None

def load_common_words():
    global commonwords
    file_path = os.path.join(BASE_DIR, 'inspire/static/commonwords.txt')
    with open(file_path) as commonwords_file:
        commonwords = commonwords_file.read().splitlines()

def compare(s1, s2):
    def countOccurrences(l):
        o = {}
        for w in l:
            if w in o:
                o[w] += 1
            else:
                o[w] = 1

        return o
    
    def unique_words(s):
        global commonwords
        punc = [".",",","!","?"]
        s = s.split(' ')
        for i in range(len(s)):
            w =  s[i]
            for p in punc:
                if p in w:
                    w = w.replace(p, "")   
            w = w.lower()
            s[i] = w

        for common_word in commonwords:
            if common_word in s:
                s = list(filter((common_word).__ne__, s))
                
        return s
    
    score = 0

    s1 = unique_words(s1)
    s2 = unique_words(s2)
    
    shared = list(set(s1) & set(s2))

    o1 = countOccurrences(s1)
    o2 = countOccurrences(s2)
    
    score += len(shared) * 100
    
    for word in shared:
        score += o1[word] + o2[word]
    
    return score