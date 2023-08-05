import os
from random import randint
from .models import *
from inspire_project.settings import BASE_DIR
from django.forms.models import model_to_dict

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


def get_categories():
    cats = {
        "quote": {
            "bible-verse": {
                "old-testament": {},
                "new-testament": {}
            }
        },
        "speech": {},
        "article": {},
        "movie": {},
        "album": {}
    }

    return cats


def get_featured():
    featured_quote = Text.objects.filter(featured=True, category="quote")[0]
    featured_speech = Video.objects.filter(featured=True, category="speech")[0]
    featured_article = Text.objects.filter(
        featured=True, category="article")[0]
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
        favourite = Favourite.objects.filter(
            category=post.category, postid=postid)
        if favourite.exists():
            fid = favourite[0].id
            if fid in favourites:
                liked[postid] = True
            else:
                liked[postid] = False
        else:
            liked[postid] = False

    return liked


def get_num_likes(postid):
    if Favourite.objects.filter(postid=postid).exists():
        return Favourite.objects.get(postid=postid).likes
    return 0

def get_favs_postids(user):
    favs = user.favourites
    postids = []
    for fav in favs:
        postids.append(Favourite.objects.get(id=fav).postid)

    return postids


def readable_datetime(date):
    months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "June",
              7: "July", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

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
        if text_or_video(category) == "text":
            Text.objects.like(id)
        else:
            Video.objects.like(id)


def unlike(user, body):
    category = body["category"]
    id = body["id"]
    f = Favourite.objects.filter(category=category, postid=id)

    if f.exists():
        InspireUser.objects.remove_favourite(user, f[0].id)
        if text_or_video(category) == "text":
            Text.objects.unlike(id)
        else:
            Video.objects.unlike(id)


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


def get_posts(postids, d=False):
    if not d:
        return [get_post(p) for p in postids]
    return [model_to_dict(get_post(p)) for p in postids]


def load_common_words():
    global commonwords
    file_path = os.path.join(BASE_DIR, 'inspire/static/commonwords.txt')
    with open(file_path) as commonwords_file:
        commonwords = commonwords_file.read().splitlines()


def unique_words(s):
    global commonwords

    if not len(commonwords):
        load_common_words()

    punc = [".", ",", "!", "?", "-", chr(8212), "'s"]
    s = s.split(' ')
    for i in range(len(s)):
        w = s[i]
        for p in punc:
            if p in w:
                w = w.replace(p, "")
        w = w.lower()
        s[i] = w

    for common_word in commonwords:
        if common_word in s:
            s = list(filter((common_word).__ne__, s))

    s = list(filter(("").__ne__, s))

    return s


def countOccurrences(l):
    o = {}
    for w in l:
        if w in o:
            o[w] += 1
        else:
            o[w] = 1

    return o


def compare(s1, s2):
    score = 0

    shared = list(set(s1) & set(s2))

    o1 = countOccurrences(s1)
    o2 = countOccurrences(s2)

    score += len(shared) * 100

    for word in shared:
        score += o1[word] + o2[word]

    score += randint(0, 25)
    return score


def rv_ex(a):
    return list(set(a))


def cb_set(s1, s2):
    return set(list(s1)+list(s2))

def conv_q(q):
    if q == 'likes':
        q = '-likes'
    elif q == 'newest':
        q = '-created'
    elif q == 'oldest':
        q = 'created'
    elif q == 'random':
        q = '?'
    elif q == 'recentliked':
        q == 'recentliked'
    elif q == 'oldestliked':
        q == 'oldestliked'
    return q

def similar_posts(postid, pavoid=[], num=10):
    post = get_post(postid)
    ptype = text_or_video(post.category)

    if not post:
        return None

    title_tags = rv_ex(unique_words(post.title))
    des_tags = rv_ex(unique_words(post.description))

    db_results = {}

    db_results_t = set()
    for t_tag in title_tags:
        db_results_t = cb_set(db_results_t, set(Text.objects.filter(
            title__icontains=t_tag).order_by('-id')[:100]))
        db_results_t = cb_set(db_results_t, set(Video.objects.filter(
            title__icontains=t_tag).order_by('-id')[:25]))

    db_results_t = list(db_results_t)
    for t in db_results_t:
        if t.postid not in pavoid and t.postid != postid:
            db_results[t.postid] = compare(post.title, t.title)

    db_results_d = set()

    for d_tag in des_tags:
        db_results_d = cb_set(db_results_d, set(Text.objects.filter(
            description__icontains=d_tag).order_by('-id')[:100]))
        db_results_d = cb_set(db_results_d, set(Video.objects.filter(
            description__icontains=d_tag).order_by('-id')[:25]))

    db_results_d = list(db_results_d)
    for d in db_results_d:
        if d in db_results:
            i = compare(post.description, d.description)
            if db_results[d.postid] < i:
                db_results[d.postid] = i
        else:
            if d.postid not in pavoid and d.postid != postid:
                db_results[d.postid] = compare(post.description, d.description)

    if ptype == "text":
        text_tags = rv_ex(unique_words(post.text))
        db_results_te = set()
        for te_tag in text_tags:
            db_results_te = cb_set(db_results_te, set(Text.objects.filter(
                text__icontains=te_tag).order_by('-id')[:100]))

        db_results_te = list(db_results_te)
        for d in db_results_te:
            if d in db_results:
                i = compare(post.text, d.text)
                if db_results[d.postid] < i:
                    db_results[d.postid] = i
            else:
                if d.postid not in pavoid and d.postid != postid:
                    db_results[d.postid] = compare(post.text, d.text)

    db_results = dict(
        sorted(db_results.items(), key=lambda item: item[1], reverse=True))
    db_results = list(db_results)[:num]

    return db_results


