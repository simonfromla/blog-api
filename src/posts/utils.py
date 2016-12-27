import datetime
import math
import re

from django.utils.html import strip_tags

# The read_time, as a field, is first defined as a field in Post.
# Then, the function/logic of the function is created here.
# Then, in Post, it is saved into the DB with the pre_save_post_receiver function.
# It is then implemented/manipulated by way of its instance in the template, post_detail.html

def count_words(html_string):
    # html_string = """
    # <h1> this is a string</h1>
    # """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0) #assumes 200wpm
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))


    # read_time = datetime.timedelta(minutes=read_time_min)
    # read_time = str(datetime.timedelta(minutes=read_time_min)) # no longer need this since changed to IntegerField
    # return read_time
    return int(read_time_min)