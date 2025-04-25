BUGS 

BUG: When I ran the server, received the following error:
 File "/Users/vikimulhall/GAA_STORE/products/views.py", line 1, in <module>
    from django.shortcuts import renderget_object_or_404
ImportError: cannot import name 'renderget_object_or_404' from 'django.shortcuts' (/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/django/shortcuts.py). Did you mean: 'get_object_or_404'?
RESOLVED BY: Went to my views.py file and saw I had a typo in the import line. Amended and started server again. 

BUG: After adding the the hurley page, it wouldn't display and sent the following error in the terminal:
Not Found: /hurleys/
[25/Apr/2025 15:06:51] "GET /hurleys/ HTTP/1.1" 404 2717
RESOLVED BY: Realised I had forgotten to include the products app in the main urls.py. I then also included the hurling page itself. 

 BUG: Hurley images not being displayed & not consistent size.  
 RESOLVED BY: Changed location of images to the static folder, restarted server, only the ash image displayed, checked for typos, found dashes rather than hyphens, ameneded in the html page and resolved problem. To fix the inconsistent size of the ash hurley image compared to the other two, I added some css, which did not work, so I fixed the image again in canva and resaved and loaded and it worked when refreshed. 

 