def searchquery(query, pavoid=[], num=10):
    q_words = rv_ex(unique_words(query))

    db_results = {}

    db_results_t = set()
    db_results_d = set()
    db_results_te = set()

    for q_word in q_words:
        db_results_t = cb_set(db_results_t, set(Text.objects.filter(
            title__icontains=q_word).order_by('-id')[:100]))
        db_results_t = cb_set(db_results_t, set(Video.objects.filter(
            title__icontains=q_word).order_by('-id')[:25]))

        db_results_d = cb_set(db_results_d, set(Text.objects.filter(
            description__icontains=q_word).order_by('-id')[:100]))
        db_results_d = cb_set(db_results_d, set(Video.objects.filter(
            description__icontains=q_word).order_by('-id')[:25]))
       
        db_results_ta = set(Text.objects.filter(
        tags__contains=[q_word]).order_by('-likes')[:100])
        print(db_results_ta)
        db_results_ta = cb_set(db_results_ta, set(Video.objects.filter(
            tags__contains=[q_word]).order_by('-likes')[:25]))

        db_results_te = cb_set(db_results_te, set(Text.objects.filter(
            text__icontains=q_word).order_by('-id')[:100]))

    db_results_t = list(db_results_t)
    for t in db_results_t:
        if t.postid not in pavoid:
            db_results[t.postid] = compare(query, t.title)

    db_results_d = list(db_results_d)
    for d in db_results_d:
        if d in db_results:
            i = compare(query, d.description)
            if db_results[d.postid] < i:
                db_results[d.postid] = i
        else:
            if d.postid not in pavoid:
                db_results[d.postid] = compare(query, d.description)

    db_results_ta = list(db_results_ta)
    for d in db_results_ta:
        if d in db_results:
            i = compare(query, ' '.join(d.tags))
            if db_results[d.postid] < i:
                db_results[d.postid] = i
        else:
            if d.postid not in pavoid:
                db_results[d.postid] = compare(query, ' '.join(d.tags))

    db_results_te = list(db_results_te)
    for d in db_results_te:
        if d in db_results:
            i = compare(query, d.text)
            if db_results[d.postid] < i:
                db_results[d.postid] = i
        else:
            if d.postid not in pavoid:
                db_results[d.postid] = compare(query, d.text)

    db_results = dict(
        sorted(db_results.items(), key=lambda item: item[1], reverse=True))
    db_results = list(db_results)[:num]

    return db_results


def tagquery(tag, pavoid=[], num=10):
    db_results = {}

    db_results_r = set(Text.objects.filter(
        tags__contains=[tag]).order_by('-likes')[:100])
    db_results_r = cb_set(db_results_r, set(Video.objects.filter(
        tags__contains=[tag]).order_by('-likes')[:25]))

    db_results_r = list(db_results_r)
    for r in db_results_r:
        if r.postid not in pavoid:
            db_results[r.postid] = r.likes

    db_results = dict(
        sorted(db_results.items(), key=lambda item: item[1], reverse=True))
    db_results = list(db_results)[:num]
    return db_results

def order_query(q, db_results_r, pavoid):
    db_results = {}
    db_results_r = list(db_results_r)

    for r in db_results_r:
        if r.postid not in pavoid:
            if q == '-likes':
                db_results[r.postid] = r.likes
            elif q == '-created' or q == 'created':
                db_results[r.postid] = r.created
            elif q == '?':
                db_results[r.postid] = randint(0, 1000)

    if q in ['-likes', '-created', 'created', '?']:
        if q == '-likes' or q == '-created' or q == '?':
            db_results = dict(
                sorted(db_results.items(), key=lambda item: item[1], reverse=True))
        elif q == 'created':
            db_results = dict(
                sorted(db_results.items(), key=lambda item: item[1]))
            
    return db_results


def catquery(cat, sc=False, q='likes', pavoid=[], num=10):
    q = conv_q(q)

    if not sc:
        db_results_r = set(Text.objects.filter(category=cat).order_by(q)[:100])
        db_results_r = cb_set(db_results_r, set(Video.objects.filter(category=cat)
                                                .order_by(q)[:25]))
    else:
        db_results_r = set(Text.objects.filter(
            subcategories__contains=[cat]).order_by(q)[:100])
        db_results_r = cb_set(db_results_r, set(Video.objects.filter(
            subcategories__contains=[cat]).order_by(q)[:25]))

    db_results = order_query(q, db_results_r, pavoid)

    db_results = list(db_results)[:num]
    return db_results


def allquery(q='likes', pavoid=[], num=10):
    q = conv_q(q)

    db_results_r = set(Text.objects.all().order_by(q)[:100])
    db_results_r = cb_set(db_results_r, set(Video.objects.all()
                                            .order_by(q)[:25]))
    db_results = order_query(q, db_results_r, pavoid)
    db_results = list(db_results)[:num]
    return db_results

def favquery(user, q='recentliked', pavoid=[], num=10):
    q = conv_q(q)
    favs = get_favs_postids(user)
    if q == 'recentliked' or q == 'oldestliked':
        db_results = [fav for fav in favs if fav not in pavoid]
        if q == 'oldestliked':
            db_results.reverse()
    else:
        db_results_r = set(Text.objects.filter(postid__in=favs).order_by(q)[:100])
        db_results_r = cb_set(db_results_r, 
                    set(Video.objects.filter(postid__in=favs).order_by(q)[:25]))
        
        db_results = order_query(q, db_results_r, pavoid)

    db_results = list(db_results)[:num]
    return db_results
