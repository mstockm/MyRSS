import os,sys

sys.path.append(os.path.abspath('../..'))
execfile('user.py')
me = User('me', 'test@gmail.com')
me.add_feed('http://feeds2.feedburner.com/PitchforkLatestNews')
me.add_feed('http://feeds.feedburner.com/seriouseatsfeaturesvideos?format=xml')
me.add_feed('http://pandodaily.com.feedsportal.com/c/35141/f/650422/index.rss')
me.update_stream()
